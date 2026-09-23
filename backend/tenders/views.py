from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from risk_service import calculate_risk
from .models import (
    Tender,
    TenderIntelligence,
    BidReadinessAnalysis,
    BidAnalysis
)
from .serializers import (
    TenderSerializer,
    TenderQuestionSerializer,
    TenderIntelligenceSerializer,
    BidReadinessAnalysisSerializer,
    BidAnalysisSerializer
)

from django.shortcuts import get_object_or_404
from django.db import transaction

from documents.processor import process_tender_document
from rag_service import answer_question

class TenderIntelligenceView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, tender_id):

        tender = get_object_or_404(
            Tender,
            id=tender_id,
            user=request.user
        )

        intelligence = get_object_or_404(
            TenderIntelligence,
            tender=tender
        )

        serializer = TenderIntelligenceSerializer(intelligence)

        return Response(serializer.data)

class TenderListCreateView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request):
        serializer=TenderSerializer(data=request.data)

        if serializer.is_valid():
            with transaction.atomic():
                tender=serializer.save(
                    user=request.user
                )

                if tender.document:
                    process_tender_document(tender)
            return Response(
                TenderSerializer(tender).data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def get(self, request):
        tenders = Tender.objects.filter(user=request.user)
        serializer = TenderSerializer(tenders, many=True)

        return Response(serializer.data)



class TenderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, request, pk):
        try:
            return Tender.objects.get(
                pk=pk,
                user=request.user
            )
        except Tender.DoesNotExist:
            return None

    def get(self, request, pk):
        tender = self.get_object(request, pk)

        if not tender:
            return Response(
                {"detail": "Tender not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(TenderSerializer(tender).data)

    def delete(self, request, pk):
        tender = self.get_object(request, pk)

        if not tender:
            return Response(
                {"detail": "Tender not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        tender.delete()

        return Response(
            {"message": "Tender deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )

class TenderQuestionView(APIView):

    def post(self, request, tender_id):

        serializer = TenderQuestionSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        question = serializer.validated_data["question"]
        history = serializer.validated_data.get("history", [])
        try:
            tender = Tender.objects.get(
                id=tender_id,
                user=request.user
            )
        except Tender.DoesNotExist:
            return Response(
                {"detail": "Tender not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        result = answer_question(
    question=question,
    tender_id=tender.id,
    history=history
)

        return Response(
            result,
            status=status.HTTP_200_OK
        )


class BidReadinessView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, tender_id):

        tender = get_object_or_404(
            Tender,
            id=tender_id,
            user=request.user
        )

        analysis = get_object_or_404(
            BidReadinessAnalysis,
            tender=tender,
            company__user=request.user
        )

        serializer = BidReadinessAnalysisSerializer(analysis)

        return Response(serializer.data)


class BidAnalysisView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, tender_id):

        tender = get_object_or_404(
            Tender,
            id=tender_id,
            user=request.user
        )

        analysis = get_object_or_404(
            BidAnalysis,
            tender=tender,
            company__user=request.user
        )

        serializer = BidAnalysisSerializer(analysis)

        return Response(serializer.data)

class TenderOverView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request,tender_id):
        tender = get_object_or_404(
        Tender.objects.select_related("Intelligence"),
        id=tender_id,
        user=request.user
        )

        intelligence=TenderIntelligence.objects.filter(
            tender=tender
        ).first()

        readiness=BidReadinessAnalysis.objects.filter(
            tender=tender,
            company__user=request.user
        ).order_by("-updated_at").first()

        bid_analysis=BidAnalysis.objects.filter(
            tender=tender,
            company__user=request.user
        ).order_by("-updated_at").first()


        summary = {
        "score": readiness.score if readiness else None,
        "readiness": readiness.readiness if readiness else None,
        "bid_ready": readiness.bid_ready if readiness else None,
        "critical_missing_requirements": (
        readiness.critical_missing_requirements
        if readiness else []
        ),
        "recommendation": (
        bid_analysis.recommendation
        if bid_analysis else None
            )
        }

        return Response({
            "summary":summary,
            "tender":TenderSerializer(tender).data,
            "intelligence":(
                TenderIntelligenceSerializer(intelligence).data
                if intelligence else None
            ),
            "readiness": (
                BidReadinessAnalysisSerializer(readiness).data
                if readiness else None
            ),
            "bid_analysis": (
                BidAnalysisSerializer(bid_analysis).data
                if bid_analysis else None
            ),

        })


class TenderDashboardStatsView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        total_tenders=Tender.objects.filter(user=request.user).count()

        bid_ready=BidReadinessAnalysis.objects.filter(
            company__user=request.user,
            bid_ready=True
        ).values("tender").distinct().count()

        needs_attention=BidReadinessAnalysis.objects.filter(
            company__user=request.user,
            bid_ready=False
        ).values("tender").distinct().count()

        return Response({
            "total_tenders":total_tenders,
            "bid_ready":bid_ready,
            "needs_attention":needs_attention
        })
class TenderRiskView(APIView):

    def get(self, request, tender_id):

        try:
            tender = Tender.objects.get(
                id=tender_id,
                user=request.user
            )
        except Tender.DoesNotExist:
            return Response(
                {"detail": "Tender not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            intelligence = TenderIntelligence.objects.get(
                tender=tender
            )
        except TenderIntelligence.DoesNotExist:
            return Response(
                {
                    "detail": "Tender intelligence is not available."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        intelligence_data = {
            "eligibility_requirements": intelligence.eligibility_requirements,
            "financial_requirements": intelligence.financial_requirements,
            "technical_requirements": intelligence.technical_requirements,
            "experience_requirements": intelligence.experience_requirements,
            "required_documents": intelligence.required_documents,
            "deadlines": intelligence.deadlines,
            "project_duration": intelligence.project_duration,
            "penalties": intelligence.penalties,
        }

        risk = calculate_risk(intelligence_data)

        return Response(
            risk,
            status=status.HTTP_200_OK
        )
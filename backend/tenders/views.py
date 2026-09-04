from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Tender
from .serializers import TenderSerializer

class TenderListCreateView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request):
        serializer=TenderSerializer(data=request.data)

        if serializer.is_valid():
            tender=serializer.save(user=request.user)

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
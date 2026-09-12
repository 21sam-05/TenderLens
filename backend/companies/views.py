from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import CompanyProfile
from .serializers import CompanyProfileSerializer
class CompanyProfileView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request):
        serializer=CompanyProfileSerializer(data=request.data)
        if serializer.is_valid():
            company=serializer.save(user=request.user)

            return Response(
                CompanyProfileSerializer(company).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    def get(self,request):
        try:
            company=CompanyProfile.objects.get(user=request.user)
        except CompanyProfile.DoesNotExist:
            return Response(
                {"detail": "Company profile not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(CompanyProfileSerializer(company).data)


    def patch(self,request):
        try:
            company=CompanyProfile.objects.get(
                user=request.user
            )
        except CompanyProfile.DoesNotExist:
            return Response(
                {"detail":"Company profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer=CompanyProfileSerializer(
            company,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
        

    



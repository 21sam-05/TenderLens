

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import RegisterSerializer

class RegisterView(APIView):
    def post(self,request):
        serializer=RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user=serializer.save()

            return Response({
                "message":"user registered successfullyy",
                "user_id":user.id,
                "email":user.email,
            },
            status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

class MeView(APIView):
    #nobody can acess this endpoint unless they are authenticated
    
    permission_classes=[IsAuthenticated]

    def get(self,request):
        return Response({
            'id':request.user.id,
            'email':request.user.email,
            'first_name':request.user.first_name,
            'last_name':request.user.last_name,
        })


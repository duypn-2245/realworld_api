from rest_framework import permissions
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from users.serializers import UserInfoSerializer, RegisterSerilizer

class Register(APIView):
    """
    Register new user
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        serializer = RegisterSerilizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(UserInfoSerializer(serializer.data).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserInfor(APIView):
    """
    Retrive , update a user
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserInfoSerializer(request.user)
        return Response({'user': serializer.data})
    
    def put(self, request, format=None):
        data = request.data.get('user', {})
        serializer = UserInfoSerializer(request.user, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

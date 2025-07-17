from rest_framework import permissions
from rest_framework import status
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import User
from users.serializers import UserInfoSerializer, RegisterSerilizer

class UserList(APIView):
    """
    Register new user
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        serializer = RegisterSerilizer(data=request.data)
        if serializer.is_valid():
            serializer.create()
            return Response(UserInfoSerializer(serializer.data).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetail(APIView):
    """
    Retrive , update a user
    """
    def get_user(self, username, format=None):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, username, format=None):
        user = self.get_user(username)
        serializer = UserInfoSerializer(user)
        return Response(serializer.data)
    
    def put(self, request, username, format=None):
        user = self.get_user(username)
        serializer = UserInfoSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import permissions, status, generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from users.models import User
from .permissions import IsFollowAnotherUser, IsFollowingAnotherUser
from .models import UserFollowing
from users.serializers import ProfileSerializer

class Follow(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsFollowAnotherUser]
    serializer_class = ProfileSerializer

    def get_following(self):
        user = self.request.user
        if user.id is not None:
            return user.following.all()
        return []

    def create(self, request, *args, **kwargs):
        user_to = get_object_or_404(User.objects, username=self.kwargs["username"])
        self.check_object_permissions(self.request, user_to)
        user_follow = UserFollowing.objects.filter(user_from=self.request.user, user_to=user_to).first()
        if user_follow is not None:
            UserFollowing.objects.create(user_from=self.request.user, user_to=user_to)
        
        serializer = self.get_serializer(user_to, context={"following": self.get_following()})
        return Response({"user": serializer.data}, status=status.HTTP_200_OK)

class UnFollow(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsFollowingAnotherUser]
    serializer_class = ProfileSerializer

    def destroy(self, request, *args, **kwargs):
        user_to = get_object_or_404(User.objects, username=self.kwargs["username"])
        user_follow = UserFollowing.objects.filter(user_from=self.request.user, user_to=user_to).first()
        if user_follow is not None:
            self.check_object_permissions(self.request, user_follow)
            user_follow.delete()
        
        serializer = self.get_serializer(user_to, context={"following": self.get_following()})
        return Response({"user": serializer.data}, status=status.HTTP_200_OK)

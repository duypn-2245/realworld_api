from rest_framework import permissions, status, generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from users.models import User
from .permissions import IsFollowAnotherUser, IsFollowingAnotherUser
from .models import UserFollowing

class Follow(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsFollowAnotherUser]

    def create(self, request, *args, **kwargs):
        user_to = get_object_or_404(User.objects, username=self.kwargs["username"])
        self.check_object_permissions(self.request, user_to)
        UserFollowing.objects.create(user_from=self.request.user, user_to=user_to)
        return Response({}, status=status.HTTP_201_CREATED)

class UnFollow(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsFollowingAnotherUser]

    def destroy(self, request, *args, **kwargs):
        user_to = get_object_or_404(User.objects, username=self.kwargs["username"])
        user_follow = get_object_or_404(UserFollowing, user_from=self.request.user, user_to=user_to)
        self.check_object_permissions(self.request, user_follow)
        user_follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

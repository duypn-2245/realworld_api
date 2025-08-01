from rest_framework import permissions, generics
from rest_framework import status
from rest_framework.response import Response
from .models import User
from .serializers import UserInfoSerializer, RegisterSerilizer, ProfileSerializer
class Register(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerilizer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data.get("user", {}))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"user": UserInfoSerializer(serializer.data).data}, 
                        status=status.HTTP_201_CREATED)

class UserInfor(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserInfoSerializer

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response({"user": serializer.data})
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        serializer = self.get_serializer(self.get_object(), data=request.data.get("user", {}), partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"user": serializer.data})

class Profile(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_user_following(self):
        user = self.request.user
        if user.id is not None:
            return user.following_relations.all()
        return []

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        user = self.get_object()
        serializer = self.get_serializer(user, context={"user_following": self.get_user_following()})
        return Response({"user": serializer.data})

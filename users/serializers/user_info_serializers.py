from rest_framework import serializers
from users.models import User

class UserInfoSerializer(serializers.ModelSerializer):
  following = serializers.CharField(source="get_following_display")
  class Meta:
    model = User
    fields = ["email", "bio", "image", "username", "following"]

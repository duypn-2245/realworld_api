from rest_framework import serializers
from users.models import User

class ProfileSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ["email", "bio", "image", "username", "following"]
    
    def get_following(self, obj):
        user_followings = self.context.get("user_following", [])
        return obj.pk in ( user_following.user_to_id for user_following in user_followings)

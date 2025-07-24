from rest_framework import serializers
from users.models import User

class ProfileSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ["email", "bio", "image", "username", "following"]
    
    def get_following(self, obj):
        return obj.pk in self.context.get("following", [])

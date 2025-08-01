from rest_framework import serializers
from comments.models import Comment
from users.serializers.profile_serializer import ProfileSerializer

class CommentSerializer(serializers.ModelSerializer):
	createdAt = serializers.SerializerMethodField()
	updatedAt = serializers.SerializerMethodField()
	author = ProfileSerializer(read_only=True)

	class Meta:
		model = Comment
		fields = ['id', 'body', 'createdAt', 'updatedAt', 'author']
		read_only_fields = ['id', 'createdAt', 'updatedAt']


	def get_createdAt(self, obj):
		return obj.created_at
	
	def get_updatedAt(self, obj):
		return obj.updated_at

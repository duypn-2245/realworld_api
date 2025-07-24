from rest_framework import serializers
from articles.models import Article
from users.serializers.profile_serializer import ProfileSerializer

class ArticleSerializer(serializers.ModelSerializer):
	author = ProfileSerializer(read_only=True)
	class Meta:
		model = Article
		fields = ["id", "slug", "title", "description", "body", "author", "tag_list"]
		read_only_fields = ["slug"]
	
	def to_internal_value(self, data):
		"""
        Convert incoming 'tagList' to 'tag_list'.
        """

		if "tagList" in data:
			data["tag_list"] = data.pop("tagList")
		return super().to_internal_value(data)

	def to_representation(self, instance):
		representation = super().to_representation(instance)
		representation["createdAt"] = instance.created_at
		representation["updatedAt"] = instance.updated_at
		representation["tagList"] = instance.tag_list
		return representation

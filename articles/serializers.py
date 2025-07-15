from rest_framework import serializers
from articles.models import Article

class ArticleSerializer(serializers.ModelSerializer):
	createdAt = serializers.SerializerMethodField()
	updatedAt = serializers.SerializerMethodField()
	tagList = serializers.SerializerMethodField()

	class Meta:
		model = Article
		fields = ['id', 'slug', 'title', 'description', 'body', 'createdAt', 'updatedAt', 'tagList']
		read_only_fields = ['slug']

	def get_createdAt(self, obj):
		return obj.created_at
	
	def get_updatedAt(self, obj):
		return obj.updated_at

	def get_tagList(self, obj):
		return obj.tag_list

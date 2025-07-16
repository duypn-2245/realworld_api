from rest_framework import serializers
from rest_framework.filters import SearchFilter
from articles.models import Article
from users.serializers.user_info_serializers import UserInfoSerializer

class ArticleSerializer(serializers.ModelSerializer):
	createdAt = serializers.SerializerMethodField()
	updatedAt = serializers.SerializerMethodField()
	tagList = serializers.SerializerMethodField()
	author = UserInfoSerializer(read_only=True)

	filter_backends = [SearchFilter]
	search_fields = ['author']
	class Meta:
		model = Article
		fields = ['id', 'slug', 'title', 'description', 'body', 'createdAt', 'updatedAt', 'tagList', 'author']
		read_only_fields = ['slug']

	def get_createdAt(self, obj):
		return obj.created_at
	
	def get_updatedAt(self, obj):
		return obj.updated_at

	def get_tagList(self, obj):
		return obj.tag_list

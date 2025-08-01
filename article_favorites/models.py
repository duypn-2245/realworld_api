from django.db import models
from users.models import User
from articles.models import Article

class ArticleFavorite(models.Model):
	user = models.ForeignKey(User, related_name='article_favorites', on_delete=models.CASCADE, null=True, blank=True)
	article = models.ForeignKey(Article, related_name='article_favorites', on_delete=models.CASCADE, null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['created_at']

	def __str__(self):
		return self.__class__.__name__

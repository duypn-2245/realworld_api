from django.db import models
from users.models import User
from articles.models import Article

class Comment(models.Model):
	body = models.TextField(blank=False, null=False)
	author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE, null=True, blank=True)
	article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE, null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['created_at']

	def __str__(self):
		return self.__class__.__name__

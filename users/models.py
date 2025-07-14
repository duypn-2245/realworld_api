from django.db import models

class User(models.Model):
	email = models.EmailField(max_length=256, unique=True)
	username = models.CharField(max_length=256, unique=True)
	image = models.URLField(blank=True, null=True)
	bio = models.TextField(blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['created_at']

	def __str__(self):
		return self.__class__.__name__

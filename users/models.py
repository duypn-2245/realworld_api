from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.db import models
class User(AbstractBaseUser):
	email = models.EmailField(max_length=256, unique=True)
	username = models.CharField(max_length=256, unique=True)
	password = models.TextField()
	image = models.URLField(blank=True, null=True)
	bio = models.TextField(blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = UserManager()
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []
	class Meta:
		ordering = ['created_at']

	def __str__(self):
		return self.__class__.__name__

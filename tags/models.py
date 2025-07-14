from django.db import models

class Tag(models.Model):
	name = models.CharField(max_length=256)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['created_at']

	def __str__(self):
		return self.__class__.__name__


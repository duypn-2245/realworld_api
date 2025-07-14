from django.db import models
from django.utils.text import slugify

class Article(models.Model):
	title = models.CharField(max_length=128)
	slug = models.SlugField(max_length=256, unique=True, blank=True)
	description = models.TextField(blank=True, null=True)
	body = models.TextField(blank=True, null=True)
	tag_list = models.JSONField(default=list)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['created_at']

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.title)
		super().save(*args, **kwargs)

	def __str__(self):
		return self.__class__.__name__

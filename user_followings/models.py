from django.db import models
from django.conf import settings

class UserFollowing(models.Model):
    user_from = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="following_relations", on_delete=models.CASCADE)
    user_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="follower_relations", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_from', 'user_to'], name='unique_followers')
        ]
        ordering = ['-created_at']

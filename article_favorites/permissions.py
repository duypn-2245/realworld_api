from rest_framework import permissions

class IsCorrectFavoriteArticle(permissions.BasePermission):
    """
    Custom permission to only allow user unfollow user who have followed before
    """
     
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user

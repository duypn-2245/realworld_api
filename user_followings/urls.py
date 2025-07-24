from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from user_followings import views

urlpatterns = [
    path("api/profiles/<str:username>/follow/", views.Follow.as_view()),
    path("api/profiles/<str:username>/unfollow/", views.UnFollow.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

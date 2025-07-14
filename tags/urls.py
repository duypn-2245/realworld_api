from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from tags import views

urlpatterns = [
    path('tags/', views.TagList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

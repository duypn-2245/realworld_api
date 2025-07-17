from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from comments import views

urlpatterns = [
    path('articles/<slug:slug>/comments/', views.ListComment.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

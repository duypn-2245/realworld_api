from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from articles import views

urlpatterns = [
    path("api/articles/", views.ArticleList.as_view()),
    path("api/articles/<slug:slug>/", views.ArticleDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

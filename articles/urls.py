from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from articles import views

urlpatterns = [
    path("api/articles/", views.ArticleList.as_view(), name="articles-create-list"),
    path("api/articles/<slug:slug>/", views.ArticleDetail.as_view(), name="article-retrieve-update"),
]

urlpatterns = format_suffix_patterns(urlpatterns)

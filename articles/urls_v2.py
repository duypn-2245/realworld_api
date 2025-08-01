from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from articles import views

app_name = "articles"

urlpatterns = [
    path("articles/", views.ArticleList.as_view(), name="articles-create-list"),
    path("articles/<slug:slug>/", views.ArticleDetail.as_view(), name="article-retrieve-update"),
]

urlpatterns = format_suffix_patterns(urlpatterns)

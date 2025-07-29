from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from article_favorites import views

urlpatterns = [
    path("articles/<slug:slug>/favorite/", views.Favorite.as_view()),
    path("articles/<slug:slug>/unfavorite/", views.UnFavorite.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

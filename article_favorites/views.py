from rest_framework import permissions, status, generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from users.models import User
from .permissions import IsCorrectFavoriteArticle
from .models import ArticleFavorite
from articles.models import Article
from articles.serializers import ArticleSerializer

class Favorite(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ArticleSerializer

    def get_article_favorites(self):
        user = self.request.user
        if user.id is not None:
            return user.article_favorites.all()
        return []

    def create(self, request, *args, **kwargs):
        article = get_object_or_404(Article.objects, slug=self.kwargs["slug"])
        article_favorite = ArticleFavorite.objects.filter(user=self.request.user, article=article).first()
        if article_favorite is None:
            ArticleFavorite.objects.create(user=self.request.user, article=article)
        
        serializer = self.get_serializer(article, context={"article_favorites": self.get_article_favorites()})
        return Response({"article": serializer.data}, status=status.HTTP_200_OK)

class UnFavorite(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsCorrectFavoriteArticle]
    serializer_class = ArticleSerializer

    def get_article_favorites(self):
        user = self.request.user
        if user.id is not None:
            return user.article_favorites.all()
        return []

    def destroy(self, request, *args, **kwargs):
        article = get_object_or_404(Article.objects, slug=self.kwargs["slug"])
        article_favorite = ArticleFavorite.objects.filter(user=self.request.user, article=article).first()
        if article_favorite is not None:
            self.check_object_permissions(self.request, article_favorite)
            article_favorite.delete()
        
        serializer = self.get_serializer(article, context={"article_favorites": self.get_article_favorites()})
        return Response({"article": serializer.data}, status=status.HTTP_200_OK)

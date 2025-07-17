from rest_framework import status
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from articles.models import Article
from comments.models import Comment
from users.models import User
from comments.serializers import CommentSerializer

class ListComment(APIView):
    """
    Create or retrive comment of a article.
    """
    def get_article(self, slug, format=None):
        try:
            return Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            raise Http404("Article not found")
    
    def get_author(self, pk, format=None):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404("Author not found")
        
    def get(self, request, slug, format=None):
        article = self.get_article(slug)
        comments = Comment.objects.filter(article_id=article.id)
        serializer = CommentSerializer(comments, many=True)
        return Response({'comments': serializer.data})
    
    def post(self, request, slug, format=None):
        article = self.get_article(slug)
        author = self.get_author(request.data.get("author_id"))
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(article=article, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

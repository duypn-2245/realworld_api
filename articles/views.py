from rest_framework import status
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from articles.models import Article
from articles.serializers import ArticleSerializer

class ArticleList(APIView):
    """
    List all articles, or create a new article.
    """
    def get(self, request, format=None):
        articles = Article.objects.select_related('author').all()
        serializer = ArticleSerializer(articles, many=True)
        return Response({'articles': serializer.data, 
                         'articlesCount': Article.objects.count()})
    
    def post(self, request, format=None):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ArticleDetail(APIView):
    """
    Retrieve, update or delete article.
    """
    def get_article(self, slug, format=None):
        try:
            return Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            raise Http404
    
    def get(self, request, slug):
        article = self.get_article(slug)
        serializer = ArticleSerializer(article)
        return Response({'article': serializer.data})
    
    def put(self, request, slug, format=None):
        article = self.get_article(slug)
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

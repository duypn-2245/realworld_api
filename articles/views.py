from rest_framework import permissions, status, generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .models import Article
from .serializers import ArticleSerializer
from .filters import ArticleFilter
from .permissions import IsOwnerOrReadOnly
from .pagination import ArticlePagination

class ArticleList(generics.ListCreateAPIView):
    queryset = Article.objects.prefetch_related("author")
    serializer_class = ArticleSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ArticleFilter
    pagination_class = ArticlePagination
    ordering_fields = ["created_at"]

    def get_following(self):
        user = self.request.user
        if user.id is not None:
            return user.following.all()
        return []


    def list(self, request, *args, **kwargs):
        self.permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        self.check_permissions(request)
        filtered_queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(filtered_queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={"following": self.get_following()})
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(filtered_queryset, many=True, 
                                         context={"following": self.get_following()})
        return Response({
            "articles": serializer.data,
            "articlesCount": filtered_queryset.count()
        })
   
    def create(self, request, *args, **kwargs):
        self.permission_classes = [permissions.IsAuthenticated]
        self.check_permissions(request)
        serializer = self.get_serializer(data=request.data.get("article", {}), 
                                         context={"following": self.get_following()})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"article": serializer.data}, status=status.HTTP_201_CREATED)
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class ArticleDetail(generics.RetrieveUpdateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get_following(self):
        user = self.request.user
        if user.id is not None:
            return user.following.all()
        return []
    
    def get_object(self):
        queryset = self.get_queryset()
        article = get_object_or_404(queryset, slug=self.kwargs["slug"])
        self.check_object_permissions(self.request, article)
        return article

    def retrieve(self, request, *args, **kwargs):
        self.permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        self.check_permissions(request)
        serializer = self.get_serializer(self.get_object(), context={"following": self.get_following()})
        return Response({"article": serializer.data})
    
    def update(self, request, *args, **kwargs):
        self.permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
        self.check_permissions(request)
        partial = kwargs.pop("partial", False)
        serializer = self.get_serializer(self.get_object(), data=request.data.get("article", {}), 
                                        partial=partial, context={"following": self.get_following()})
        
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"article": serializer.data})

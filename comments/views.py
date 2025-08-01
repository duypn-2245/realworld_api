from rest_framework import permissions, status, generics
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from articles.models import Article
from .models import Comment
from .serializers import CommentSerializer
from .permissions import IsOwnerOrReadOnly

class ListComment(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_user_following(self):
        user = self.request.user
        if user.id is not None:
            return user.following_relations.all()
        return []

    def get_queryset(self):
        article = get_object_or_404(Article.objects, slug=self.kwargs["slug"])
        return article.comments.select_related("author").all()

    def list(self, request, *args, **kwargs):
        self.permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        self.check_permissions(request)
        serializer = self.get_serializer(self.get_queryset(), many=True,  
                                         context={"user_following": self.get_user_following()})
        
        return Response({"comments": serializer.data})
    
    def create(self, request, *args, **kwargs):
        self.permission_classes = [permissions.IsAuthenticated]
        self.check_permissions(request)
        serializer = self.get_serializer(data=request.data.get("comment", {}),
                                         context={"user_following": self.get_user_following()})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"comment": serializer.data}, status=status.HTTP_201_CREATED)
    
    def perform_create(self, serializer):
        article = get_object_or_404(Article.objects, slug=self.kwargs["slug"])
        serializer.save(author=self.request.user, article=article)

class UpdateDestroyComment(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.select_related("author")
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_user_following(self):
        user = self.request.user
        if user.id is not None:
            return user.following_relations.all()
        return []
    
    def get_queryset(self):
        article = get_object_or_404(Article.objects, slug=self.kwargs["slug"])
        return article.comments.all()
    
    def get_object(self):
        comment = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, comment)
        return comment
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        serializer = self.get_serializer(self.get_object(), data=request.data.get("comment", {}), 
                                         partial=partial, 
                                         context={"user_following": self.get_user_following()})
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"comment": serializer.data})

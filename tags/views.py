from rest_framework import status, generics
from rest_framework.response import Response
from django.core.cache import cache
from .models import Tag
from .serializers import TagSerializer


class TagList(generics.ListAPIView):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()

    def list(self, request, *args, **kwargs):
        cache_key = "tags_list"
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)
        
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = {"tag": serializer.data}
        cache.set(cache_key, data)
        return Response(data, status=status.HTTP_200_OK)

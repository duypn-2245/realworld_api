from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from tags.models import Tag
from tags.serializers import TagSerializer

class TagList(APIView):
    """
    List all tags
    """
    def get(self, request, format=None):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)

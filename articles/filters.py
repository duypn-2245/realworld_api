import django_filters
from articles.models import Article

class ArticleFilter(django_filters.FilterSet):
    # Use "icontains" for case-insensitive partial match (like SearchFilter)
    author = django_filters.CharFilter(field_name="author__username", lookup_expr="exact")
    tag = django_filters.CharFilter(field_name="tag_list", lookup_expr="icontains")

    class Meta:
        model = Article
        # Define the fields you want to filter on
        fields = ["author", "tag"]

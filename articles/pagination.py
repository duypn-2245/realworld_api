from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class ArticlePagination(PageNumberPagination):
    # Set the default number of items per page
    page_size = 20
    
    # Allow the client to override the page size via a query parameter (e.g., ?page_size=100)
    page_size_query_param = "page_size"
    
    # Set a maximum limit on the page size that clients can request
    max_page_size = 1000
    
    # Change the query parameter for the page number (e.g., ?p=2)
    page_query_param = "page"

    def get_paginated_response(self, data):
        next_page = None
        previous_page = None

        if self.page.has_next():
            next_page = self.page.next_page_number()

        if self.page.has_previous():
            previous_page = self.page.previous_page_number()
            
        return Response({
            "articlesCount": self.page.paginator.count,
            "currentPage": self.page.number,
            "nextPageNumber": next_page,
            "previousPageNumber": previous_page,
            "articles": data
        })

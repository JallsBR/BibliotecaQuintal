"""
Paginação que aceita page_size na query string.
Ex.: ?page=1&page_size=25
"""
from rest_framework.pagination import PageNumberPagination


class PageSizePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

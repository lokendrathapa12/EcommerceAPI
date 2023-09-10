from rest_framework.pagination import PageNumberPagination

class Mypagenumberpagination(PageNumberPagination):
    page_size = 3
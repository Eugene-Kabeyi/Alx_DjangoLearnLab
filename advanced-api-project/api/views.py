from django_filters import rest_framework
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView
)
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


# ===============================
# ViewSets (Unchanged)
# ===============================

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# ===============================
# DRF GENERIC VIEW WITH FILTERING
# ===============================

class BookListView(ListAPIView):
    """
    List all books and allow:
    - Filtering (by title, author, publication_year)
    - Searching (text search on title or author fields)
    - Ordering (sort results by title or publication year)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Enable filtering, search, ordering
    filter_backends = [
        DjangoFilterBackend,     # For filtering
        filters.SearchFilter,    # For search
        filters.OrderingFilter   # For ordering
    ]

    # -------- FILTERING FIELDS --------
    # Users can filter like:
    # /books/?title=Harry
    # /books/?publication_year=2020
    filterset_fields = ['title', 'author', 'publication_year']

    # -------- SEARCH FIELDS --------
    # Users can search like:
    # /books/?search=harry
    search_fields = ['title', 'author__name']

    # -------- ORDERING FIELDS --------
    # Users can order like:
    # /books/?ordering=title
    # /books/?ordering=-publication_year
    ordering_fields = ['title', 'publication_year']


# ===============================
# Detail View (unchanged)
# ===============================
class BookDetailView(RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# ===============================
# Create / Update / Delete Views
# ===============================
class BookCreateView(CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookUpdateView(UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookDeleteView(DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

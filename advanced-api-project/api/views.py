from django.shortcuts import render
from rest_framework import viewsets

from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


# Author ViewSet
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

# Book ViewSet
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
 
# Generic Class-Based Views for Book Model   
class BookListView(ListView):
    model = Book

# Detail View for a single Book
class BookDetailView(DetailView):
    model = Book

# Create View for a new Book
class BookCreateView(CreateView):
    model = Book
    fields = "__all__"

# Update View for an existing Book
class BookUpdateView(UpdateView):
    model = Book
    fields = "__all__"

# Delete View for a Book
class BookDeleteView(DeleteView):
    model = Book
    success_url = "/books/"
from django.http import HttpResponse
from django.shortcuts import render
from .models import Book

# Create your views here.
def book_list(request):
    """View to display a list of books."""
    books = Book.objects.all()
    context = {'book_list':books}

    return render(request, 'bookshelf/book_list.html', context), HttpResponse("Hello, this is the book list view.")
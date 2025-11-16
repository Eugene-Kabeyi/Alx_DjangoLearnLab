from django.urls import path
from . import views  # imports both function-based and class-based views

urlpatterns = [
    # Function-based view to list all books
    path('books/', views.list_books, name='list_books'),
    
    # Class-based view to show library details
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
]

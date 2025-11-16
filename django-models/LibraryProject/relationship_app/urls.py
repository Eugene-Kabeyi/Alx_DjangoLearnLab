from django.urls import path
from .views import (
    list_books,
    LibraryDetailView,
    register_view,
    login_view,
    logout_view,
)
 # imports both FBV + CBV

urlpatterns = [
    # Function-based view to list all books
    path('books/', list_books, name='list_books'),
    
    # Class-based view to show library details
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", register_view, name="register"),
]

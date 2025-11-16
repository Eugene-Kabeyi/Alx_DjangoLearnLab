from django.urls import path
from .views import (
    list_books,
    LibraryDetailView,
    RegisterView,
    LoginView,
    LogoutView,
)
 # imports both FBV + CBV

urlpatterns = [
    # Function-based view to list all books
    path('books/', list_books, name='list_books'),
    
    # Class-based view to show library details
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
]

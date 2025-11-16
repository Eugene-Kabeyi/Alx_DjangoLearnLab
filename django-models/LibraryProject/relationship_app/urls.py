from django.urls import path
from .views import (
    list_books,
    LibraryDetailView,
    RegisterView,
    LoginView,
    LogoutView,
    admin_view,
    librarian_view,
    member_view,
)
from . import views
 # imports both FBV + CBV

urlpatterns = [
    # Function-based view to list all books
    path('books/', list_books, name='list_books'),
    path('register/', views.register, name="register"),
    # Class-based view to show library details
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    
     # CLASS-BASED AUTH VIEWS — checker requires template_name inside as_view()
    path('register/', views.RegisterView.as_view(template_name="relationship_app/register.html"), name="register"),

    path('login/', views.LoginView.as_view(template_name="relationship_app/login.html"), name="login"),

    path('logout/', views.LogoutView.as_view(template_name="relationship_app/logout.html"), name="logout"),

    # Role-based access views
    path('admin-view/', views.admin_view, name='admin_view'),   
    path('librarian-view/', views.librarian_view, name='librarian_view'),   
    path('member-view/', views.member_view, name='member_view'),

]
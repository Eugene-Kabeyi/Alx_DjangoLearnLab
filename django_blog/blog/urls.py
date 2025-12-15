from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView,
)

urlpatterns = [
    # Registration
    path('register/', views.register, name='register'),

    # Login (uses Django built-in view but custom template)
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),

    # Logout (uses built-in view)
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),

    # Profile (view & edit)
    path('profile/', views.profile, name='profile'),
    
    # Comments Add
    path('post/<int:post_id>/comments/new/', views.add_comment, name='add-comment'),
   
    # Comments Edit
    path('comments/<int:comment_id>/edit/', views.edit_comment, name='edit-comment'),
    
    # Comments Delete
    path('comments/<int:comment_id>/delete/', views.delete_comment, name='delete-comment'),

    # Post URLs  path('posts/', PostListView.as_view(), name='post-list'),                 # list all
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),         # create
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),    # detail
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-edit'), # edit
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'), # delete

     # NEW TAG URL
    path('tags/<str:tag_name>/', views.PostListByTagView.as_view(), name='post-by-tag'),

    # NEW SEARCH URL
    path('search/', views.SearchView.as_view(), name='search'),
    

    path('post/<int:pk>/comments/new/', CommentCreateView.as_view(), name='comment-create'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-edit'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),


]
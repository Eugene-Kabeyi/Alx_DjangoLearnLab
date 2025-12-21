from django.urls import path
from .views import (
    FeedView,
    PostListCreateView,
    PostDetailView,
    CommentListCreateView,
    CommentDetailView
)

urlpatterns = [
    # Posts
    path('post/', PostListCreateView.as_view(), name='post-list-create'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),

    # Comments
    path('comment/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('comment/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    
    # Feed
    path('feed/', FeedView.as_view(), name='feed'),
]

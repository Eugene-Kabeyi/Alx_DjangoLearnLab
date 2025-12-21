from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
urlpatterns = [
    path('', include(router.urls)),
    # url patterns for account management
    path('users/', views.CustomUserViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-list'),
    
    # url patterns for registration and login
    path('register/', views.RegisterViewSet.as_view({'post': 'create'}), name='register'),
    path('login/', views.LoginViewSet.as_view({'post': 'create'}), name='login'),
    
]


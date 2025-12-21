from django.shortcuts import render
from . import models
from . import serializers
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from posts.models import Post
from posts.serializers import PostSerializer
from rest_framework import permissions, status
from django.shortcuts import get_object_or_404

User = get_user_model()
# Create your views here.

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = models.CustomUser.objects.all()
    serializer_class = serializers.CustomUserSerializer

class RegisterViewSet(viewsets.ModelViewSet):
    queryset = models.CustomUser.objects.all()
    serializer_class = serializers.RegisterSerializer
    http_method_names = ['post']


class LoginViewSet(viewsets.ViewSet):
    serializer_class = serializers.LoginSerializer

    def create(self, request):
        
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        try:
            user = models.CustomUser.objects.get(username=username)
            if not user.check_password(password):
                raise Exception("Invalid credentials")
        except models.CustomUser.DoesNotExist:
            raise Exception("Invalid credentials")
        
    
        token, created = Token.objects.get_or_create(user=user)
        token_serializer = serializers.TokenSerializer(token)
        return Response(token_serializer.data)
    
class FollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        user_to_follow = get_object_or_404(User, id=user_id)

        if user_to_follow == request.user:
            return Response(
                {"error": "You cannot follow yourself"},
                status=status.HTTP_400_BAD_REQUEST
            )

        request.user.following.add(user_to_follow)
        return Response(
            {"message": f"You are now following {user_to_follow.username}"},
            status=status.HTTP_200_OK
        )

class UnfollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        user_to_unfollow = get_object_or_404(User, id=user_id)

        request.user.following.remove(user_to_unfollow)
        return Response(
            {"message": f"You unfollowed {user_to_unfollow.username}"},
            status=status.HTTP_200_OK
        )

class FeedView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        following_users = request.user.following.all()

        posts = Post.objects.filter(
            author__in=following_users
        ).order_by('-created_at')

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

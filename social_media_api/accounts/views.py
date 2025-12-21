from django.shortcuts import render
from . import models
from . import serializers
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
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
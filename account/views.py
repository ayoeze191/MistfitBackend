from wsgiref import validate
from django.shortcuts import render
import jwt
from .models import Customer, Jwt, CustomUser
from rest_framework.views import APIView
from rest_framework import generics
import random
import string
from datetime import datetime, timedelta
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework.response import Response
from .serializer import LoginSerializer, UserSerializer, LogOutTokenSerializers, RefreshTokenSerializers, RegisterSerializer
from .import authentication
from account import serializer
from .authentication import Authentication
from rest_framework import permissions
# from .authentication import Authentication
# Create your views here.


def get_random(length):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
def get_access_token(payload):
    return jwt.encode({'exp':datetime.now() + timedelta(hours=5), **payload}, 
    settings.SECRET_KEY, algorithm="HS256")


def get_refresh_token():
    return jwt.encode(
        {"exp": datetime.now() + timedelta(days=365), "data":get_random(10)},
         settings.SECRET_KEY, algorithm="HS256"
    )


class LoginView(APIView):
    serializer_class = LoginSerializer
    def post(self, request):
     
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(username = serializer.validated_data['email'], password = serializer.validated_data['password'])
        if not user:
            return Response({"invalid: username"}, status=400)
        Jwt.objects.filter(user_id=user.id).delete()
        access = get_access_token({"user_id": user.id, "username": user.get_username()})
        print('access', access)
        refresh = get_refresh_token()
        serializedUser = UserSerializer(user)
        Jwt.objects.create(
            user_id = user.id, access=access, refresh=refresh
        )
        return Response({'access': access, 'refresh': refresh, 'user': serializedUser.data})


class LogoutView(APIView):
    serializer_class = LogOutTokenSerializers
    def get(self, request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['access']
        try:
            Jwt.objects.get(access = serializer.validated_data['access'])
        except Jwt.DoesNotExist:
            return Response({"data": "invalid token"})
        else:
            Jwt.objects.get(access=serializer.validated_data["access"]).delete()
            return Response({"logged out successfully"})


class UserApi(generics.RetrieveAPIView):
    authentication_classes = [Authentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    def get_object(self):
        print(self.request.user)
        return self.request.user


class RefreshTokenView(APIView):
    serializer_class = RefreshTokenSerializers
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            active_jwt = Jwt.objects.get(refresh=serializer.validated_data["refresh"])
        except Jwt.DoesNotExist:
            return Response({"error": "refresh does not exist"}, status='404')

        if not authentication.verify_token(serializer.validated_data['refresh']):
            return Response({"error": "Token is invalid or has expired"})
        access = get_access_token({"user_id": active_jwt.user.id})
        refresh = get_refresh_token()
        active_jwt.access = access
        active_jwt.refresh = refresh
        active_jwt.save()
        PersonSerializer = UserSerializer(active_jwt.user)
        return Response({
            'access': access, 'refresh': refresh, 'user': PersonSerializer.data
        })


class RegisterView(APIView):
    serializer_class = RegisterSerializer
    def post(self, request):
        serilizer = self.serializer_class(data=request.data)
        serilizer.is_valid(raise_exception=True)
        if CustomUser.objects.filter(email = serilizer.validated_data['email']).exists():
            return Response({"Email already Exist"})
        CustomUser.objects._create_(email = serilizer.validated_data['email'], password = serilizer.validated_data['password'], name = serilizer.validated_data['name'])
        user = Customer.objects.get(user__email = serilizer.validated_data['email'])
        
        user.last_name = serilizer.validated_data['last_name']
        user.save()
        return Response({"user succesfully created"})

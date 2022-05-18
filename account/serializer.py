import email
from wsgiref import validate
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser

# def must_contain_email(value):
#     lis = []
    
#     for i in value:
#         lis.append(i)
#     if '@' not in lis:
#         raise serializers.ValidationError('Invalid Email') 
#     if '.' not in lis:
#         raise serializers.ValidationError('Invalid Email') 
#     return value 

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
   
    # def validate(self, attrs):
    #     user = authenticate(username = attrs['email'], password = attrs['password'])
    #     if not user:
    #         serializers.ValidationError(
    #                 "Invalid email or password"
    #         )
    #     return user

    
        


    


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    name = serializers.CharField()
    is_staff = serializers.BooleanField()
    is_superuser = serializers.BooleanField()
    
class LogOutTokenSerializers(serializers.Serializer):
    refresh = serializers.CharField()

class RefreshTokenSerializers(serializers.Serializer):
    # access = serializers.CharField()
    refresh = serializers.CharField()


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    password1 = serializers.CharField()
    name = serializers.CharField()
    last_name = serializers.CharField()


    def validate(self, data):
        if data['password'] != data['password1']:
            raise serializers.ValidationError('passwords does not match')
        if CustomUser.objects.filter(email = data['email']).exists():
            raise serializers.ValidationError("Email already Exist")
        return data


        





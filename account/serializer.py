from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


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
    name = serializers.CharField()
    last_name = serializers.CharField()




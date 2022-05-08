import email
from itertools import product
from rest_framework import serializers
from store.serializer import ProductSerializers
from .models import Order, OrderItem, Shipping



class OrderItemSerializer(serializers.Serializer):
    product = ProductSerializers()
    quantity = serializers.IntegerField()

class ShippingInFoSerializer(serializers.Serializer):
    address = serializers.CharField()
    city = serializers.CharField()
    state = serializers.CharField()
    zipcode= serializers.CharField()
        


class VisitingUserSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.EmailField()
    
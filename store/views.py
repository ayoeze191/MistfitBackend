from django.shortcuts import render
from rest_framework import filters
# Create your views here.
from rest_framework.views import APIView    
from rest_framework import generics
from rest_framework.response import Response
from .serializer import ProductSerializers
from.models import Product
from account.authentication import Authentication
from rest_framework.permissions import IsAuthenticated, AllowAny


class ProductsView(generics.ListAPIView): 
    # authentication_classes = [Authentication]
    permission_classes = [AllowAny]
    serializer_class = ProductSerializers
    queryset = Product.objects.all()
    # def get(self, request):
    #     products = Product.objects.all()
    #     serializer = self.serializer_class(products, many = True)
    #     return Response(serializer.data)


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers


class ProductSearchView(generics.ListAPIView):
    authentication_classes = [Authentication]
    serializer_class = ProductSerializers
    queryset = Product.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['^name']




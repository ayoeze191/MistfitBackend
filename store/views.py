from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView    
from rest_framework import generics
from rest_framework.response import Response
from .serializer import ProductSerializers, SearchSerializer
from.models import Product
from account.authentication import Authentication
from rest_framework.permissions import IsAuthenticated


class ProductsView(APIView):
    # authentication_classes = [Authentication]
    # permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializers
    def get(self, request):
        products = Product.objects.all()
        serializer = self.serializer_class(products, many = True)
        return Response(serializer.data)


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers

class ProductSearchView(APIView):

    def post(self, request):
        serializer = SearchSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        
        if serializer.validated_data['based_on'] == 'category':
            products = Product.objects.filter(category__title__contains = serializer.validated_data['text'])
            return Response(ProductSerializers(products, many=True).data)

        if serializer.validated_data['based_on'] == 'name':
            products = Product.objects.filter(name__contains = serializer.validated_data['text'])
            return Response(ProductSerializers(products, many=True).data)

        else:
            return Response({"can only search based on names and categories"})
    

        



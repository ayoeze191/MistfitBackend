# from pyexpat import model

# from unicodedata import category
from dataclasses import field
from pyexpat import model
from rest_framework import serializers
from .models import Product

class CategorySerializers(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()


class ProductSerializers(serializers.ModelSerializer):
    # category = CategorySerializers()
    # name = serializers.CharField()
    # description = serializers.CharField()
    # stock_price = serializers.IntegerField()
    productimage = serializers.StringRelatedField(many=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'description', 'stock_price', 'productimage']
        depth = 1
        
    
class SearchSerializer(serializers.Serializer):
    based_on = serializers.CharField(required = False, allow_blank = True)
    text =  serializers.CharField(required = False, allow_blank = True)
from ast import Delete
import datetime
import email
from unicodedata import name
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from account.authentication import Authentication

from rest_framework.permissions import IsAuthenticated, AllowAny

from account.models import Customer
# from backend.backend.account.models import CustomUser
from .models import Order, OrderItem, Shipping
from account.models import CustomUser
from .serializer import OrderItemSerializer, ShippingInFoSerializer, VisitingUserSerializer
from store.models import Product
# Create your views here.


class AuthenticatedUserCart(APIView):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        
        # order = ''
        # if Order.objects.get(buyer=request.user.customer, complete=False):
        #     order = Order.objects.get(buyer = request.user.customer, complete = False)
        # else:
        #     Order.objects.create(buyer=request.user.customer, complete = False)
        #     order = Order.objects.get(buyer=request.user.customer, complete = False)
        order, created = Order.objects.get_or_create(buyer = request.user.customer, complete = False)
        product = Product.objects.get(id = pk)
        
        orderItem, created = OrderItem.objects.get_or_create(order = order, product = product)
        orderItem.quantity += 1
        orderItem.save()

        total_number_of_products = order.total_number_of_product
        total_amount_of_all_goods_bought = order.total_amount_of_all_goods_bought
        items = order.orderitem_set.all()
        serializer_class = OrderItemSerializer
        serializer = serializer_class(items, many = True)
        return Response({
                'total_amount_of_all_goods_bought':total_amount_of_all_goods_bought,
                 "total_number_of_products" :total_number_of_products,
                 "orders": serializer.data
                })
        
    def delete(self, request, pk):
        # order = ''
        # if Order.objects.get(buyer=request.user.customer, complete=False):
        #    order = Order.objects.get(buyer=request.user.customer)

        # else:
        #        Order.objects.create(buyer=request.user.customer, complete = False)
        #        order = Order.objects.get(buyer=request.user.customer, complete = False)
        order, created = Order.objects.get_or_create(buyer = request.user.customer, complete = False)
        product = Product.objects.get(id = pk)

        product = Product.objects.get(pk = pk)
        orderItem, created = OrderItem.objects.get_or_create(order = order, product = product)
        orderItem.quantity -= 1
        orderItem.save()

        if orderItem.quantity <= 0:
            orderItem.delete()
        total_number_of_products = order.total_number_of_product
        total_amount_of_all_goods_bought = order.total_amount_of_all_goods_bought
        items = order.orderitem_set.all()
        serializer_class = OrderItemSerializer
        serializer = serializer_class(items, many = True)
       
        return Response({
                'total_amount_of_all_goods_bought':total_amount_of_all_goods_bought,
                 "total_number_of_products" :total_number_of_products,
                 "orders": serializer.data
                })
 

class CartComponents(APIView):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
            user = request.user.customer
            order, created = Order.objects.get_or_create(buyer = user, complete=False)
            total_number_of_products = order.total_number_of_product
            total_amount_of_all_goods_bought = order.total_amount_of_all_goods_bought
            items = order.orderitem_set.all()
            serializer_class = OrderItemSerializer
            serializer = serializer_class(items, many = True)
            return Response({
                'total_amount_of_all_goods_bought':total_amount_of_all_goods_bought,
                 "total_number_of_products" :total_number_of_products,
                 "orders": serializer.data
                 })

class ProcessOrder(APIView):
    authentication_classes = [Authentication]
    permission_classes = [AllowAny]
    transaction_id = datetime.datetime.now().timestamp()
    shipping_serializer = ShippingInFoSerializer
    def post(self, request):
        if request.user is not None:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(buyer = customer, complete = False)
            total = request.data['shipping_data']['total']
            order.transaction_id = self.transaction_id
            shipping_info_serializer = self.shipping_serializer(data = request.data['shipping_data']['shipping_info'])
            shipping_info_serializer.is_valid(raise_exception=True)
            if total == order.total_amount_of_all_goods_bought:
                order.complete = True
                order.save()
            order.save()
            Shipping.objects.create(**shipping_info_serializer.validated_data, order = order, customer = customer)
            return Response( {"order succesfully processed"})
        
        else:
            seriliazer = VisitingUserSerializer(data = request.data['shipping_data']['user_info'])
            seriliazer.is_valid(raise_exception=True)
            shipping_info_serializer = self.shipping_serializer(data = request.data['shipping_data']['shipping_info'])
            shipping_info_serializer.is_valid(raise_exception=True)
            user, created = CustomUser.objects.get_or_create(email = seriliazer.validated_data['email'], name = seriliazer.validated_data['name'])
            customer = Customer.objects.get(user = user)
            user_cart = request.data['order']
            
            d, created = Order.objects.get_or_create(buyer = customer, complete = False)
            order = Order.objects.get(buyer = customer, complete = False)
            print(user_cart)
            for i in user_cart:
                product = Product.objects.get(id = i["product"]["id"])
                order_item, created = OrderItem.objects.get_or_create(order = order, product = product, quantity = i['quantity'])
                order_item.save()

            shipping_info_serializer = self.shipping_serializer(data = request.data['shipping_data']['shipping_info'])
            shipping_info_serializer.is_valid(raise_exception=True)
            Shipping.objects.create(**shipping_info_serializer.validated_data, order = order, customer = customer)
            order.complete = True
            order.save()

            return Response({"order successfully processed"})

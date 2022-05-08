from itertools import product
from django.db import models
from store.models import Product
from account.models import Customer
from .Order import OrderClass
# Create your models here.

class Order(models.Model):
    buyer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    complete = models.BooleanField(default=False)
    date_ordered = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=200, null=True, blank=True)
    @property
    def total_number_of_product(self):
         return OrderClass.total_number_of_product(self)

    @property
    def total_amount_of_all_goods_bought(self):
         return OrderClass.total_amount_of_all_goods_bought(self)


class OrderItem(models.Model):
     product = models.ForeignKey(Product, on_delete=models.CASCADE)
     order = models.ForeignKey(Order, on_delete=models.CASCADE)
     quantity = models.IntegerField(default=0, null=True, blank=True)
     date_added = models.DateTimeField(auto_now_add=True)
     

     @property
     def get_total_amount_of_a_particular_goods_bought(self):
        return OrderClass.get_total_amount_of_a_particular_goods_bought(self)



class Shipping(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank = True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length = 200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length = 200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)





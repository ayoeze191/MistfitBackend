from django.contrib import admin

# Register your models here.
from .models import Order, OrderItem, Shipping

admin.site.register((Order, OrderItem, Shipping))


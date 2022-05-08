from django.contrib import admin

# Register your models here.
from .models import Category, Product, Image

admin.site.register((Category, Product, Image))



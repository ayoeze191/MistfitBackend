from django.contrib import admin

# Register your models here.

from .models import Customer, CustomUser

admin.site.register((Customer, CustomUser))


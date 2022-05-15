from django.contrib import admin

# Register your models here.

from .models import Customer, CustomUser, BlackListedToken

admin.site.register((Customer, CustomUser))


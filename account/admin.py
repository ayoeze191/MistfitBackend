from django.contrib import admin

# Register your models here.

from .models import Customer, CustomUser, BlackListedToken, Jwt

admin.site.register((Customer, CustomUser, BlackListedToken, Jwt))


from django.contrib import admin
from .models import Product, Order, CustomUser
# Register your models here.
@admin.register(CustomUser)
class CustomUserAdminModel(admin.ModelAdmin):
    list_display = ['id','username', 'password', 'user_type']

@admin.register(Product)
class ProductAdminModel(admin.ModelAdmin):
    list_display = ['id','name','description','quantity','price','seller']


@admin.register(Order)
class OrderAdminModel(admin.ModelAdmin):
    list_display = ['id','buyer','product','status']
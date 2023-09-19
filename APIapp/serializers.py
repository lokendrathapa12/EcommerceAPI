from rest_framework import serializers
from .models import Product,Order,CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'user_type')
        extra_kwargs = {'password': {'write_only': True}}
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name','description','price','seller']
        


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['buyer','product','order_quantity','status']


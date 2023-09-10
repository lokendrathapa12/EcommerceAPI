from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('Buyer', 'Buyer'),
        ('Seller', 'Seller'),
        ('Admin','Admin'),
    )

    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)

    
class Product(models.Model):
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=500)
    quantity = models.IntegerField()
    price = models.BigIntegerField()
    seller = models.ForeignKey(CustomUser,on_delete=models.CASCADE)

class Order(models.Model):
    STATUS_CHOICES = (
        ('Accepted','Accepted'),
        ('Rejectes','Rejected'),
    )
    buyer = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    order_quantity = models.IntegerField()
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,default='Accepted')
    
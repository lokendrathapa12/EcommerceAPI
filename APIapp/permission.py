from rest_framework.permissions import BasePermission
from rest_framework import permissions
from django.core.exceptions import ObjectDoesNotExist
from .models import CustomUser


class IsSeller(BasePermission):
    """
    Allows access to Seller.
    """

    message = "You must have a Seller User_type."

    def has_permission(self, request, view):
        authenticated = bool(request.user and request.user.is_authenticated)
        if not authenticated:
            return authenticated
        else:
            try:
                cuser = CustomUser.objects.get(pk=request.user.pk)
            except CustomUser.DoesNotExist:
                raise ObjectDoesNotExist("Unauthenticated User")
            if cuser.user_type == "Seller":
                return True
            return False
                


class IsBuyer(permissions.BasePermission):
    def has_permission(self, request, view):
        authenticated = bool(request.user and request.user.is_authenticated)
        if not authenticated:
            return authenticated
        else:
            try:
                cuser = CustomUser.objects.get(pk=request.user.pk)
            except CustomUser.DoesNotExist:
                raise ObjectDoesNotExist("Unauthenticated User")
            if cuser.user_type == "Buyer":
                return True
            return False
        

class IsSellerUniqueuser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        authenticated = bool(request.user and request.user.is_authenticated)
        if not authenticated:
            return authenticated
        else:
            try:
                cuser = CustomUser.objects.get(pk=request.user.pk)
            except CustomUser.DoesNotExist:
                raise ObjectDoesNotExist("Unauthenticated User")
            if cuser.user_type == "Seller" and obj.seller == request.user:
                return True
            return False
        # Check if the request user (Seller) is the owner of the Product associated with the Order.
        #return request.user.is_authenticated and request.user.is_seller and obj.product.seller == request.user

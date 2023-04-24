from rest_framework import permissions

from shop.models import Order, Cart, Purchaser

# class IsAdminOrReadOnly(permissions.BasePermission):
#     def has_permission(self, request, view):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         return bool(request.user and request.user.is_staff)


# class IsAdminOrReadOnlyForAuth(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         if (request.method in permissions.SAFE_METHODS) and obj.purchaser == request.user:
#             return True
#         return bool(request.user and request.user.is_staff)
from shop.service import get_client_ip


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or bool(request.user.is_staff)


class IsOwnerOrder(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = Order.objects.get(order=obj.order).user
        return user == request.user or bool(request.user.is_staff)


class IsOwnerCart(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            user = Cart.objects.get(pk=request.data['cart']).user
            if user == request.user:
                return True
        except:
            pass
        return bool(request.user and request.user.is_staff)


class IsOwnerCartIP(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            ip = Cart.objects.get(pk=request.data['cart']).ip
            if ip == get_client_ip(request) and not request.user:
                return True
        except:
            pass
        return bool(request.user and request.user.is_staff)


class IsPurchaser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        purchaser = Purchaser.objects.get(pk=obj.id).user
        return purchaser == request.user

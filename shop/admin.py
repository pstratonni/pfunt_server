from django.contrib import admin

from .models import Manufacturer, Product, Order, Purchaser, OrderItem, Composition, Cart, CartItem, Delivery

admin.site.register(Manufacturer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Purchaser)
admin.site.register(Composition)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Delivery)





from django.contrib import admin

from .models import *

admin.site.register(Manufacturer)
# admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Purchaser)
admin.site.register(Composition)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Delivery)
admin.site.register(Thumbnail)
admin.site.register(Category)
admin.site.register(FAQ)
admin.site.register(Tax)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'discount', 'active', 'date_created',)
    list_per_page = 16
    search_fields = ('title',)
    list_filter = ('active',)
    date_hierarchy = 'date_created'

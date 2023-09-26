import calendar
import datetime

import dateutils
from django.contrib import admin
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe

from .models import *

admin.site.register(Manufacturer)
# admin.site.register(Product)
# admin.site.register(Order)
# admin.site.register(OrderItem)
admin.site.register(Purchaser)
admin.site.register(Composition)
# admin.site.register(Cart)
# admin.site.register(CartItem)
admin.site.register(Delivery)
admin.site.register(Thumbnail)
admin.site.register(Category)
admin.site.register(FAQ)
admin.site.register(Tax)


class DateCommentFilter(admin.SimpleListFilter):
    title = 'Bestellungsdate'
    parameter_name = 'date_created'

    def lookups(self, request, model_admin):
        filter = []
        orders = Order.objects.order_by('date_created')
        dates = {}
        for order in orders:
            if order.date_created.strftime('%B %Y') in dates.keys():
                continue
            _, last_day = calendar.monthrange(order.date_created.year, order.date_created.month)
            date_value = order.date_created.strftime(f"%Y,%m,{last_day},23,59,59")
            dates[order.date_created.strftime('%B %Y')] = ''
            filter.append((date_value, order.date_created.strftime('%B %Y')))
        return filter

    def queryset(self, request, queryset):
        if not self.value():
            return queryset

        value = tuple(map(int, self.value().split(',')))
        value = datetime.datetime(*value)
        return queryset.filter(
            date_created__gte=(value - dateutils.relativedelta(months=1) + datetime.timedelta(seconds=1)),
            date_created__lte=value)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('colored_title', 'price', 'discount', 'active', 'date_created',)
    list_per_page = 16
    search_fields = ('title',)
    list_filter = ('active',)
    date_hierarchy = 'date_created'
    list_display_links = ('colored_title', 'discount')
    list_editable = ('active',)
    raw_id_fields = ('thumbnail', 'composition')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'id', 'total_amount', 'total_price')
    search_fields = ('user',)
    date_hierarchy = 'date_created'
    readonly_fields = ('cart_items',)

    def cart_items(self, instance):
        items = instance.cart_items.all()
        render = '<tr><td>Title of product</td><td>Quantity</td><tr>'
        for line in items:
            render += f'<tr><td>{line.product}</td><td style="text-align:center">{line.quantity}</td><td>{line.id}</td></tr>'
        render_html = "<table>" + render + "</table>"

        return format_html(
            render_html
        )

    cart_items.short_description = 'Products in cart'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'discount', 'total_price')
    search_fields = ('cart',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'id', 'total_price', 'delivery_cost', 'date_created', 'date_shipping', 'status',
        'payment_type', 'payment_status', 'full_address')
    search_fields = ('user',)
    list_per_page = 12
    date_hierarchy = 'date_created'
    list_editable = ('status', 'date_shipping')
    list_filter = ('status', 'date_shipping', DateCommentFilter)
    readonly_fields = ('address', 'order_items',)
    fields = (('user', 'ip'), 'email', ('products_price', 'delivery_cost', 'total_price', 'products_amount'),
              'order_items', ('date_shipping', 'status'), ('payment_type', 'payment_status'), 'address',
              'address_last_name', ('address_street', 'address_home_number'), ('address_ZIP', 'address_city'),
              'phone_number', 'invoice')

    def address(self, instance):
        street = instance.address_street + ' ' + instance.address_home_number
        city = instance.address_ZIP + ' ' + instance.address_city
        return format_html_join(
            mark_safe('<br>'),
            '{}',
            ((line,) for line in
             [instance.address_last_name, street, city, instance.phone_number])
        )

    address.short_description = 'Full address'

    def order_items(self, instance):
        items = instance.order_items.all()
        render = '<tr><td>Title of product</td><td>Quantity</td><tr>'
        for line in items:
            render += f'<tr><td>{line.product}</td><td style="text-align:center">{line.quantity}</td></tr>'
        render_html = "<table>" + render + "</table>"
        return format_html(
            render_html
        )

    order_items.short_description = 'Products in oder'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'id', 'product', 'quantity', 'price', 'discount')

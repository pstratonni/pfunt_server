from decouple import config
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from shop.models import Purchaser, Cart, CartItem, Order, OrderItem, Delivery, Tax


@receiver(post_save, sender=User)
def create_cart(sender, instance, created, **kwargs):
    if created:
        Purchaser.objects.create(user=instance)
        Cart.objects.create(user=instance)


@receiver(post_save, sender=CartItem)
def update_cart(sender, instance, **kwargs):
    cart = Cart.objects.get(pk=instance.cart.id)
    cart_item = CartItem.objects.get(pk=instance.id)
    cart_item.update_cart_item()
    cart.update_cart()


@receiver(post_save, sender=Order)
def create_order_items(sender, instance, created, **kwargs):
    if created:
        if instance.user:
            cart = Cart.objects.get(user=instance.user)
        else:
            cart = Cart.objects.get(ip=instance.ip)
        try:
            cart_items = CartItem.objects.filter(cart=cart)
            for item in cart_items:
                if item.product.active:
                    OrderItem.objects.create(order=instance, quantity=item.quantity, price=item.price,
                                             product=item.product, discount=item.discount, total_price=item.total_price)

            order = Order.objects.get(pk=instance.id)
            delivery_cost = Delivery.objects.latest('id').price

            if delivery_cost > order.products_price:
                order.delivery_cost = delivery_cost
                order.total_price = order.products_price + order.delivery_cost
            else:
                order.total_price = order.products_price

            order.update_order()
            order_items = OrderItem.objects.filter(order=order)
            tax = Tax.objects.latest('id').annotate(sum=F('tax_cost')/100*order.total_price)
            cart.delete()

            if instance.user:
                Cart.objects.create(user=instance.user)
            else:
                Cart.objects.create(ip=instance.ip)

            html_order = render_to_string(
                'order.html',
                {
                    'order': order,
                    'order_items': order_items,
                    'tax': tax,
                }
            )

            order_message = EmailMultiAlternatives(
                subject=f'Bestellung №{order.id} ist am {order.date_created.strftime("%d.%m.%Y")} angekommen',
                body=f'Bestellung TEEEEEEEEEEst',
                from_email=config('EMAIL_USER'),
                to=[config('EMAIL_USER'), order.email]
            )
            order_message.attach_alternative(html_order, 'text/html')
            order_message.send()
        except:
            pass


@receiver(post_save, sender=OrderItem)
def update_order_items(sender, instance, created, **kwargs):
    if not created:
        order = Order.objects.get(pk=instance.order.id)
        order.update_order()
        delivery = Delivery.objects.filter(date_created__lte=order.date_created).latest('id')
        if delivery.price > order.total_price:
            order.delivery_cost = delivery.cost
            order.total_price += order.delivery_cost
        else:
            order.delivery_cost = 0

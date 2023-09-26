from decimal import Decimal

from django.contrib.auth.models import User
from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver

from shop.models import Purchaser, Cart, CartItem, Order, OrderItem, Delivery, Tax
from shop.service import send_email_with_attach


@receiver(post_save, sender=User)
def create_cart(sender, instance, created, **kwargs):
    if created:
        Purchaser.objects.create(user=instance)
        Cart.objects.create(user=instance)


@receiver(post_save, sender=CartItem)
def update_cart_(sender, instance, **kwargs):
    cart = Cart.objects.get(pk=instance.cart.id)
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
            delivery = Delivery.objects.latest('id')

            order.update_order(delivery.price, delivery.cost)

            order_items = OrderItem.objects.filter(order=order)
            tax_cost = Tax.objects.latest('id').tax_cost
            tax_sum = float((Decimal(str(tax_cost / 100)) * order.total_price) * 100 // 1 / 100)
            tax = {
                'tax_cost': tax_cost,
                'tax_sum': tax_sum,
            }
            cart.delete()
            if instance.user:
                Cart.objects.create(user=instance.user)
            else:
                Cart.objects.create(ip=instance.ip)

            send_email_with_attach(order, order_items, tax)
        except:
            pass


recursion = False


@receiver(post_save, sender=OrderItem)
def update_order_items(sender, instance, created, **kwargs):
    if not created:
        global recursion
        if recursion:
            pass
        else:
            recursion = True
            OrderItem.objects.get(pk=instance.id).update_price()
            order = Order.objects.get(pk=instance.order.id)
            delivery = Delivery.objects.latest('id')
            order.update_order(delivery.price, delivery.cost)
            recursion = False

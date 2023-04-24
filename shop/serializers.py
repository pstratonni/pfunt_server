from rest_framework import serializers

from shop.models import *


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = "__all__"


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


# class CompositionSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Composition
#         fields = ('title',)


class ProductDetailSerializer(serializers.ModelSerializer):
    composition = serializers.SlugRelatedField(slug_field='title', read_only=True, many=True, )

    class Meta:
        model = Product
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = '__all__'


class OrderIPSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


# class OrderItemToOrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OrderItem
#         fields = ('product', 'quantity', 'price')


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderRetrieveSerializer(serializers.ModelSerializer):
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    order_items = OrderItemSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Order
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    # product = serializers.SlugRelatedField(slug_field='title', read_only=True)

    def create(self, validated_data):
        product = Product.objects.get(pk=validated_data.get('product', None).id)
        cart_item, _ = CartItem.objects.filter(cart=validated_data.get('cart'))\
                                       .update_or_create(product=product,
                                                         defaults={**validated_data})
        return cart_item


    class Meta:
        model = CartItem
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    cart_items = CartItemSerializer(many=True, required=False)

    class Meta:
        model = Cart
        fields = '__all__'


class CartIPSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, required=False)

    class Meta:
        model = Cart
        fields = '__all__'


class PurchaserRetrieveSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Purchaser
        fields = '__all__'

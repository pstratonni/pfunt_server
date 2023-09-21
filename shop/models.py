from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Sum


class Delivery(models.Model):
    cost = models.DecimalField(default=0, validators=[MinValueValidator(0.0)], max_digits=5, decimal_places=2)
    price = models.DecimalField(default=0, validators=[MinValueValidator(0.0)], max_digits=5, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'price {self.price} cost {self.cost}'


class Purchaser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address_city = models.CharField(max_length=20, null=True, blank=True, verbose_name='Stadt')
    address_ZIP = models.CharField(max_length=5, null=True, blank=True, verbose_name='PLZ')
    address_street = models.CharField(max_length=50, null=True, blank=True, verbose_name='Straße')
    address_home_number = models.CharField(max_length=5, null=True, blank=True, verbose_name='Hausnumer')
    address_last_name = models.CharField(max_length=20, null=True, blank=True, verbose_name='Nachname')
    favorite_product = models.ForeignKey('Product', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Kunde"
        verbose_name_plural = "Kunden"
        ordering = ['user']


class Manufacturer(models.Model):
    title = models.CharField(max_length=50)
    address_city = models.CharField(max_length=50)
    address_street = models.CharField(max_length=50)
    address_ZIP = models.CharField(max_length=10)
    address_home_number = models.CharField(max_length=5)
    img_manufacturer = models.ImageField(upload_to='author_img')
    activ = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def deactivate_manufacturer(self):
        for product in self.product_set.all():
            product.active = False
        self.save()

    class Meta:
        verbose_name = 'Hersteller'
        verbose_name_plural = 'Hersteller'
        ordering = ['title']


class Product(models.Model):
    title = models.CharField(max_length=150)
    subtitle = models.CharField(max_length=150, default='')
    cooking = models.TextField(default='', blank=True)
    description = models.TextField(default='', blank=True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.SET_NULL, null=True)
    weight = models.IntegerField(validators=[MinValueValidator(1)], default=500)
    price = models.DecimalField(validators=[MinValueValidator(0.0)], max_digits=5, decimal_places=2)
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                                   default=0)
    image = models.ImageField(upload_to='product_img')
    amount = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    prepared = models.BooleanField(default=False)
    composition = models.ManyToManyField('Composition', related_name='product')
    vendor_code = models.CharField(max_length=15, default='9-')
    thumbnail = models.ManyToManyField('Thumbnail', related_name='product', blank=True)
    category = models.ManyToManyField('Category', related_name='product')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['id']


class Composition(models.Model):
    title = models.CharField(max_length=150)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Zutaten"
        verbose_name_plural = "Zutaten"
        ordering = ['title']


class Thumbnail(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='thumbnails_img')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Bild"
        verbose_name_plural = "Bilder"
        ordering = ['title']


class Category(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['title']


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='orders')
    ip = models.CharField(max_length=20, null=True)
    email = models.EmailField(default='')
    products_price = models.DecimalField(default=0, validators=[MinValueValidator(0.0)],
                                         max_digits=5, decimal_places=2)
    total_price = models.DecimalField(default=0, validators=[MinValueValidator(0.0)],
                                      max_digits=5, decimal_places=2)
    products_amount = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    delivery_cost = models.DecimalField(default=0, validators=[MinValueValidator(0.0)],
                                        max_digits=5, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)
    date_shipping = models.DateTimeField(null=True)
    STATUSES = [
        ('UNF', 'angenommen'),
        ('CON', 'bestätigt'),
        ('COL', 'gesammelt'),
        ('SHI', 'verschickt')
    ]
    status = models.CharField(choices=STATUSES, default='UNF', max_length=3)
    PAYMENTS = [
        ('PP', 'PayPal'),
        ('BG', 'Bar')
    ]
    payment_type = models.CharField(choices=PAYMENTS, max_length=2, default='BG')
    PAY_STATUS = [
        ('PAI', 'bezahlt'),
        ('UNP', 'unbezahlt')
    ]
    payment_status = models.CharField(choices=PAY_STATUS, max_length=3, default='UNP')
    address_city = models.CharField(max_length=20, default='')
    address_ZIP = models.CharField(max_length=5, default='')
    address_street = models.CharField(max_length=50, default='')
    address_home_number = models.CharField(max_length=5, default='')
    address_last_name = models.CharField(max_length=20, default='')
    phone_number = models.CharField(max_length=20, default='')

    def __str__(self):
        return f'{self.user}, {self.date_created.strftime("%d.%m.%Y %H:%M:%S")}'

    def update_order(self):
        self.products_price = sum([order_item.total_price for order_item in self.order_items.all()])
        # self.products_amount = sum([order_item.quantity for order_item in self.order_items.all()])
        self.products_amount = self.order_items.aggregate(Sum('quantity'))
        self.save()

    class Meta:
        ordering = ['-date_created']


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.IntegerField(validators=[MinValueValidator(1)], default=1)
    price = models.DecimalField(default=0, validators=[MinValueValidator(0.0)], max_digits=5, decimal_places=2)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=True, default=0)
    total_price = models.DecimalField(default=0, validators=[MinValueValidator(0.0)], max_digits=5, decimal_places=2)


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='cart')
    total_price = models.DecimalField(default=0, validators=[MinValueValidator(0.0)], max_digits=5, decimal_places=2)
    total_amount = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    ip = models.CharField(max_length=20, null=True, blank=True)

    def update_cart(self):
        self.total_price = sum([cart_item.total_price for cart_item in self.cart_items.all()])
        self.total_amount = sum([cart_item.quantity for cart_item in self.cart_items.all()])
        self.save()

    def __str__(self):
        try:
            return f'{self.user.username}'
        except:
            return f'{self.ip}'


class CartItem(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.IntegerField(validators=[MinValueValidator(1)], default=1)
    price = models.DecimalField(default=0, validators=[MinValueValidator(0.0)], max_digits=5, decimal_places=2)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=True, default=0)
    total_price = models.DecimalField(default=0, validators=[MinValueValidator(0.0)], max_digits=5, decimal_places=2)

    def __str__(self):
        return f'{self.cart.id}'

    def update_cart_item(self):
        self.total_price = self.quantity * self.price
        self.save()


class FAQ(models.Model):
    question = models.CharField(max_length=50)
    answer = models.TextField()

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQ's"
        ordering = ['id']


class Tax(models.Model):
    tax_cost = models.IntegerField(default=7, validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return f"{self.tax_cost}%"

    class Meta:
        verbose_name = "Steuer"
        verbose_name_plural = "Steuern"
        ordering = ['id']
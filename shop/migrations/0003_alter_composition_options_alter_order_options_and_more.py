# Generated by Django 4.0 on 2023-03-21 21:57

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('shop', '0002_cartitem_composition_order_orderitem_purchaser_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='composition',
            options={'ordering': ['title'], 'verbose_name': 'Zutaten', 'verbose_name_plural': 'Zutaten'},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['title']},
        ),
        migrations.AlterModelOptions(
            name='purchaser',
            options={'ordering': ['user'], 'verbose_name': 'Kunde', 'verbose_name_plural': 'Kunden'},
        ),
        migrations.RemoveField(
            model_name='cart',
            name='purchaser',
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cart', to='auth.user'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='ip',
            field=models.CharField(default='', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='cart',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='shop.cart'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='discount',
            field=models.IntegerField(default=0, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='product',
            name='discount',
            field=models.IntegerField(default=0, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='purchaser',
            name='address_ZIP',
            field=models.CharField(blank=True, max_length=5, null=True, verbose_name='PLZ'),
        ),
        migrations.AlterField(
            model_name='purchaser',
            name='address_city',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Stadt'),
        ),
        migrations.AlterField(
            model_name='purchaser',
            name='address_home_number',
            field=models.CharField(blank=True, max_length=5, null=True, verbose_name='Hausnumer'),
        ),
        migrations.AlterField(
            model_name='purchaser',
            name='address_last_name',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Nachname'),
        ),
        migrations.AlterField(
            model_name='purchaser',
            name='address_street',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Straße'),
        ),
    ]

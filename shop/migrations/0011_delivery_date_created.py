# Generated by Django 4.0 on 2023-03-29 21:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_delivery_order_delivery_cost_order_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]

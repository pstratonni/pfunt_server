# Generated by Django 4.1.1 on 2023-09-20 19:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0041_product_vendor'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='vendor',
            new_name='vendor_code',
        ),
    ]

# Generated by Django 3.1.14 on 2023-02-08 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0016_orders_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproducts',
            name='product_quantity',
            field=models.IntegerField(default=0, verbose_name='Количество'),
        ),
    ]

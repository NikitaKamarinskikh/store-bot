# Generated by Django 3.1.14 on 2023-01-31 11:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_auto_20230131_1124'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='products',
        ),
        migrations.AddField(
            model_name='orderproducts',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.orders', verbose_name='Заказ'),
        ),
    ]

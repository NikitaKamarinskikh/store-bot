# Generated by Django 3.1.14 on 2023-01-24 16:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clients', '0002_auto_20230122_1401'),
        ('products', '0002_productimages'),
    ]

    operations = [
        migrations.CreateModel(
            name='BasketProducts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_quantity', models.PositiveIntegerField(verbose_name='Количество товара')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clients.clients', verbose_name='Клиент')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.products', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Корзина',
                'verbose_name_plural': 'Товары в корзине',
            },
        ),
    ]

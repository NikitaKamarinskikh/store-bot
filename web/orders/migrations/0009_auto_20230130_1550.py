# Generated by Django 3.1.14 on 2023-01-30 15:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_auto_20230128_1436'),
        ('transport_companies', '0001_initial'),
        ('orders', '0008_auto_20230130_1522'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orders',
            options={'ordering': ['-created_at'], 'verbose_name': 'Заказ', 'verbose_name_plural': 'Заказы'},
        ),
        migrations.RemoveField(
            model_name='orders',
            name='client_info',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='product_quantity',
        ),
        migrations.AddField(
            model_name='orders',
            name='recipient_full_name',
            field=models.CharField(default='asd', max_length=255, verbose_name='ФИО получателя'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orders',
            name='transport_company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='transport_companies.transportcompanies', verbose_name='Транспортная компания'),
        ),
        migrations.CreateModel(
            name='OrderProducts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('additional_products', models.ManyToManyField(blank=True, to='products.AdditionalProducts', verbose_name='Дополнительные товары')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.orders', verbose_name='Товары заказа')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.products', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'товар в заказе',
                'verbose_name_plural': 'Товары в заказе',
            },
        ),
    ]

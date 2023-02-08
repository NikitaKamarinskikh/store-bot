# Generated by Django 3.1.14 on 2023-02-08 04:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_auto_20230128_1436'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='additional_products',
        ),
        migrations.AddField(
            model_name='additionalproducts',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.products', verbose_name='Товар'),
        ),
        migrations.AlterField(
            model_name='products',
            name='sizes',
            field=models.CharField(blank=True, max_length=60, null=True, verbose_name='Размеры'),
        ),
    ]
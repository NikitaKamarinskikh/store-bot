# Generated by Django 3.1.14 on 2023-03-01 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0004_clients_orders_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='clients',
            name='registration_date',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата регистрации'),
        ),
    ]
# Generated by Django 3.1.14 on 2023-02-09 15:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_auto_20230209_1431'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subcategories',
            options={'verbose_name': 'Подкатегория', 'verbose_name_plural': 'Подкатегории'},
        ),
    ]

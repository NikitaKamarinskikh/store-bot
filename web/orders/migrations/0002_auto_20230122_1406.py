# Generated by Django 3.1.14 on 2023-01-22 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='desired_completion_date',
            field=models.DateField(verbose_name='Желаемая дата выполнения'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='last_completion_date',
            field=models.DateField(verbose_name='Желаемая дата выполнения'),
        ),
    ]

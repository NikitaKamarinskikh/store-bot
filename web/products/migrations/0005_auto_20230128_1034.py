# Generated by Django 3.1.14 on 2023-01-28 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20230128_0855'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdditionalProducts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('price', models.PositiveIntegerField(verbose_name='Стоимость')),
            ],
            options={
                'verbose_name': 'Дополнительный товар',
                'verbose_name_plural': 'Дополнительные товары',
            },
        ),
        migrations.AddField(
            model_name='products',
            name='additional_products',
            field=models.ManyToManyField(to='products.AdditionalProducts', verbose_name='Дополнительные опции'),
        ),
    ]

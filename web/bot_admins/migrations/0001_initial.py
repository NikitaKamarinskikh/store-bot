# Generated by Django 3.1.14 on 2023-01-23 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BotAdmins',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_id', models.CharField(max_length=100, verbose_name='Телеграмм ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Имя')),
            ],
            options={
                'verbose_name': 'Админ бота',
                'verbose_name_plural': 'Админы бота',
            },
        ),
    ]

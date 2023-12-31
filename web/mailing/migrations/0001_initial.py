# Generated by Django 3.1.14 on 2023-01-31 20:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MailingLists',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст')),
                ('clients_category', models.CharField(choices=[('ALL', 'Все'), ('HAS_ORDERS', 'Всем кто делал заказы'), ('HAS_NO_ORDER', 'Всем кто не делал заказы')], max_length=100, verbose_name='Категория пользователей')),
            ],
            options={
                'verbose_name': 'Рассылка',
                'verbose_name_plural': 'Рассылки',
            },
        ),
        migrations.CreateModel(
            name='MailingListsVideos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_id', models.CharField(max_length=255, verbose_name='ID файла в телеграмме')),
                ('mailing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailing.mailinglists', verbose_name='Рассылка')),
            ],
            options={
                'verbose_name': 'Видеоролик',
                'verbose_name_plural': 'Видеоролики',
            },
        ),
        migrations.CreateModel(
            name='MailingListsImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_id', models.CharField(max_length=255, verbose_name='ID файла в телеграмме')),
                ('mailing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailing.mailinglists', verbose_name='Рассылка')),
            ],
            options={
                'verbose_name': 'Фотография',
                'verbose_name_plural': 'Фотографии',
            },
        ),
    ]

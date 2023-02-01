# Generated by Django 3.1.14 on 2023-02-01 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0014_auto_20230131_1944'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='track_number',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Трек номер'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='status',
            field=models.CharField(choices=[('PENDING_PROCESSING', 'Ожидает обработки'), ('IN_PROGRESS', 'В работе'), ('IN_DELIVERY', 'Передан в доставку'), ('SENT', 'Отправлен'), ('REJECTED', 'Отклонен')], default='PENDING_PROCESSING', max_length=100, verbose_name='Статус'),
        ),
    ]

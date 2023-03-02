from django.db import models
from web.clients.models import Clients
from web.products.models import Products, AdditionalProducts
from web.transport_companies.models import TransportCompanies
from config import OrderStatuses
from .notifications import notify_client_about_order_in_progress_status, notify_client_about_order_in_delivery_status,\
    notify_client_about_order_in_sent_status
from .services import check_client_referrer


class Orders(models.Model):
    client = models.ForeignKey(Clients, verbose_name='Клиент', on_delete=models.CASCADE)
    recipient_full_name = models.CharField(verbose_name='ФИО получателя', max_length=255)
    created_at = models.DateTimeField(verbose_name='Дата заказа', auto_now_add=True)
    transport_company = models.ForeignKey(TransportCompanies, verbose_name='Транспортная компания', on_delete=models.CASCADE, null=True, blank=True)
    phone_number = models.CharField(verbose_name='Номер телефона', max_length=255)
    delivery_address = models.CharField(verbose_name='Адрес доставки', max_length=255)
    desired_completion_date = models.CharField(verbose_name='Желаемая дата выполнения', max_length=100)
    last_completion_date = models.CharField(verbose_name='Последняя дата выполнения', max_length=100)
    track_number = models.CharField(verbose_name='Трек номер', max_length=255, null=True, blank=True)
    status = models.CharField(verbose_name='Статус', max_length=100, choices=OrderStatuses.choices(), default=OrderStatuses.PENDING_PROCESSING.name)
    amount = models.PositiveIntegerField(verbose_name='Общая стоимость', default=0)
    bonus_coins = models.PositiveIntegerField(verbose_name='Количество бонусов', default=0)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._old_status = self.status
        self._old_track_number = self.track_number

    def __str__(self) -> str:
        return f'{self.client}'

    def save(self, *args, **kwargs):
        if self.status != self._old_status:
            if self.status == OrderStatuses.IN_PROGRESS.name:
                notify_client_about_order_in_progress_status(self.client.telegram_id, self.pk)
                check_client_referrer(self.client.telegram_id, self.amount)

            elif self.status == OrderStatuses.IN_DELIVERY.name:
                notify_client_about_order_in_delivery_status(self.client.telegram_id, self.pk)
            self._old_status = self.status
    
        if self.track_number != self._old_track_number:
            notify_client_about_order_in_sent_status(self.client.telegram_id, self.pk, self.track_number)
            self._old_track_number = self.track_number

        super(Orders, self).save(*args, **kwargs)

    class Meta:
        ordering= ['-created_at']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderProducts(models.Model):
    order = models.ForeignKey(Orders, verbose_name='Заказ', on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Products, verbose_name='Товар', on_delete=models.CASCADE)
    product_quantity = models.IntegerField(verbose_name='Количество', default=0)
    additional_products = models.ManyToManyField(AdditionalProducts, verbose_name='Дополнительные товары', blank=True)

    def __str__(self) -> str:
        return self.order.__str__()

    class Meta:
        verbose_name = 'товар в заказе'
        verbose_name_plural = 'Товары в заказе'


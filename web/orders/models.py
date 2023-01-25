from django.db import models
from web.clients.models import Clients
from web.products.models import Products
from web.certificates.models import Certificates
from config import OrderStatuses


class Orders(models.Model):
    client = models.ForeignKey(Clients, verbose_name='Клиент', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, verbose_name='Товар', on_delete=models.CASCADE)
    product_quantity = models.PositiveIntegerField('Количество товара')
    client_info = models.CharField(verbose_name='Информация о клиенте', max_length=255)
    created_at = models.DateField(verbose_name='Дата заказа', auto_now_add=True)
    desired_completion_date = models.DateField(verbose_name='Желаемая дата выполнения')
    last_completion_date = models.DateField(verbose_name='Последняя дата выполнения')
    status = models.CharField(verbose_name='Статус', max_length=100, choices=OrderStatuses.choices(), default=OrderStatuses.PENDING_PROCESSING.name)

    def __str__(self) -> str:
        return f"{self.client} | {self.product} | {self.product_quantity}"
    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'



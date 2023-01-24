from django.db import models
from web.clients.models import Clients
from web.products.models import Products


class BasketProducts(models.Model):
    client = models.ForeignKey(Clients, verbose_name='Клиент', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, verbose_name='Товар', on_delete=models.CASCADE)
    product_quantity = models.PositiveIntegerField(verbose_name='Количество товара')
    created_at = models.DateTimeField(verbose_name='Дата и время создания', auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.client} | {self.product} | {self.product_quantity}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Корзина'



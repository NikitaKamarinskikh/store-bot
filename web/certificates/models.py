from django.db import models
from web.clients.models import Clients


class Certificates(models.Model):
    client = models.ForeignKey(Clients, verbose_name='Клиент', null=True, blank=True,
                                on_delete=models.CASCADE)
    hash = models.CharField(verbose_name='Хэш', max_length=255)
    amount = models.PositiveIntegerField(verbose_name='Сумма')
    is_activated = models.BooleanField('Активирован', default=False)

    def __str__(self) -> str:
        return f"{self.hash[:10]} | {self.amount}"
    
    class Meta:
        verbose_name = 'Сертификат'
        verbose_name_plural = 'Сертификаты'







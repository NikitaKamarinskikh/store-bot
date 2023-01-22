from django.db import models


class Clients(models.Model):
    telegram_id = models.CharField("Телеграмм ID", max_length=50)
    username = models.CharField("Телеграмм username", max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        return self.telegram_id
    
    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'



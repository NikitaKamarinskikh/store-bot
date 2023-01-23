from django.db import models


class BotAdmins(models.Model):
    telegram_id = models.CharField(verbose_name='Телеграмм ID', max_length=100)
    name = models.CharField(verbose_name='Имя', max_length=100, null=True, blank=True)

    def  __str__(self) -> str:
        if self.name:
            return self.name
        return self.telegram_id
    
    class Meta:
        verbose_name = 'Админ бота'
        verbose_name_plural = 'Админы бота'



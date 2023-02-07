from django.db import models


class Managers(models.Model):
    telegram_id = models.CharField(verbose_name='ID в телеграмме', max_length=255)
    name = models.CharField(verbose_name='Имя', max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        if self.name:
            return self.name
        return self.telegram_id
    
    class Meta:
        verbose_name = 'Менеджер'
        verbose_name_plural  = 'Менеджеры'




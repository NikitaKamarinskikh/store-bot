from django.db import models


class Documents(models.Model):
    name = models.CharField(verbose_name='Название', max_length=255)
    type = models.CharField(verbose_name='Тип', max_length=255)
    file = models.FileField(verbose_name='Файл')


    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'


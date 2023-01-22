from django.db import models


class TransportCompanies(models.Model):
    name = models.CharField(verbose_name='Название', max_length=255)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = 'Транспортная компания'
        verbose_name_plural = 'Транспортные компании'



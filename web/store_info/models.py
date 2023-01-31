from django.db import models


class StoreInfo(models.Model):
    text = models.TextField()

    def __str__(self) -> str:
        return self.text[:20]
    
    class Meta:
        verbose_name = 'Общая информация'
        verbose_name_plural = 'Общая информация'


class StoreInfoImages(models.Model):
    info = models.ForeignKey(StoreInfo, verbose_name='Описание', on_delete=models.CASCADE)
    telegram_id = models.CharField(verbose_name='ID файла в телеграмме', max_length=255)

    def __str__(self) -> str:
        return self.telegram_id

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'


class StoreInfoVideos(models.Model):
    info = models.ForeignKey(StoreInfo, verbose_name='Описание', on_delete=models.CASCADE)
    telegram_id = models.CharField(verbose_name='ID файла в телеграмме', max_length=255)

    def __str__(self) -> str:
        return self.telegram_id

    class Meta:
        verbose_name = 'Видеоролик'
        verbose_name_plural = 'Видеоролики'






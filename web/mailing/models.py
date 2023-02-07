from django.db import models
from config import ClientsCategories


class MailingLists(models.Model):
    text = models.TextField(verbose_name='Текст')
    clients_category = models.CharField(verbose_name='Категория пользователей', max_length=100,
                                        choices=ClientsCategories.choices())
    sending_time = models.DateTimeField(verbose_name='Время отправки', blank=True, null=True)


    def __str__(self) -> str:
        return self.text[:20]
    
    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class MailingListsImages(models.Model):
    mailing = models.ForeignKey(MailingLists, verbose_name='Рассылка', on_delete=models.CASCADE)
    telegram_id = models.CharField(verbose_name='ID файла в телеграмме', max_length=255)

    def __str__(self) -> str:
        return self.telegram_id

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'


class MailingListsVideos(models.Model):
    mailing = models.ForeignKey(MailingLists, verbose_name='Рассылка', on_delete=models.CASCADE)
    telegram_id = models.CharField(verbose_name='ID файла в телеграмме', max_length=255)

    def __str__(self) -> str:
        return self.telegram_id

    class Meta:
        verbose_name = 'Видеоролик'
        verbose_name_plural = 'Видеоролики'






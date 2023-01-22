from django.contrib import admin
from .models import Clients


@admin.register(Clients)
class ClientsAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', 'username')

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


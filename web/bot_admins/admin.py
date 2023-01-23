from django.contrib import admin
from .models import BotAdmins


@admin.register(BotAdmins)
class BotAdminsAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', 'name')

    class Meta:
        model = BotAdmins


from django.contrib import admin
from .models import Managers


@admin.register(Managers)
class ManagersAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', 'name')

    class Meta:
        model = Managers



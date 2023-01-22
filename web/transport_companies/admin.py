from django.contrib import admin
from .models import TransportCompanies


@admin.register(TransportCompanies)
class TransportCompaniesAdmin(admin.ModelAdmin):
    list_display = ('name', )

    class Meta:
        model = TransportCompanies



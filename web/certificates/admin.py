from django.contrib import admin
from .models import Certificates


@admin.register(Certificates)
class CertificatesAdmin(admin.ModelAdmin):
    list_display = ('client', 'hash', 'amount', 'is_activated')

    class Meta:
        model = Certificates


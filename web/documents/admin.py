from django.contrib import admin
from .models import Documents


@admin.register(Documents)
class DocumentsAdmin(admin.ModelAdmin):
    list_display = ('name',)


    class Meta:
        model = Documents

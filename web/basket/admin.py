from django.contrib import admin
from .models import BasketProducts


@admin.register(BasketProducts)
class BasketProductsAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', )

    class Meta:
        model = BasketProducts



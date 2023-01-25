from django.contrib import admin
from .models import BasketProducts


@admin.register(BasketProducts)
class BasketProductsAdmin(admin.ModelAdmin):
    list_display = ('client', 'product', 'product_quantity', 'created_at')
    readonly_fields = ('created_at', )

    class Meta:
        model = BasketProducts



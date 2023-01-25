from django.contrib import admin
from .models import Orders


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ('client', 'product', 'product_quantity', 'created_at',
                    'desired_completion_date', 'last_completion_date', 'status')
    list_display_links  = ('client', 'product')
    readonly_fields = ('created_at',)
    list_filter = ('status',)

    class Meta:
        model = Orders



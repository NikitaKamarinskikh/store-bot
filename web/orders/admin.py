from django.contrib import admin
from .models import Orders, OrderProducts


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ('client', 'created_at',
                    'desired_completion_date', 'last_completion_date', 'status')
    list_display_links  = ('client',)
    readonly_fields = ('created_at',)
    list_filter = ('status',)

    class Meta:
        model = Orders


@admin.register(OrderProducts)
class OrderProductsAdmin(admin.ModelAdmin):
    list_display = ('order', 'product')

    class Meta:
        model = OrderProducts


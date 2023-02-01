from __future__ import annotations
from web.orders.models import Orders, OrderProducts
from web.clients.models import Clients
from web.transport_companies.models import TransportCompanies
from config import OrderData


def create(order_data: OrderData) -> Orders:
    client = Clients.objects.get(telegram_id=order_data.client_telegram_id)
    transport_company = TransportCompanies.objects.get(pk=order_data.transport_company_id)

    order = Orders.objects.create(
        client=client,
        recipient_full_name=order_data.recipient_full_name,
        transport_company=transport_company,
        phone_number=order_data.recipient_phone_number,
        delivery_address=order_data.delivery_address,
        desired_completion_date=order_data.desired_completion_date,
        last_completion_date=order_data.last_completion_date,
        amount=order_data.amount
    )

    for basket_product in order_data.products:
        order_product = OrderProducts.objects.create(
            order=order,
            product=basket_product.product
        )
        for additional_basket_product in basket_product.additional_products.all():
            order_product.additional_products.add(additional_basket_product)
        order_product.save()


    return order




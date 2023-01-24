from typing import List
from web.basket.models import BasketProducts
from web.clients.models import Clients
from web.products.models import Products


def create(client_id: int, product_id: int, products_quantity: int) -> BasketProducts:
    client = Clients.objects.get(pk=client_id)
    product = Products.objects.get(pk=product_id)
    return BasketProducts.objects.create(
        client=client,
        product=product,
        products_quantity=products_quantity
    )


def get_products_by_client_id(client_id: int) -> List[BasketProducts]:
    client = Clients.objects.get(pk=client_id)
    return list(BasketProducts.objects.filter(client=client))



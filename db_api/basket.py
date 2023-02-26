from typing import List
from web.basket.models import BasketProducts
from web.clients.models import Clients
from web.products.models import Products, AdditionalProducts
from config import BasketInfo


def add(client_telegram_id: int, product_id: int, additional_products: List[int], product_quantity: int = 0) -> BasketProducts:
    client = Clients.objects.get(telegram_id=client_telegram_id)
    product = Products.objects.get(pk=product_id)
    additional_products = AdditionalProducts.objects.filter(pk__in=additional_products)
    basket = BasketProducts.objects.create(
        client=client,
        product=product,
        product_quantity=product_quantity
    )
    for additional_product in additional_products:
        basket.additional_products.add(additional_product)
    basket.save()
    return basket


def get_products_by_client_telegram_id(client_id: int) -> List[BasketProducts]:
    client = Clients.objects.get(telegram_id=client_id)
    return list(BasketProducts.objects.filter(client=client))


def clear(client_telegrm_id: int) -> None:
    client = Clients.objects.get(telegram_id=client_telegrm_id)
    BasketProducts.objects.filter(client=client).delete()


def get_info(client_telegram_id: int) -> BasketInfo:
    products_quantity = 0
    amount = 0
    client = Clients.objects.get(telegram_id=client_telegram_id)
    client_products = BasketProducts.objects.filter(client=client)
    for product in client_products:
        amount += product.product.price * product.product_quantity
        for additional_product in product.additional_products.all():
            amount += additional_product.price
        products_quantity += 1
    return BasketInfo(
        products_quantity=products_quantity,
        amount_in_rub=amount
    )


def remove(product_id: int) -> None:
    return BasketProducts.objects.filter(pk=product_id).delete()

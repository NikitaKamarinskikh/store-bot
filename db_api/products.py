from  typing import List
from web.products.models import Categories, Subcategories, Products, ProductImages, AdditionalProducts


def get_all_categories() -> List[Categories]:
    return list(Categories.objects.all())


def get_category_by_id(category_id: int) -> Categories:
    return Categories.objects.get(pk=category_id)


def get_all_subcategories() -> List[Subcategories]:
    return list(Subcategories.objects.all())


def get_subcategories_by_category_id(category_id: int)  -> List[Categories]:
    category = Categories.objects.get(pk=category_id)
    return Subcategories.objects.filter(category=category)


def get_products_by_category_and_subcategory(category_id: int, subcategory_id: int) -> List[Products]:
    category = Categories.objects.get(pk=category_id)
    subcategory = Subcategories.objects.get(pk=subcategory_id)
    return Products.objects.filter(category=category, subcategory=subcategory)


def get_product_by_id(product_id: int) -> Products:
    return Products.objects.get(pk=product_id)


def get_additional_products_by_product_id(product_id: int) -> List[AdditionalProducts]:
    product = Products.objects.get(pk=product_id)
    return list(AdditionalProducts.objects.filter(product=product))


def get_all_products() -> List[Products]:
    return list(Products.objects.all())


def get_product_images_by_product_id(product_id: int) -> List[ProductImages]:
    product = Products.objects.get(pk=product_id)
    return ProductImages.objects.filter(product=product)


def get_products_by_name_pattern(pattern: str) -> List[Products]:
    products = Products.objects.all()
    filtered_products = [product for product in products if _levenstein(product.name, pattern) <= 3]
    return filtered_products


def _levenstein(lhs: str, rhs: str) -> int:
    lhs = lhs.lower()
    rhs = rhs.lower()
    n, m = len(lhs), len(rhs)
    if n > m:
        lhs, rhs = rhs, lhs
        n, m = m, n

    current_row = range(n + 1)
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if lhs[j - 1] != rhs[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]


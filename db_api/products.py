from  typing import List, Union
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


def get_products_by_category_or_category_and_subcategory(category_id: int, subcategory_id: int = None) -> List[Products]:
    filtered_products = []
    category = Categories.objects.get(pk=category_id)
    subcategory = Subcategories.objects.filter(pk=subcategory_id).first()
    products = Products.objects.filter(category=category)
    for product in products:
        if product.subcategory is not None:
            if product.subcategory == subcategory:
                filtered_products.append(product)
        else:
            filtered_products.append(product)
    return filtered_products


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
    filtered_products = [product for product in products
                            if pattern.lower() in product.name.lower()]
    return filtered_products


def get_first_image(product_id: str):
    product = Products.objects.get(pk=product_id)
    images = ProductImages.objects.filter(product=product)
    return images.first()



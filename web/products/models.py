from django.db import models


class Categories(models.Model):
    name = models.CharField(verbose_name='Название', max_length=60)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Subcategories(models.Model):
    name = models.CharField(verbose_name='Название', max_length=60)
    category =  models.ForeignKey(Categories, verbose_name='Категория', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Пдокатегории'



class AdditionalProducts(models.Model):
    name = models.CharField(verbose_name='Название', max_length=255)
    price = models.PositiveIntegerField(verbose_name='Стоимость')

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Дополнительный товар'
        verbose_name_plural= 'Дополнительные товары'


class Products(models.Model):
    name = models.CharField(verbose_name='Название', max_length=255)
    category = models.ForeignKey(Categories, verbose_name='Категория', on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategories, verbose_name='Подкатегория', on_delete=models.CASCADE)
    description = models.TextField(verbose_name='Описание')
    sizes = models.CharField(verbose_name='Размеры', max_length=60)
    price = models.IntegerField(verbose_name='Цена')
    additional_products = models.ManyToManyField(AdditionalProducts, verbose_name='Дополнительные опции')

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class ProductImages(models.Model):
    product = models.ForeignKey(Products, verbose_name='Товар', on_delete=models.CASCADE)
    photo = models.CharField(verbose_name='ID файла', max_length=255)

    class Meta:
        verbose_name = 'Фото товара'
        verbose_name_plural = 'Фото товаров'



from django.db import models


class Categories(models.Model):
    name = models.CharField(verbose_name="Название", max_length=60)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Subcategories(models.Model):
    name = models.CharField(verbose_name="Название", max_length=60)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Пдокатегории"


class Products(models.Model):
    name = models.CharField(verbose_name="Название", max_length=255)
    category = models.ForeignKey(Categories, verbose_name="Категория", on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategories, verbose_name="Подкатегория", on_delete=models.CASCADE)
    description = models.TextField(verbose_name="Описание")
    sizes = models.CharField(verbose_name="Размеры", max_length=60)
    price = models.IntegerField(verbose_name="Цена")

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"



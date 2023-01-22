from django.contrib import admin

from .models import Products, Categories, Subcategories

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'subcategory', 'price')

    class Meta:
        model = Products


@admin.register(Categories)
class CategorieasAdmin(admin.ModelAdmin):

    class Meta:
        model = Categories


@admin.register(Subcategories)
class SubcategoriesAdmin(admin.ModelAdmin):

    class Meta:
        model = Subcategories





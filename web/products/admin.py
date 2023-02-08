from django.contrib import admin

from .models import Products, ProductImages, Categories, Subcategories, AdditionalProducts


@admin.register(ProductImages)
class ProductImagesAdmin(admin.ModelAdmin):

    class Meta:
        model = ProductImages


class ProductImagesinline(admin.StackedInline):
    model = ProductImages
    extra = 0


@admin.register(AdditionalProducts)
class AdditionalProductsAdmin(admin.ModelAdmin):

    class Meta:
        model = AdditionalProducts


class AdditionalProductsInline(admin.StackedInline):
    model = AdditionalProducts
    extra = 0


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'subcategory', 'price')
    inlines = [ProductImagesinline, AdditionalProductsInline]

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




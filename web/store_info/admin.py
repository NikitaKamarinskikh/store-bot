from django.contrib import admin
from .models import StoreInfo, StoreInfoImages, StoreInfoVideos



@admin.register(StoreInfoImages)
class StoreInfoImagesAdmin(admin.ModelAdmin):

    class Meta:
        model = StoreInfoImages


@admin.register(StoreInfoVideos)
class StoreInfoVideosAdmin(admin.ModelAdmin):

    class Meta:
        model = StoreInfoVideos


class StoreInfoImagesInline(admin.StackedInline):
    model = StoreInfoImages
    extra = 0


class StoreInfoVideosInline(admin.StackedInline):
    model = StoreInfoVideos
    extra = 0


@admin.register(StoreInfo)
class StoreInfoAdmin(admin.ModelAdmin):
    inlines = [StoreInfoImagesInline, StoreInfoVideosInline]

    class Model:
        model = StoreInfo


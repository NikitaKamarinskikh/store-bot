from django.contrib import admin

from .models import MailingLists, MailingListsImages, MailingListsVideos



@admin.register(MailingListsImages)
class MailingListsImagesAdmin(admin.ModelAdmin):

    class Meta:
        model = MailingListsImages


@admin.register(MailingListsVideos)
class MailingListsVideosAdmin(admin.ModelAdmin):

    class Meta:
        model = MailingListsVideos


class MailingListsImagesInline(admin.StackedInline):
    model = MailingListsImages
    extra = 0


class MailingListsVideosInline(admin.StackedInline):
    model = MailingListsVideos
    extra = 0


@admin.register(MailingLists)
class StoreInfoAdmin(admin.ModelAdmin):
    inlines = [MailingListsImagesInline, MailingListsVideosInline]

    class Model:
        model = MailingLists





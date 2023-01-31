from exceptions.exceptions import InfoDoesNotExists
from web.store_info.models import StoreInfo, StoreInfoImages, StoreInfoVideos
from config import StoreInfoDescription


def get_info() -> StoreInfoDescription:
    store_info_object = StoreInfoDescription()
    info = StoreInfo.objects.filter().first()
    if info is None:
        raise InfoDoesNotExists()
    info_images = StoreInfoImages.objects.filter(info=info)
    info_videos = StoreInfoVideos.objects.filter(info=info)
    store_info_object.text = info.text
    for image in info_images:
        store_info_object.images.append(image.telegram_id)
    for video in info_videos:
        store_info_object.images.append(video.telegram_id)
    return store_info_object


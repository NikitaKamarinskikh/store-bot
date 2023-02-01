from typing import Union
from web.certificates.models import Certificates
from web.clients.models import Clients


def get_by_hash_or_none(hash: str) -> Union[Certificates, None]:
    return Certificates.objects.filter(hash=hash).first()


def make_activated(client_telegram_id: int, certificate_id: int) -> None:
    certificate = Certificates.objects.get(pk=certificate_id)
    client = Clients.objects.get(telegram_id=client_telegram_id)
    certificate.client = client
    certificate.is_activated = True
    certificate.save()




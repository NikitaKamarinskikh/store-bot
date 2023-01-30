from __future__ import annotations
from typing import List
from web.transport_companies.models import TransportCompanies


def get_all() -> List[TransportCompanies]:
    return list(TransportCompanies.objects.all())


def get_by_id(transport_company_id: int) -> TransportCompanies:
    return TransportCompanies.objects.get(pk=transport_company_id)


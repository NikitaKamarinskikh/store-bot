from __future__ import annotations
from typing import List
from web.transport_companies.models import TransportCompanies



def get_all() -> List[TransportCompanies]:
    return TransportCompanies.objects.all()



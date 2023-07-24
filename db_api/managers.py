from typing import List
from web.managers.models import Managers


def get_all_managers() -> List[Managers]:
    return list(Managers.objects.all())


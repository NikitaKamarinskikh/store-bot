from aiogram.dispatcher.filters.state import StatesGroup, State


class CertificatesStates(StatesGroup):
    get_certificate_hash = State()


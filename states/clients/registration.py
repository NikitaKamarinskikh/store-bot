from aiogram.dispatcher.filters.state import StatesGroup, State


class ClientRegistrationStates(StatesGroup):
    get_full_name = State()
    get_phone_number = State()
    get_address = State()
    get_transport_company = State()




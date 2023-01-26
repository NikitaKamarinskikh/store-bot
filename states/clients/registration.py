from aiogram.dispatcher.filters.state import StatesGroup, State


class ClientRegistrationStates(StatesGroup):
    accept_welcome_message = State()
    accept_privacy_policy = State()

    # get_full_name = State()
    # get_phone_number = State()
    # get_address = State()
    # get_transport_company = State()




from aiogram.dispatcher.filters.state import StatesGroup, State


class ClientRegistrationStates(StatesGroup):
    accept_welcome_message = State()
    accept_privacy_policy = State()



from aiogram.dispatcher.filters.state import StatesGroup, State


class MakeOrderStates(StatesGroup):
    get_category = State()
    get_subcategory = State()
    get_product_quantity = State()
    get_full_name = State()
    get_desired_completion_date = State()
    get_last_completion_date = State()
    # get_certificate = State()


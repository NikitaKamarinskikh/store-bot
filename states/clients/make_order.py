from aiogram.dispatcher.filters.state import StatesGroup, State


class MakeOrderStates(StatesGroup):
    get_recipient_full_name = State()
    get_recipient_phone_number = State()
    get_transport_company = State()
    get_delivery_address = State()
    get_desired_completion_date = State()
    get_last_completion_date = State()
    confirm_order = State()


class ProductNotInCategoryStates(StatesGroup):
    get_product_description = State()
    get_full_name = State()
    get_phone_number = State()


class WholesaleOrder(StatesGroup):
    get_wholesale_order_info = State()
    get_full_name = State()
    get_phone_number = State()


class GetProductFromCatalogStates(StatesGroup):
    get_category = State()
    get_subcategory = State()
    chose_product = State()


class UpdateOrderStates(StatesGroup):
    get_order_point = State()
    update_receiver_full_name = State()
    update_receiver_phone_number = State()
    update_transport_company = State()
    update_delivery_address = State()
    update_desired_completion_date = State()
    update_last_completion_date = State()




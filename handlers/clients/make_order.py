from aiogram import types
from aiogram.dispatcher import FSMContext
from main import dp
from messages_texts import MainMenuMessagesTexts
from states.clients.make_order import MakeOrderStates
from re import match


@dp.message_handler(text=MainMenuMessagesTexts.make_order)
async def start_making_order(message: types.Message):
    await message.answer('Выберите категорию')
    await MakeOrderStates.get_category.set()


@dp.message_handler(state=MakeOrderStates.get_category)
async def get_category(message: types.Message, state: FSMContext):
    category = message.text
    await state.update_data(category=category)
    await message.answer('Укажите подкатегорию')
    await MakeOrderStates.get_subcategory.set()


@dp.message_handler(state=MakeOrderStates.get_subcategory)
async def get_subcategory(message: types.Message, state: FSMContext):
    subcategory = message.text
    await state.update_data(subcategory=subcategory)
    await message.answer('Укажите количество выбранного товара')
    await MakeOrderStates.get_product_quantity.set()


@dp.message_handler(state=MakeOrderStates.get_product_quantity)
async def get_product_quantity(message: types.Message, state: FSMContext):
    product_quantity = message.text
    if _is_correct_product_quantity(product_quantity):
        await state.update_data(product_quantity=int(product_quantity))
        await message.answer('Укажите ожидаемую дату готовности')
        # TODO:
        # - add calendar
        await MakeOrderStates.get_desired_completion_date.set()
    else:
        await message.answer('Количество товара должно быть указано числом больше 0')


@dp.message_handler(state=MakeOrderStates.get_desired_completion_date)
async def get_desired_completion_date(message: types.Message, state: FSMContext):
    desired_date = message.text
    await state.update_data(desired_date=desired_date)
    await message.answer('Укажите крайную дату готовности')
    await MakeOrderStates.get_last_completion_date.set()


@dp.message_handler(state=MakeOrderStates.get_last_completion_date)
async def get_last_completion_date(message: types.Message, state: FSMContext):
    last_date = message.text
    print(last_date)
    order_data = await state.get_data()
    print(order_data)
    await message.answer('Заказ успешно создан. Ожидайте ответа от менеджера')
    await state.finish()


def _is_correct_product_quantity(quantity: str) -> bool:
    # ^[1-9][1-9]*$ - check number greather then zero
    return match('^[1-9][1-9]*$', quantity) is not None




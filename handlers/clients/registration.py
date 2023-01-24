from re import match
from aiogram import types
from aiogram.dispatcher import FSMContext
from main import dp
from keyboards.default.get_contact import get_phone_markup
from states.clients.registration import ClientRegistrationStates
from db_api import transport_companies
from keyboards.inline.transport_companies import transport_companies_markup, transport_companies_callback


@dp.message_handler(text='test_registration')
async def start_registration(message: types.Message):
    await ClientRegistrationStates.get_full_name.set()  
    await message.answer('Укажите фио')   


@dp.message_handler(state=ClientRegistrationStates.get_full_name)
async def get_full_name(message: types.Message, state: FSMContext):
    full_name = message.text
    if _is_correct_full_name(full_name):
        await state.update_data(full_name=full_name)
        await ClientRegistrationStates.get_phone_number.set()
        await message.answer(
            'Отправьте ваш номер телефона сообщением, либо воспользуйтесь прикрепленной кнопкой',
            reply_markup=get_phone_markup
        )
    else:
        await message.answer('ФИО указано неверно')


@dp.message_handler(content_types=types.ContentTypes.CONTACT, state=ClientRegistrationStates.get_phone_number)
async def get_phone_number_by_button(message: types.Message, state: FSMContext):
    phone_number = message.contact.phone_number
    await state.update_data(phone_number=phone_number)
    await _ask_delivery_address(message)


@dp.message_handler(state=ClientRegistrationStates.get_phone_number)
async def get_phone_number_by_message(message: types.Message, state: FSMContext):
    phone_number = message.text
    if phone_number.isdigit():
        await state.update_data(phone_number=phone_number)
        await _ask_delivery_address(message)
    else:
        await message.answer('Номер телефона может содержать только цифры')


@dp.message_handler(state=ClientRegistrationStates.get_address)
async def get_address(message: types.Message, state: FSMContext):
    address = message.text
    await state.update_data(address=address)
    await ClientRegistrationStates.get_transport_company.set()
    transport_companies_list = transport_companies.get_all()
    await message.answer(
        'Укажите транспортную компанию',
        reply_markup=transport_companies_markup(transport_companies_list)
    )


@dp.callback_query_handler(transport_companies_callback.filter(), state=ClientRegistrationStates.get_transport_company)
async def get_transport_company(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    transport_company_id = callback_data.get('id')
    print(transport_company_id)
    await state.finish()
    await callback.message.answer('Регистрация прошла успешно')


async def _ask_delivery_address(message: types.Message) -> None:
    await ClientRegistrationStates.get_address.set()
    await message.answer(
        'Укажите адресс доставки',
        reply_markup=types.ReplyKeyboardRemove()
    )


def _is_correct_full_name(full_name: str) -> bool:
    # ^[а-яА-ЯёЁ]{2,30} [а-яА-ЯёЁ]{2,30} [а-яА-ЯёЁ]{2,30}$ - three Cyrillic words separated by a space 
    return match('^[а-яА-ЯёЁ]{2,30} [а-яА-ЯёЁ]{2,30} [а-яА-ЯёЁ]{2,30}$', full_name) is not None



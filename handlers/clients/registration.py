from re import match
from aiogram import types
from aiogram.dispatcher import FSMContext
from main import dp
from keyboards.default.get_contact import get_phone_markup
from states.clients.registration import ClientRegistrationStates


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
    await _ask_address(message)


@dp.message_handler(state=ClientRegistrationStates.get_phone_number)
async def get_phone_number_by_message(message: types.Message, state: FSMContext):
    phone_number = message.text
    if phone_number.isdigit():
        await state.update_data(phone_number=phone_number)
        await _ask_address(message)
    else:
        await message.answer('Номер телефона может содержать только цифры')


@dp.message_handler(state=ClientRegistrationStates.get_address)
async def get_address(message: types.Message, state: FSMContext):
    address = message.text
    await state.update_data(address=address)
    await ClientRegistrationStates.get_transport_company.set()
    # TODO:
    #   - load companies list
    await message.answer('Укажите транспортную компанию')


@dp.message_handler(state=ClientRegistrationStates.get_transport_company)
async def get_transport_company(message: types.Message, state: FSMContext):
    transport_company = message.text
    await state.finish()
    await message.answer('Регистрация прошла успешно')


async def _ask_address(message: types.Message) -> None:
    await ClientRegistrationStates.get_address.set()
    await message.answer(
        'Укажите адресс доставки',
        reply_markup=types.ReplyKeyboardRemove()
    )


def _is_correct_full_name(full_name: str) -> bool:
    # ^[а-яА-ЯёЁ]{2,30} [а-яА-ЯёЁ]{2,30} [а-яА-ЯёЁ]{2,30}$ - three Cyrillic words separated by a space 
    return match('^[а-яА-ЯёЁ]{2,30} [а-яА-ЯёЁ]{2,30} [а-яА-ЯёЁ]{2,30}$', full_name) is not None



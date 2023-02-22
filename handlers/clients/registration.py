import os
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from main import dp, bot
from config import MEDIA_URL, PRIVACY_POLICY_FILE_TYPE
from keyboards.default.one_button_markup import one_button_markup
from keyboards.default.main_markup import create_main_markup
from states.clients.registration import ClientRegistrationStates
from messages_texts import RegistrationMessagesTexts,MAIN_MENU_TEXT
from db_api import clients, basket as basket_model, documents as documents_model
from notifications import client_notification
from referral_program.referral_program import load_referral_program_settings_from_json_file


@dp.message_handler(CommandStart())
async def start(message: types.Message, state: FSMContext):
    client = clients.get_by_telegram_id_or_none(message.from_user.id)
    if client is None:
        await message.answer(
            'Здравствуйте. Добро пожаловать. Здесь вы можете приобрести экипировку производства "Bear Gear"',
            reply_markup=one_button_markup(RegistrationMessagesTexts.accept_welcome_message)
        )
        await ClientRegistrationStates.accept_welcome_message.set()

        referrer_telegram_id = None
        message_args = message.get_args()
        if message_args.isdigit():  # Приведен пользователем
            referrer_telegram_id = message_args
        await state.update_data(referrer_telegram_id=referrer_telegram_id)
    else:
        basket_info = basket_model.get_info(message.from_user.id)
        await message.answer(
            'Вы уже зарегистрированы в боте',
            reply_markup=create_main_markup(basket_info)
        )


@dp.message_handler(text=RegistrationMessagesTexts.accept_welcome_message,
                    state=ClientRegistrationStates.accept_welcome_message)
async def accept_welcome_message(message: types.Message):
    await message.answer(
        'Чтобы сделать заказ нужно согласиться с правилами бота, в том числе касаемо ваших персональных данных.',
        reply_markup=one_button_markup(RegistrationMessagesTexts.accept_privacy_policy_message)
    )
    privacy_policy = documents_model.get_document_by_type(PRIVACY_POLICY_FILE_TYPE)
    file_name = privacy_policy.file.name
    file_path = os.path.join(os.path.abspath(os.getcwd()), f'web/media/{file_name}')
    file = types.InputFile(file_path)
    await message.answer_document(file)
    await ClientRegistrationStates.accept_privacy_policy.set()


@dp.message_handler(text=RegistrationMessagesTexts.accept_privacy_policy_message,
                    state=ClientRegistrationStates.accept_privacy_policy)
async def accept_privacy_policy(message: types.Message, state: FSMContext):
    await _register_client(message, state)
    await message.answer(
        MAIN_MENU_TEXT,
        reply_markup=create_main_markup()
    )
    await state.finish()


async def _register_client(message: types.Message, state: FSMContext) -> None:
    client_data = {
        'telegram_id': message.from_user.id,
        'username': message.from_user.username
    }

    state_data = await state.get_data()
    referrer_telegram_id = state_data.get('referrer_telegram_id')

    if referrer_telegram_id is not None:
        client_data['referrer_telegram_id'] =  referrer_telegram_id
        referral_program_settings = load_referral_program_settings_from_json_file()
        if referral_program_settings.user_acquisition_reward_satus:
            client_notification.notify_client_about_new_referral(message.from_user.id, referral_program_settings.user_acquisition_reward)

        client_data['bonus_coins_quantity'] = 100

    clients.create(**client_data)










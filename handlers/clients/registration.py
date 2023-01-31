from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from main import dp
from config import PRIVACY_POLICY_FILE_TELEGRAM_ID
from keyboards.default.one_button_markup import one_button_markup
from keyboards.default.main_markup import main_markup
from states.clients.registration import ClientRegistrationStates
from messages_texts import RegistrationMessagesTexts
from db_api import clients
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
        await message.answer(
            'Вы уже зарегистрированы в боте',
            reply_markup=main_markup
        )


@dp.message_handler(text=RegistrationMessagesTexts.accept_welcome_message,
                    state=ClientRegistrationStates.accept_welcome_message)
async def accept_welcome_message(message: types.Message):
    await message.answer(
        'Чтобы сделать заказ нужно согласиться с правилами бота, в том числе касаемо ваших персональных данных.',
        reply_markup=one_button_markup(RegistrationMessagesTexts.accept_privacy_policy_message)
    )
    await message.answer_document(PRIVACY_POLICY_FILE_TELEGRAM_ID)
    await ClientRegistrationStates.accept_privacy_policy.set()


@dp.message_handler(text=RegistrationMessagesTexts.accept_privacy_policy_message,
                    state=ClientRegistrationStates.accept_privacy_policy)
async def accept_privacy_policy(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    referrer_telegram_id = state_data.get('referrer_telegram_id')
    if referrer_telegram_id is not None:
        referral_program_settings = load_referral_program_settings_from_json_file()
        if referral_program_settings.user_acquisition_reward_satus:
            client_notification.notify_client_about_new_referral(message.from_user.id, referral_program_settings.user_acquisition_reward)

    clients.create(message.from_user.id, message.from_user.username)
    await message.answer(
        """Главное меню:
1. Заказ - для выбора из каталога, оформления нестандартного заказа, а так же оптового заказа.
2. Поиск - поиск по каталогу. Нажмите кнопку и начните вводить то что ищите.
3. Кошелек - ваши бонусные монеты, за заказы и приглашения, которые можете потратить на
4. Общая информация""",
    reply_markup=main_markup
    )

    await state.finish()









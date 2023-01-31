from aiogram import types
from aiogram.dispatcher import FSMContext
from main import dp
from messages_texts import MainMenuMessagesTexts, ReferralProgramMessagesTexts
from db_api import clients as clients_model
from referral_program.referral_program import load_referral_program_settings_from_json_file
from keyboards.default.referral_program_markups import referral_program_markup


@dp.message_handler(text=MainMenuMessagesTexts.bonuses)
async def show_bonuses(message: types.Message):
    referral_program_settings = load_referral_program_settings_from_json_file()
    client = clients_model.get_by_telegram_id_or_none(message.from_user.id)
    referrals_quantity = clients_model.get_client_referrals_quantity(message.from_user.id)
    data = f"""
У вас {client.coins} монет, вы можете их потратить на приобретение снаряжения.
Приглашенных пользователей: {referrals_quantity}

За приглашение нового пользователя вы получите {referral_program_settings.user_acquisition_reward} монет после его первой покупки, а так же сразу получит {referral_program_settings.referral_reward} монет на первую покупку.
Кроме того, со всех покупок приглашенного вы будете получать {referral_program_settings.referral_order_reward_in_percentages}% в виде монет на свой бонусный счет.
Со своих покупок будете получать {referral_program_settings.make_order_reward_in_percentages}% на счет.
    """
    await message.answer(
        data,
        reply_markup=referral_program_markup
    )


@dp.message_handler(text=ReferralProgramMessagesTexts.invite_user)
async def invite_user(message: types.Message):
    referral_program_settings = load_referral_program_settings_from_json_file()
    await message.answer(
        f'Просто скопируй или перешли сообщение ниже. В нем твоя ссылка, по которой приглашенный сразу получит {referral_program_settings.referral_reward} монет на первый заказ, а ты получишь свой бонус {referral_program_settings.user_acquisition_reward} монет, после его первого заказа. Кроме того сразу же получишь еще и % от его заказа.'
    )
    bot_name = (await message.bot.get_me()).username
    referral_link = f"https://t.me/{bot_name}?start={message.from_user.id}"
    await message.answer(
        f'Получи {referral_program_settings.referral_reward} монет на первый заказ снаряжения и экипировки в мастерской BearGear по этой ссылке: {referral_link}'
    )



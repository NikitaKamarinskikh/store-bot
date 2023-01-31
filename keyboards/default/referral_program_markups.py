from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from messages_texts import ReferralProgramMessagesTexts


referral_program_markup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(ReferralProgramMessagesTexts.invite_user), KeyboardButton(ReferralProgramMessagesTexts.back)],
    ],
    resize_keyboard=True
)


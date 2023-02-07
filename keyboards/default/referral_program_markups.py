from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from messages_texts import ReferralProgramMessagesTexts


referral_program_markup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(ReferralProgramMessagesTexts.invite_user), KeyboardButton(ReferralProgramMessagesTexts.back)],
        [KeyboardButton(ReferralProgramMessagesTexts.activate_certificate)]
    ],
    resize_keyboard=True
)


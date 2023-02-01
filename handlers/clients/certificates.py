from aiogram import types
from aiogram.dispatcher import FSMContext
from main import dp
from states.clients.certificates import CertificatesStates
from messages_texts import MainMenuMessagesTexts
from db_api import certificates, clients


@dp.message_handler(text=MainMenuMessagesTexts.certificate)
async def certificate(message: types.Message):
    await message.answer('Введите код сертификата')
    await CertificatesStates.get_certificate_hash.set()


@dp.message_handler(state=CertificatesStates.get_certificate_hash)
async def get_certificate_hash(message: types.Message, state: FSMContext):
    hash = message.text
    certificate = certificates.get_by_hash_or_none(hash)
    if certificate is not None:
        certificates.make_activated(message.from_user.id, certificate.pk)
        clients.add_coins(message.from_user.id, certificate.amount)
        await message.answer(f'Сертификат успешно активирован. Вам зачислен бонус {certificate.amount} монет')
    else:
        await message.answer('Сертификат не найден')
    await state.finish()



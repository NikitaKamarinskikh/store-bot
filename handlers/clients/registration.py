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


from typing import List
from web.products.models import ProductImages
from db_api import products as products_model
from keyboards.inline import product_markups
from states.clients.make_order import GetProductFromCatalogStates
from main import bot


@dp.message_handler(CommandStart())
async def start(message: types.Message, state: FSMContext):
    await state.finish()
    await GetProductFromCatalogStates.chose_product.set()
    await _test(message, state)
    # client = clients.get_by_telegram_id_or_none(message.from_user.id)
    # if client is None:
    #     await message.answer(
    #         'Здравствуйте. Добро пожаловать. Здесь вы можете приобрести экипировку производства "Bear Gear"',
    #         reply_markup=one_button_markup(RegistrationMessagesTexts.accept_welcome_message)
    #     )
    #     await ClientRegistrationStates.accept_welcome_message.set()
    # else:
    #     await message.answer('Вы уже зарегистрированы в боте')


async def _test(message: types.Message, state: FSMContext):
    products = products_model.get_all_products()
    products_ids_list = [product.pk for product in products]
    await state.update_data(products_ids_list=products_ids_list)
    markup = product_markups.chose_product_markup(products[0].pk, 0, len(products))
    product = products[0]
    product_images = products_model.get_product_images_by_product_id(product.pk)
    if product_images:
        album = _collect_image_files_to_media_group(product_images)
        images_id = await message.answer_media_group(album)
        await state.update_data(images_id=images_id)
    else:
        await state.update_data(images_id=None)
    r = await message.answer(
        text=f'{product.name}\n{product.description}',
        reply_markup=markup
    )
    await state.update_data(menu_message_id=r.message_id)


@dp.callback_query_handler(product_markups.next_product_callback.filter(), state=GetProductFromCatalogStates.chose_product)
async def next_product(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    index = int(callback_data.get('index'))
    state_data = await state.get_data()
    products_ids_list = state_data.get('products_ids_list')
    images_id = state_data.get('images_id')
    next_product_id = products_ids_list[index]
    product = products_model.get_product_by_id(next_product_id)

    markup = product_markups.chose_product_markup(next_product_id, index, len(products_ids_list))
    product_images = products_model.get_product_images_by_product_id(product.pk)
    if images_id:
        for image_id in images_id:
            await bot.delete_message(
                chat_id=callback.from_user.id,
                message_id=image_id.message_id
            )
        await state.update_data(images_id=None)
    if product_images:
        album = _collect_image_files_to_media_group(product_images)
        images_id = await callback.message.answer_media_group(album)
        menu_message_id = state_data.get('menu_message_id')
        await bot.delete_message(
            chat_id=callback.from_user.id,
            message_id=menu_message_id
        )
        r = await callback.message.answer(
            text=f'{product.name}\n{product.description}',
            reply_markup=markup
        )
        await state.update_data(images_id=images_id, menu_message_id=r.message_id)
    else:
        menu_message_id = state_data.get('menu_message_id')
        await bot.edit_message_text(
            chat_id=callback.from_user.id,
            message_id=menu_message_id,
            text=f'{product.name}\n{product.description}',
            reply_markup=markup
        )


def _collect_image_files_to_media_group(product_images: List[ProductImages]) -> types.MediaGroup():
    album = types.MediaGroup()
    for product_image in product_images:
        album.attach_photo(product_image.telegram_id)
    return album



















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









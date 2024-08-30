from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
import buttons
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from db import db_main

sizes = ['S', 'L', 'XL', 'XXL']


class Store(StatesGroup):
    name = State()
    size = State()
    category = State()
    price = State()
    id_product = State()
    info_product = State()
    collection_product = State()
    photo = State()
    submit = State()


async def fsm_start(message: types.Message):
    await message.answer(text='Название товара: \n',
                              reply_markup=buttons.cancel)
    await Store.name.set()


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await Store.next()
    await message.answer(text='Размер: ', reply_markup=buttons.size)


async def load_size(message: types.Message, state: FSMContext):
    if message.text in sizes:
        async with state.proxy() as data:
            data['size'] = message.text
    else:
        await message.answer('Только кнопки!!!')

    await Store.next()
    await message.answer(text='Категория: ', reply_markup=buttons.cancel)


async def load_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text

    await Store.next()
    await message.answer(text='Стоимость: ')


async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text

    await Store.next()
    await message.answer(text='Отправьте айди: ')


async def load_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data_store:
        data_store['id_product'] = message.text

    await Store.next()
    await message.answer(text='Напишите Информацию товара:')


async def load_info(message: types.Message, state: FSMContext):
    async with state.proxy() as data_store:
        data_store['info_product'] = message.text

    await Store.next()
    await message.answer(text='Отправьте коллекцию товара:')


async def load_collection(message: types.Message, state: FSMContext):
    async with state.proxy() as data_store:
        data_store['collection_product'] = message.text

    await Store.next()
    await message.answer(text='Отправьте фотографию товара:')


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id

    keyboard = InlineKeyboardMarkup(row_width=2)
    yes_button = InlineKeyboardButton(text='Да', callback_data='confirm_yes')
    no_button = InlineKeyboardButton(text='Нет', callback_data='confirm_no')
    keyboard.add(yes_button, no_button)

    await Store.next()
    await message.answer_photo(photo=data['photo'],
                               caption=f"Название товара - {data['name']}\n"
                                       f"Размер - {data['size']}\n"
                                       f"Категория - {data['category']}\n"
                                       f"Стоимость - {data['price']}\n"
                                       f"Информация о товаре - {data['info_product']}\n"
                                       f"Коллекия - {data['collection_product']}\n",


                               reply_markup=keyboard)


async def submit(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == 'confirm_yes':

        await callback_query.message.answer('Отлично! Регистрация заказа пройдена.', reply_markup=buttons.remove)
        async with state.proxy() as data_store:
            await db_main.sql_insert_products(
                name=data_store['name'],
                size=data_store['size'],
                price=data_store['price'],
                id_product=data_store['id_product'],
                photo=data_store['photo']
            )

            await db_main.sql_insert_products_details(
                category=data_store['category'],
                info_product=data_store['info_product'],
                id_product=data_store['id_product']
            )

            await db_main.sql_insert_collection_products(
                product_id = data_store['id_product'],
                collection = data_store['collection_product'],

            )
        await state.finish()
    elif callback_query.data == 'confirm_no':
        await callback_query.message.answer('Отменено!', reply_markup=buttons.remove)
        await state.finish()


async def cancel_fsm(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer(text='Отменено!', reply_markup=buttons.cancel)


def register_fsm(dp: Dispatcher):
    dp.register_message_handler(cancel_fsm, Text(equals='Отмена',
                                                            ignore_case=True),
                                                            state="*")

    dp.register_message_handler(fsm_start, commands=['registration'])
    dp.register_message_handler(load_name, state=Store.name)
    dp.register_message_handler(load_size, state=Store.size)
    dp.register_message_handler(load_category, state=Store.category)
    dp.register_message_handler(load_price, state=Store.price)
    dp.register_message_handler(load_id, state=Store.id_product)
    dp.register_message_handler(load_info, state=Store.info_product)
    dp.register_message_handler(load_collection, state=Store.collection_product)
    dp.register_message_handler(load_photo, state=Store.photo, content_types=['photo'])
    dp.register_callback_query_handler(submit, state=Store.submit)


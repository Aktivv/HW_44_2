from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
import buttons
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

sizes = ['S', 'L', 'XL', 'XXL']

class Store(StatesGroup):
    name = State()
    size = State()
    category = State()
    price = State()
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
    await message.answer(text='Категория: ')


async def load_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text

    await Store.next()
    await message.answer(text='Стоимость: ')


async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text

    await Store.next()
    await message.answer(text='Отправьте фотографию: ')


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id

    keyboard = InlineKeyboardMarkup(row_width=2)
    yes_button = InlineKeyboardButton(text='Yes', callback_data='confirm_yes')
    no_button = InlineKeyboardButton(text='No', callback_data='confirm_no')
    keyboard.add(yes_button, no_button)

    await Store.next()
    await message.answer_photo(photo=data['photo'],
                               caption=f"Название товара - {data['name']}\n"
                                       f"Размер - {data['size']}\n"
                                       f"Категория - {data['category']}\n"
                                       f"Стоимость - {data['price']}\n",
                               reply_markup=keyboard)


async def submit(callback_query: types.CallbackQuery, state: FSMContext):
    kb = types.ReplyKeyboardRemove()

    if callback_query.data == 'confirm_yes':
        await callback_query.message.answer('Сохранено в базу',
                                            reply_markup=kb)
        await state.finish()
    elif callback_query.data == 'confirm_no':
        await callback_query.message.answer('Отменено!')
        await state.finish()


async def cancel_fsm(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer(text='Отменено!')


def register_fsm(dp: Dispatcher):
    dp.register_message_handler(cancel_fsm, Text(equals='Отмена',
                                                            ignore_case=True),
                                                            state="*")

    dp.register_message_handler(fsm_start, commands=['registration'])
    dp.register_message_handler(load_name, state=Store.name)
    dp.register_message_handler(load_size, state=Store.size)
    dp.register_message_handler(load_category, state=Store.category)
    dp.register_message_handler(load_price, state=Store.price)
    dp.register_message_handler(load_photo, state=Store.photo, content_types=['photo'])
    dp.register_callback_query_handler(submit, state=Store.submit)


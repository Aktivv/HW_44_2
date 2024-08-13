from aiogram import types, Dispatcher
from config import bot


# @dp.message_handler()
async def echo_handler(message: types.Message):
    if message.text.isdigit():
        await message.answer(int(message.text)**2)
    else:
        await message.answer(message.text)


def register_echo(dp: Dispatcher):
    dp.register_message_handler(echo_handler)

from aiogram import types, Dispatcher
from config import bot
from aiogram.types import InputFile
import glob
import random
import os
from db import db_main


# @dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await bot.send_message(
            chat_id=message.from_user.id,
            text=f'Привет {message.from_user.first_name}'
            )
    await message.answer(text='Привет')
    print(message.from_user.id)
    await db_main.sql_insert_registration(telegram_id=message.from_user.id,
                                          firstname=message.from_user.first_name)


async def info_handler(message: types.Message):
    await message.answer('Алибабла, новый бот')


async def send_mem(message: types.Message):
    path = 'media/'
    files = glob.glob(os.path.join(path, '*'))
    random_photo = random.choice(files)

    await bot.send_photo(chat_id=message.from_user.id,
                         photo=InputFile(random_photo))


async def send_file(message: types.Message):
    await bot.send_document(
        chat_id=message.from_user.id,
        document=open('main.py', 'rb'),
    )


async def game_dice(message: types.Message):
    games = ['⚽', '🎰', '🏀', '🎯', '🎳', '🎲']
    await bot.send_dice(
        chat_id=message.from_user.id,
        emoji=random.choice(games)
    )


def register_commands(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands="start")
    dp.register_message_handler(info_handler, commands="info")
    dp.register_message_handler(send_mem, commands="mem")
    dp.register_message_handler(send_file, commands="file")
    dp.register_message_handler(game_dice, commands="game")

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

cancel = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Отмена')
)
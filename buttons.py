from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

cancel = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Отмена')
)

size = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(text='S'),
                                                     KeyboardButton(text='L'),
                                                     KeyboardButton(text='XL'),
                                                     KeyboardButton(text='XXL')
                                                     )
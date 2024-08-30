# from aiogram import types

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove


cancel = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Отмена')
)

size = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(text='S'),
                                                     KeyboardButton(text='L'),
                                                     KeyboardButton(text='XL'),
                                                     KeyboardButton(text='XXL'),
                                                     KeyboardButton('Отмена')
                                                     )

remove = ReplyKeyboardRemove()



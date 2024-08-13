from aiogram import types, Dispatcher
from config import bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def quiz(message: types.Message):
    # button_quiz = InlineKeyboardMarkup(row_width=1)
    # button_quiz_1 = InlineKeyboardButton("Первая!",
    #                                      callback_data="button_1")
    # button_quiz_2 = InlineKeyboardButton("Вторая",
    #                                      callback_data="button_2")
    # button_quiz_3 = InlineKeyboardButton("Третья",
    #                                      callback_data="button_3")
    # button_quiz.add(button_quiz_1, button_quiz_2, button_quiz_3)
    #
    # await message.answer(text='Проверка кнопок',
    #                      reply_markup=button_quiz)

    button_quiz = InlineKeyboardMarkup()
    button_quiz.add(InlineKeyboardButton("Дальше!",
                                         callback_data="button_1"))

    question = 'Месси или Роналду'

    answer = ['Месси', 'Роналду', 'Никто']

    await bot.send_poll(
        chat_id=message.from_user.id,
        question=question,
        options=answer,
        is_anonymous=True,
        type='quiz',
        correct_option_id=2,
        explanation='Ну ты даешь :)',
        open_period=60,
        reply_markup=button_quiz
    )


async def quiz_2(call: types.CallbackQuery):
    button_quiz = InlineKeyboardMarkup()
    button_quiz.add(InlineKeyboardButton("Дальше!",
                                         callback_data="button_2"))

    question = 'Фортнайт или пабг'

    answer = ['Fortnite', 'Pubg', 'CS-2', "Free fire",
              "Call of Duty", "Mobile legends"]

    await bot.send_poll(
        chat_id=call.from_user.id,
        question=question,
        options=answer,
        is_anonymous=True,
        type='quiz',
        correct_option_id=0,
        explanation='Ты че не шаришь, позер',
        open_period=60,
        reply_markup=button_quiz
    )


# async def quiz_3(call: types.CallbackQuery):
#     question = 'Backend, Frontend or IOS developer'
#
#     answer = ["Backend", "Frontend", "IOS"]
#
#     await bot.send_photo(chat_id=call.from_user.id,
#                          photo=open('media/img_3.png', 'rb'))
#
#     await bot.send_poll(
#         chat_id=call.from_user.id,
#         question=question,
#         options=answer,
#         is_anonymous=True,
#         type='quiz',
#         allows_multiple_answers=True,
#         explanation='Ты че не шаришь, позер'
#     )


async def quiz_3(call: types.CallbackQuery):
    button_quiz = InlineKeyboardMarkup()
    button_quiz.add(InlineKeyboardButton("Дальше!",
                                         callback_data="button_3"))

    question = 'Кошка или собака'

    answer = ['Кошка', 'Собака']

    await bot.send_photo(chat_id=call.from_user.id,
                         photo=open('media/Кот.jpg', 'rb'))
    await bot.send_photo(chat_id=call.from_user.id,
                         photo=open('media/собака.jpg', 'rb'))

    await bot.send_poll(
        chat_id=call.from_user.id,
        question=question,
        options=answer,
        is_anonymous=True,
        allows_multiple_answers=True,
        # correct_option_id=False,
        explanation='О вкусах не спорят:)',
        open_period=60,
        )


def register_quiz(dp: Dispatcher):
    dp.register_message_handler(quiz, commands=['quiz'])
    dp.register_callback_query_handler(quiz_2, text='button_1')
    dp.register_callback_query_handler(quiz_3, text='button_2')

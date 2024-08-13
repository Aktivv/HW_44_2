from aiogram import types
import logging
from config import dp, bot, Admins
from aiogram.utils import executor
from handlers import commands, echo


async def on_startup(_):
    for i in Admins:
        await bot.send_message(
            chat_id=i,
            text='Вруум-Вруум'
        )

commands.register_commands(dp)


echo.register_echo(dp)




if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

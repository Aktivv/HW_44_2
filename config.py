from aiogram import dispatcher, Bot, Dispatcher
from decouple import config

TOKEN = config('TOKEN')
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
admins = ['1277330153']

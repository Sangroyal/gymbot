import logging
import os
import datetime

from aiogram import Bot, Dispatcher, executor

from handlers import Handlers

logging.basicConfig(level=logging.INFO)

# API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
API_TOKEN = '1202070076:AAHCDBf0bIm4A9xmqRKf5726Ux9EKS0gYok'
# ACCESS_ID = os.getenv("TELEGRAM_ACCESS_ID")
ACCESS_ID = '545679284'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
handler = Handlers(dp, bot)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

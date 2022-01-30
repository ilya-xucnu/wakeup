
import logging
from aiogram import Bot, Dispatcher, executor, types
from config import bot_api_token
import subprocess
logging.basicConfig(level=logging.INFO)

bot = Bot(token=bot_api_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=['callme'])
async def callme(message: types.Message):
    await message.reply(message["from"].username)
    subprocess.call(["python", "call.py", message['from'].username])

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

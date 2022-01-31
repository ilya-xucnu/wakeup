
import logging
from aiogram import Bot, Dispatcher, executor, types
from config import bot_api_token, admins_list, valid_targets
import subprocess
logging.basicConfig(level=logging.INFO)

bot = Bot(token=bot_api_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=['callme'])
async def callme(message: types.Message):
    await message.reply(message["from"].username)
    subprocess.call(["python", "call.py", message['from'].username])

@dp.message_handler()
async def once(message: types.Message):
    text = message.text.split()
    if text[0] == "@wakeup2bot" and text[1] == "once":
        if message["from"].username in admins_list:
            if text[2] in valid_targets:
                await message.reply(f"try call to {text[2]}")
                subprocess.call(["python", "call.py", text[2]])
            else:
                await message.reply("Hell knows who it is. I will not call. Ping @xucnu")
        else:
            await message.reply(f"I don't know you. Submit your id and username to @xucnu. Perhaps he will confirm your rights. ({message['from'].username}, {message['from'].id})")



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

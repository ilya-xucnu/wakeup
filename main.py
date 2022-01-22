from pyrogram import Client, filters
from call import call_user
from config import bot_api_token

app = Client(
    "wakeup2bot",
    bot_token=bot_api_token
)


@app.on_message(filters.command("callme"))
def callback(client, message):
    call_user(message.from_user.username)

app.run()

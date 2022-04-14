from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message
from dotenv import load_dotenv
import os
import re
import requests
from bs4 import BeautifulSoup

load_dotenv()

TOKEN = os.getenv('TOKEN')

bot = Bot(TOKEN)
dp = Dispatcher(bot)

static = 'https://www.y2mate.com/ru/youtube/'

@dp.message_handler(commands=['start'])
async def command_start(message: Message):
    chat_id = message.chat.id
    if message.text == '/start':
        await bot.send_message(chat_id, 'Привет, я бот для скачивания видео с ютуба.')
        await start_message(message)


async def start_message(message: Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id, 'Отправьте ссылку на видео.')


@dp.message_handler(content_types=['text'])
async def trying_to_get_link(message: Message):
    link = message.text
    chat_id = message.chat.id
    try:
        true_link = re.findall(r'((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube(-nocookie)?\.com|youtu.be))(\/(?:['
                r'\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$', link)
        true_static = static + true_link[0][5]
        await bot.send_message(chat_id, f'Ваша ссылка скачивание: {true_static}')
    except:
        await bot.send_message(chat_id, 'Скидывай нормальную ссылку')
    finally:
        await start_message(message)


executor.start_polling(dp, skip_updates=True)

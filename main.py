from random import randrange

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from config import TOKEN

bot = Bot(TOKEN)
dp = Dispatcher(bot)

kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(
    KeyboardButton('/help')).insert(
        KeyboardButton('/description')).add(
            KeyboardButton('❤️')).add(
                KeyboardButton('/orange')).add(
                    KeyboardButton('/random'))

HELP_COMMAND = """
<b>/help</b> - <em>список команд</em>
<b>/start</b> - <em>старт бота</em>
<b>/description</b> - <em>описание бота</em>
<b>/photo</b> - <em>отправка нашего фото</em>
"""


@dp.message_handler(commands=['start'])
async def send_start(message: types.Message):
    await bot.send_message(
        chat_id=message.from_user.id,
        text='Добро пожаловать!',
        reply_markup=kb
    )


@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await bot.send_message(
        chat_id=message.from_user.id,
        text=HELP_COMMAND,
        parse_mode='HTML',
    )


@dp.message_handler(commands=['description'])
async def send_description(message: types.Message):
    await bot.send_message(
        chat_id=message.from_user.id,
        text='Наш бот просто прикольный!',
    )


@dp.message_handler(commands=['orange'])
async def send_orange(message: types.Message):
    await bot.send_photo(
        chat_id=message.chat.id,
        photo="https://www.santosfood.com/wp-content/uploads/2020/01/img-7-500x372.jpg"
    )


@dp.message_handler(commands=['random'])
async def send_random(message: types.Message):
    await bot.send_location(
        chat_id=message.chat.id,
        latitude=randrange(1, 100),
        longitude=randrange(1, 100),
    )


@dp.message_handler()
async def send_kitty(message: types.Message):
    if message.text == '❤️':
        await bot.send_sticker(
            chat_id=message.from_user.id,
            sticker='CAACAgIAAxkBAAEGKvVjU9sbxZVJdXT4EP0tQsBvDWh-gwACURIAAnnTMUsazYOb0eFm1ioE'
        )


async def on_startup(_):
    print('Bot started.')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

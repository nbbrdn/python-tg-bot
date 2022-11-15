import random

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text

from config import TOKEN
from keyboards import kb, kb_photo

HELP_COMMAND = """
<b>/help</b> - <em>список команд</em>
<b>/start</b> - <em>запуск бота</em>
<b>/description</b> - <em>описание бота</em>
"""

arr_photos = [
    'https://tlgrm.ru/_/stickers/c4a/4ce/c4a4ce46-dc17-3777-be23-d29ebbd4e25c/1.jpg',
    'https://tlgrmx.ru/stickers/156/11.png',
    'https://i.pinimg.com/564x/f8/93/dc/f893dc70557f133a6dcd84d9e23c4b33.jpg',
]

bot = Bot(TOKEN)
dp = Dispatcher(bot)


async def on_startup(_):
    print('I have been started.')


@dp.message_handler(Text(equals='Random photo'))
async def open_kb_photo(message: types.Message):
    await message.answer(
        text='Чтобы отправить рандомную фотографию - нажми на кнопку "Рандом"',
        reply_markup=kb_photo
    )
    await message.delete()


@dp.message_handler(Text(equals='Рандом'))
async def send_random_photo(message: types.Message):
    await bot.send_photo(chat_id=message.chat.id, photo=random.choice(arr_photos))


@dp.message_handler(Text(equals='Главное меню'))
async def open_kb(message: types.Message):
    await message.answer(
        text='Добро пожаловать в главное меню!',
        reply_markup=kb
    )
    await message.delete()


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer(text='Добро пожаловать! 🐝', reply_markup=kb)
    await message.delete()


@dp.message_handler(commands=['help'])
async def cmd_help(message: types.Message):
    await message.answer(text=HELP_COMMAND, parse_mode='HTML')
    await message.delete()


@dp.message_handler(commands=['description'])
async def cmd_description(message: types.Message):
    await message.answer(text='Наш бот умеет отправлять рандомные фотки.')
    await bot.send_sticker(
        chat_id=message.chat.id,
        sticker='CAACAgIAAxkBAAEGaqFjcjrNjuFhJ9yvX3AV4y4kOjN_TgACSwAD4FP5CycQs-qvf8GBKwQ'
    )
    await message.delete()


if __name__ == '__main__':
    executor.start_polling(
        dispatcher=dp,
        skip_updates=True,
        on_startup=on_startup
    )

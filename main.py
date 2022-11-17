import random

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove

from config import TOKEN
from keyboards import kb, kb_photo, ikb

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
photos = dict(zip(arr_photos, ['angry', 'hungry', 'funny']))
random_photo = random.choice(list(photos.keys()))

flag = False

bot = Bot(TOKEN)
dp = Dispatcher(bot)


async def on_startup(_):
    print('I have been started.')


async def send_random(message: types.message):
    global random_photo
    random_photo = random.choice(list(photos.keys()))
    await bot.send_photo(chat_id=message.chat.id,
                         photo=random_photo,
                         caption=photos[random_photo],
                         reply_markup=ikb)


@dp.message_handler(Text(equals='Random photo'))
async def open_kb_photo(message: types.Message):
    await message.answer(text='Рандомная фотка!',
                         reply_markup=ReplyKeyboardRemove())
    await send_random(message)
    await message.delete()


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


@dp.callback_query_handler()
async def calback_random_photo(calback: types.CallbackQuery):
    global random_photo  # ! нежелательно использование глобальных переменных
    global flag

    if calback.data == 'like':
        if not flag:
            await calback.answer('Вам понравилось!')
            flag = not flag
        else:
            await calback.answer('Вы уже лайкнули!')
        # await calback.message.answer('Вам понравилось!')
    elif calback.data == 'dislike':
        await calback.answer('Вам не понравилось!')
        # await calback.message.answer('Вам не понравилось!')
    elif calback.data == 'main':
        await calback.message.answer(text='Добро пожаловать в главное меню!',
                                     reply_markup=kb)
        await calback.message.delete()
        await calback.answer()
    else:
        random_photo = random.choice(
            list(filter(lambda x: x != random_photo, list(photos.keys()))))
        await calback.message.edit_media(
            types.InputMedia(media=random_photo, type='photo',
                             caption=photos[random_photo]),
            reply_markup=ikb)
        await calback.answer()


if __name__ == '__main__':
    executor.start_polling(
        dispatcher=dp,
        skip_updates=True,
        on_startup=on_startup
    )

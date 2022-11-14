from aiogram import Bot, Dispatcher, executor, types

from config import TOKEN
from keyboards import kb

HELP_COMMAND = """
<b>/help</b> - <em>список команд</em>
<b>/start</b> - <em>запуск бота</em>
<b>/description</b> - <em>описание бота</em>
"""

bot = Bot(TOKEN)
dp = Dispatcher(bot)


async def on_startup(_):
    print('I have been started.')


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

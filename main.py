from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from config import TOKEN

bot = Bot(TOKEN)
dp = Dispatcher(bot)

kb = ReplyKeyboardMarkup(
    resize_keyboard=True,
)

btn_help = KeyboardButton('/help')
btn_start = KeyboardButton('/start')
btn_description = KeyboardButton('/description')

kb.add(btn_start).insert(btn_help).add(btn_description)

HELP_COMMAND = '''
<b>/help</b> - <em>список команд</em>
<b>/start</b> - <em>старт бота</em>
'''


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await bot.send_message(
        chat_id=message.from_user.id,
        text=HELP_COMMAND,
        parse_mode='HTML',
        reply_markup=ReplyKeyboardRemove(),
    )


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await bot.send_message(
        chat_id=message.from_user.id,
        text='Добро пожаловать в наш бот!',
        parse_mode='HTML',
        reply_markup=kb,
    )


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(text=message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

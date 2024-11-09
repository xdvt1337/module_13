from gettext import textdomain
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import  FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import  InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = "ключ"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb1 = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton(text="Рассчитать")
button2 = KeyboardButton(text="Информация")
kb1.add(button1, button2)


kb2 = InlineKeyboardMarkup()
b1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
b2 = InlineKeyboardButton(text='Формула расчёта', callback_data='formula')
kb2.add(b1, b2)


@dp.message_handler(commands=["start"])
async def start_message(message):
    await message.answer("Привет, я бот, который поможет твоему здоровью. Введи: Рассчитать норму калорий", reply_markup = kb1)

@dp.message_handler(text="Информация")
async def info_message(message):
    await message.answer("Инфа про бота!")

@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию.', reply_markup=kb2)

@dp.callback_query_handler(text='formula')
async def get_formula(call):
    await call.message.answer('(10 х вес в кг) + (6,25 х рост в см) – (5 х возраст в г) – 161')
    await call.answer()

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.callback_query_handler(text= "calories")
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await call.answer()
    await UserState.age.set()

@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(age = message.text)
    data = await state.get_data()
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state = UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth = message.text)
    data = await state.get_data()
    await message.answer('Введите свой вес в кг:')
    await UserState.weight.set()

@dp.message_handler(state = UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight = message.text)
    data = await state.get_data()
    age = int(data['age'])
    growth = int(data['growth'])
    weight = int(data['weight'])
    calories = 10 * weight + 6.25 * growth - 5 * age - 161
    await message.answer(calories)
    await state.finish()

@dp.message_handler()
async def all_messages(message):
    print("Новое сообщение!")
    await message.answer('Пиши команду /start')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

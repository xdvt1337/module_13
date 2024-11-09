from gettext import textdomain

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import  FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

api = "ключ"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton(text="Рассчитать")
button2 = KeyboardButton(text="Информация")
kb.add(button1)
kb.add(button2)

@dp.message_handler(commands=["start"])
async def start_message(message):
    await message.answer("Привет, я бот, который поможет твоему здоровью. Введи: Рассчитать", reply_markup = kb)

@dp.message_handler(text="Информация")
async def startcommand(message):
    await message.answer('Бот — специальная программа, выполняющая автоматически и/или по заданному расписанию какие-либо действия через интерфейсы, предназначенные для людей.')

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(text= "Рассчитать")
async def set_age(message):
    await message.answer('Введите свой возраст:')
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

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

api = "Ключ"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(text=["Cup", "ff"])
async def cup_message(message):
    print("CUP!")
    await message.answer("Answer cup message")


@dp.message_handler(commands=["start"])
async def start_message(message):
    print("STARTMESSAGE")
    await message.answer("Привет, я бот у которого всего 3 фукции. :(")


@dp.message_handler()
async def all_messages(message):
    print("Новое сообщение!")
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

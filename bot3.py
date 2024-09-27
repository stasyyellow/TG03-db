import sqlite3
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from config import TOKEN

# Создаем объект бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Определение состояний
class Form(StatesGroup):
    name = State()
    age = State()
    grade = State()

# Обработчик команды /start
@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer("Привет! Как тебя зовут?")
    await state.set_state(Form.name)

# Обработка имени пользователя
@dp.message(Form.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Сколько тебе лет?")
    await state.set_state(Form.age)

# Обработка возраста пользователя
@dp.message(Form.age)
async def process_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("В каком ты классе?")
    await state.set_state(Form.grade)

# Обработка класса и сохранение в базу данных
@dp.message(Form.grade)
async def process_grade(message: Message, state: FSMContext):
    await state.update_data(grade=message.text)

    # Получение всех данных пользователя
    user_data = await state.get_data()

    # Подключение к базе данных и сохранение данных
    conn = sqlite3.connect('school_data.db')
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO students (name, age, grade) VALUES (?, ?, ?)
    ''', (user_data['name'], user_data['age'], user_data['grade']))
    conn.commit()
    conn.close()

    await message.answer("Данные успешно сохранены!")
    await state.clear()

# Обработчик команды /help
@dp.message(Command(commands=["help"]))
async def help_command(message: Message):
    await message.answer(
        "Этот бот собирает данные студентов и сохраняет их в базу данных. "
        "Вот что он делает:\n"
        "1. Команда /start запускает сбор информации: имя, возраст и класс.\n"
        "2. Ваши данные сохраняются в базе данных после завершения ввода."
    )

# Функция для запуска бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

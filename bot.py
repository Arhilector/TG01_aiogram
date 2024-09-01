# bot.py

import logging
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from config import TELEGRAM_TOKEN, OPENWEATHER_API_KEY

# Логирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


# Создание клавиатуры
def get_main_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    weather_button = KeyboardButton('Узнать погоду')
    keyboard.add(weather_button)
    return keyboard


# Команда /start
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer(
        "Привет! Я бот, который поможет узнать погоду. Нажми 'Узнать погоду', чтобы начать.",
        reply_markup=get_main_menu()
    )


# Обработка кнопки "Узнать погоду"
@dp.message_handler(lambda message: message.text == 'Узнать погоду')
async def ask_city(message: types.Message):
    await message.answer("Скажи на английском или на русском языке название города, в котором хочешь узнать погоду?")


# Обработка ввода города
@dp.message_handler()
async def send_weather(message: types.Message):
    city = message.text
    weather_info = get_weather(city)
    await message.answer(weather_info)


# Функция для получения погоды
def get_weather(city: str) -> str:
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={OPENWEATHER_API_KEY}&lang=ru'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        description = data['weather'][0]['description']
        return f"Погода в городе {city}:\nТемпература: {temp}°C\nОписание: {description}"
    else:
        return "Не удалось получить данные о погоде. Проверьте правильность написания города."


# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

import os
import telebot
from dotenv import load_dotenv


load_dotenv()
# Инициализация Telegram-бота
TOKEN_BOT = os.getenv('TOKEN_BOT')  # Токен бота из переменной окружения
if not TOKEN_BOT:
    raise ValueError("Токен бота не найден в переменной окружения")
bot = telebot.TeleBot(TOKEN_BOT)

TOKEN_MONGO = os.getenv('URL_MONGO')
if not TOKEN_MONGO:
    raise ValueError("URL MongoDB не найден в переменной окружения")

TOKEN_PAY_MASTER = os.getenv('PAY_MASTER')
if not TOKEN_PAY_MASTER:
    raise ValueError("Токен PayMaster не найден в переменной окружения")
from telebot import types
from handlers.config import bot
def create_inline_back_menu():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    back_menu = types.InlineKeyboardButton("Главное меню", callback_data="main_menu")
    keyboard.add(back_menu)
    return keyboard
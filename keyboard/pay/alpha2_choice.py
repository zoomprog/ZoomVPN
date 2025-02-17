from telebot import types
from handlers.config import bot
def create_inline_alpha2_button_choice():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    ru_button_choice = types.InlineKeyboardButton("Россия", callback_data="ru_ssh_profile")
    fi_button_choice = types.InlineKeyboardButton("Финляндия", callback_data="fi_ssh_profile")
    keyboard.add(ru_button_choice,fi_button_choice)
    return keyboard



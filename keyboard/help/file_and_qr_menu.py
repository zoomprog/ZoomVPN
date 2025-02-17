from telebot import types
from handlers.config import bot
def create_inline_help_connect():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    qr_button_connect = types.InlineKeyboardButton("QR-код", callback_data="qr_connect_help")
    file_button_connect = types.InlineKeyboardButton("Файл", callback_data="file_connect_help")
    back_menu = types.InlineKeyboardButton("Главное меню", callback_data="main_menu")
    keyboard.add(qr_button_connect,file_button_connect)
    keyboard.add(back_menu)
    return keyboard
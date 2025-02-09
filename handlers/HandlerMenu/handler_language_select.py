from handlers.config import bot
from telebot import types
# Функция для обработки выбора языка

def handle_language_selection(call):
    if call.data == "language":
        # Создаем клавиатуру для выбора языка
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("RU", callback_data="ru"))
        markup.add(types.InlineKeyboardButton("EN", callback_data="en"))
        markup.add(types.InlineKeyboardButton("DE", callback_data="de"))
        markup.add(types.InlineKeyboardButton("FR", callback_data="fr"))
        markup.add(types.InlineKeyboardButton("Главное меню", callback_data="main_menu"))
        bot.answer_callback_query(call.id, "Выбрано: Язык")
        bot.send_message(call.message.chat.id, "Выберите язык интерфейса:", reply_markup=markup)

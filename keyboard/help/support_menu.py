from handlers.config import bot
from telebot import types
# Функция для обработки выбора языка

def support_help_menu(call):
    if call.data == "help":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Как подключиться❓", callback_data="help_how_to_connect"))
        markup.add(types.InlineKeyboardButton("Не работает VPN", callback_data="vpn_not_working"))
        markup.add(types.InlineKeyboardButton("Связаться со мной", callback_data="contact_with_me"))
        markup.add(types.InlineKeyboardButton("Главное меню", callback_data="main_menu"))
        bot.answer_callback_query(call.id, "Выбор меню: Помощь")
        bot.send_message(call.message.chat.id, "Выберите в чем проблема:", reply_markup=markup)

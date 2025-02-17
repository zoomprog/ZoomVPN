from handlers.config import bot
from telebot import types
from messages.messages import mess_doesnt_work_vpn


def doesnt_work_vpn(call):

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    main_menu = types.InlineKeyboardButton("Главное меню", callback_data="main_menu")
    keyboard.add(main_menu)
    bot.send_message(
        call.message.chat.id,
        text=mess_doesnt_work_vpn,
        reply_markup=keyboard,
        parse_mode='Markdown'
    )
import telebot

# Создание инлайн-клавиатуры
def create_inline_keyboard():
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)

    buy_extend = telebot.types.InlineKeyboardButton("🛒 Купить/Продлить", callback_data="buy_extend")
    active_keys = telebot.types.InlineKeyboardButton("ℹ️ Профиль", callback_data="active_keys")
    help_button = telebot.types.InlineKeyboardButton("❓ Помощь", callback_data="help")
    change_location = telebot.types.InlineKeyboardButton("🌍 Изменить локацию", callback_data="change_location")
    donate = telebot.types.InlineKeyboardButton("❤️ Пожертвовать", callback_data="donate")
    about_vpn = telebot.types.InlineKeyboardButton("📚 Всё о ZoomVPN", callback_data="about_vpn")


    # Добавляем кнопки в клавиатуру
    keyboard.add(
        buy_extend, active_keys,change_location,help_button,
         donate, about_vpn
    )

    return keyboard
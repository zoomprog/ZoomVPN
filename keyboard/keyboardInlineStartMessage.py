import telebot

# Создание инлайн-клавиатуры
def create_inline_keyboard():
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)

    buy_extend = telebot.types.InlineKeyboardButton("🛒 Купить/Продлить", callback_data="buy_extend")
    help_button = telebot.types.InlineKeyboardButton("❓ Помощь", callback_data="help")
    active_keys = telebot.types.InlineKeyboardButton("🔑 Мои активные ключи", callback_data="active_keys")
    change_location = telebot.types.InlineKeyboardButton("🌍 Изменить локацию", callback_data="change_location")
    change_protocol = telebot.types.InlineKeyboardButton("⚙️ Изменить протокол", callback_data="change_protocol")
    donate = telebot.types.InlineKeyboardButton("❤️ Пожертвовать", callback_data="donate")
    about_vpn = telebot.types.InlineKeyboardButton("📚 Всё о ZoomVPN", callback_data="about_vpn")
    invite = telebot.types.InlineKeyboardButton("👥 Пригласить", callback_data="invite")
    language = telebot.types.InlineKeyboardButton("🌐 Язык", callback_data="language")
    partnership = telebot.types.InlineKeyboardButton("💼 Партнерская программа", callback_data="partnership")

    # Добавляем кнопки в клавиатуру
    keyboard.add(
        buy_extend, help_button, active_keys, change_location,
        change_protocol, donate, about_vpn, invite, language, partnership
    )

    return keyboard
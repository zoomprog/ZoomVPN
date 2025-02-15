from handlers.config import bot
from keyboard.keyboardInlineStartMessage import create_inline_keyboard


def main_menu(call):
    username = call.from_user.first_name or "Пользователь"
    text = (
        f"👋 Привет, {username}!\n\n"
        "💻 Добро пожаловать в ZoomVPN!:\n"
        "🚫 Никаких ограничений скорости — полная свобода в интернете на максимальной скорости.\n"
        "🌍 Доступ ко всем сайтам — никаких блокировок, где бы вы ни находились.\n"
        "🔒 Конфиденциальность и безопасность — шифрование данных на уровне банковских стандартов.\n"
        "⚙️ Быстрое подключение — легко настроить за 1 минуту на iPhone, Android, ПК и macOS.\n"
        "💳 Оплата картами РФ 🇷🇺 и СБП — просто и удобно.\n"
        "💵 Всего 199₽ в месяц — без скрытых платежей и рекламы.\n\n"
        "🚀 Начните прямо сейчас!"
    )
    keyboard = create_inline_keyboard()  # Создание клавиатуры
    bot.send_message(
        call.message.chat.id,
        text,
        reply_markup=keyboard,
        parse_mode='Markdown'
    )
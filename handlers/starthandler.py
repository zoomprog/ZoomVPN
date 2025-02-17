from handlers.config import bot
from database.mongoDB import coll
from keyboard.vpn_menu.main_menu import create_inline_keyboard
@bot.message_handler(commands=['start','menu'])
def start(message):
    try:
        # Получаем Telegram ID пользователя и его имя
        telegram_id = message.from_user.id
        username = message.from_user.first_name or "Пользователь"

        # Текст приветствия (общий для всех)
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

        # Проверяем, существует ли уже пользователь в базе данных
        user = coll.find_one({"telegram_id": telegram_id})
        if not user:
            # Если пользователь новый, регистрируем его
            new_user = {
                "telegram_id": telegram_id,
                "subscription_status": "нет подписки",
                "subscription_expiry_date": None
            }
            coll.insert_one(new_user)

        # Создаем инлайн-клавиатуру
        keyboard = create_inline_keyboard()

        # Отправляем сообщение с инлайн-кнопками
        bot.send_message(
            message.chat.id,
            text,
            reply_markup=keyboard,
            parse_mode='Markdown'
        )

    except Exception as e:
        bot.send_message(
            message.chat.id,
            "❌ Произошла ошибка при регистрации. Попробуйте позже."
        )
        print(f"Ошибка при обработке /start: {e}")
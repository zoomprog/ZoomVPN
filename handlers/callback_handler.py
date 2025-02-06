from handlers.config import bot
from handlers.HandlerMenu.handler_language_select import handle_language_selection
from handlers.HandlerMenu.handler_help import handle_halp
from keyboard.keyboardInlineStartMessage import create_inline_keyboard
from telebot import types
from handlers.config import TOKEN_PAY_MASTER
import logging

# Настройка логирования для отладки
logging.basicConfig(level=logging.INFO)


# Вспомогательная функция для обработки общих действий
def process_callback(call, message_text, answer_text=None, parse_mode=None):
    if answer_text:
        bot.answer_callback_query(call.id, answer_text)
    bot.send_message(call.message.chat.id, message_text, parse_mode=parse_mode)


# Обработчик нажатий инлайн-кнопок
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    try:
        if call.data == "buy_extend":
            # Создаем клавиатуру с вариантами подписки
            subscription_keyboard = types.InlineKeyboardMarkup()

            # Добавляем кнопки для разных вариантов подписки
            one_month_button = types.InlineKeyboardButton("1 месяц - 199₽", callback_data="subscribe_1")
            two_months_button = types.InlineKeyboardButton("2 месяца - 399₽", callback_data="subscribe_2")
            three_months_button = types.InlineKeyboardButton("3 месяца - 569₽ (-5%)", callback_data="subscribe_3")
            six_months_button = types.InlineKeyboardButton("6 месяцев - 960₽ (-20%)", callback_data="subscribe_6")
            twelve_months_button = types.InlineKeyboardButton("12 месяцев - 1560₽ (-35%)", callback_data="subscribe_12")

            subscription_keyboard.row(one_month_button, two_months_button)
            subscription_keyboard.row(three_months_button, six_months_button)
            subscription_keyboard.row(twelve_months_button)

            # Отправляем сообщение с клавиатурой
            bot.send_message(
                call.message.chat.id,
                "Выберите вариант подписки:",
                reply_markup=subscription_keyboard
            )

        elif call.data.startswith("subscribe_"):
            # Определяем выбранный срок подписки
            subscription_period = call.data.split("_")[1]

            # Создаем словарь с ценами для разных периодов
            subscription_prices = {
                "1": {"label": "Подписка на 1 месяц", "amount": 199},
                "2": {"label": "Подписка на 2 месяца", "amount": 399},
                "3": {"label": "Подписка на 3 месяца -5% скидка", "amount": 569},
                "6": {"label": "Подписка на 6 месяцев -20% скидка", "amount": 960},
                "12": {"label": "Подписка на 12 месяцев -35% скидка", "amount": 1560},
            }

            if subscription_period in subscription_prices:
                # Получаем данные о выбранной подписке
                price_info = subscription_prices[subscription_period]
                label = price_info["label"]
                amount = price_info["amount"]

                # Отправляем инвойс для оплаты
                bot.send_invoice(
                    chat_id=call.message.chat.id,
                    title=label,
                    description=f"Оплата {label}",
                    provider_token=TOKEN_PAY_MASTER,  # Убедитесь, что это тестовый токен
                    currency='RUB',
                    prices=[types.LabeledPrice(label=label, amount=amount * 100)],  # Сумма в копейках
                    start_parameter='test-invoice-payload',
                    invoice_payload=f'subscription_{subscription_period}'
                )
            else:
                process_callback(call, "Неизвестный вариант подписки.", "Ошибка: Неизвестный вариант")

        elif call.data == "help":
            handle_halp(call)  # Вызов функции помощи

        elif call.data == "active_keys":
            process_callback(call, "Вы выбрали опцию 'Мои активные ключи'.", "Выбрано: Мои активные ключи")

        elif call.data == "change_location":
            process_callback(call, "Вы выбрали опцию 'Изменить локацию'.", "Выбрано: Изменить локацию")

        elif call.data == "change_protocol":
            process_callback(call, "Вы выбрали опцию 'Изменить протокол'.", "Выбрано: Изменить протокол")

        elif call.data == "donate":
            process_callback(call, "Вы выбрали опцию 'Пожертвовать'.", "Выбрано: Пожертвовать")

        elif call.data == "about_vpn":
            process_callback(call, "Вы выбрали опцию 'Всё о ZoomVPN'.", "Выбрано: Всё о ZoomVPN")

        elif call.data == "invite":
            process_callback(call, "Вы выбрали опцию 'Пригласить'.", "Выбрано: Пригласить")

        elif call.data == "language":
            handle_language_selection(call)  # Вызов функции выбора языка

        elif call.data == "partnership":
            process_callback(call, "Вы выбрали опцию 'Партнерская программа'.", "Выбрано: Партнерская программа")

        elif call.data == "main_menu":  # Проверяем "Главное меню" до языков
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

        elif call.data in ["ru", "en", "de", "fr"]:  # Языки проверяем после "Главное меню"
            language_mapping = {
                "ru": "русский",
                "en": "английский",
                "de": "немецкий",
                "fr": "французский"
            }
            selected_language = language_mapping.get(call.data)
            if selected_language:
                process_callback(
                    call,
                    f"Ты выбрал {selected_language} язык! В разработке!",
                    f"Вы выбрали: {selected_language} язык",
                    parse_mode='HTML'
                )
            else:
                process_callback(call, "Выбранный язык не поддерживается.", "Неизвестный язык")

        else:
            process_callback(call, "Неизвестная команда. Пожалуйста, выберите одну из доступных опций.",
                             "Неизвестная команда")

    except Exception as e:
        bot.send_message(call.message.chat.id, f"Произошла ошибка: {e}")
        logging.error(f"Error in callback handler: {e}")


# Обработка pre_checkout_query (подтверждение оплаты)
@bot.pre_checkout_query_handler(func=lambda query: True)
def process_pre_checkout_query(pre_checkout_query):
    logging.info(f"Pre-checkout query received: {pre_checkout_query}")
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


# Обработка успешной оплаты
@bot.message_handler(content_types=['successful_payment'])
def process_successful_payment(message):
    logging.info(f"Successful payment received: {message.successful_payment}")
    bot.send_message(message.chat.id, "Спасибо за оплату! Ваша подписка активирована.")
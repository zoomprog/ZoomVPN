from handlers.config import bot
from telebot import types
from handlers.callback_action_handler import process_callback
from handlers.config import TOKEN_PAY_MASTER
def keyboard_inline_buy(call):
    # Создаем клавиатуру с вариантами подписки
    subscription_keyboard = types.InlineKeyboardMarkup()

    # Добавляем кнопки для разных вариантов подписки
    one_month_button = types.InlineKeyboardButton("1 месяц - 199₽", callback_data="subscribe_1")
    two_months_button = types.InlineKeyboardButton("2 месяца - 399₽", callback_data="subscribe_2")
    three_months_button = types.InlineKeyboardButton("3 месяца - 569₽ (-5%)", callback_data="subscribe_3")
    four_months_button = types.InlineKeyboardButton("4 месяца - 720₽ (-10%)", callback_data="subscribe_4")
    five_months_button = types.InlineKeyboardButton("5 месяцев - 900₽ (-15%)", callback_data="subscribe_5")
    six_months_button = types.InlineKeyboardButton("6 месяцев - 960₽ (-20%)", callback_data="subscribe_6")
    seven_months_button = types.InlineKeyboardButton("7 месяцев - 1120 (-25%)", callback_data="subscribe_7")
    eight_months_button = types.InlineKeyboardButton("8 месяцев - 1200 (-30%)", callback_data="subscribe_8")
    nine_months_button = types.InlineKeyboardButton("9 месяцев - 1350₽ (-35%)", callback_data="subscribe_9")
    ten_months_button = types.InlineKeyboardButton("10 месяцев - 1400₽ (-40%)", callback_data="subscribe_10")
    eleven_months_button = types.InlineKeyboardButton("11 месяцев - 1540₽ (-45%)", callback_data="subscribe_11")
    twelve_months_button = types.InlineKeyboardButton("12 месяцев - 1560₽ (-35%)", callback_data="subscribe_12")

    subscription_keyboard.row(one_month_button)
    subscription_keyboard.row(two_months_button)
    subscription_keyboard.row(three_months_button)
    subscription_keyboard.row(four_months_button)
    subscription_keyboard.row(five_months_button)
    subscription_keyboard.row(six_months_button)
    subscription_keyboard.row(seven_months_button)
    subscription_keyboard.row(eight_months_button)
    subscription_keyboard.row(nine_months_button)
    subscription_keyboard.row(ten_months_button)
    subscription_keyboard.row(eleven_months_button)
    subscription_keyboard.row(twelve_months_button)

    # Отправляем сообщение с клавиатурой
    bot.send_message(
        call.message.chat.id,
        "Выберите вариант подписки:",
        reply_markup=subscription_keyboard
    )

def keyboard_inline_payment(call):
    # Определяем выбранный срок подписки
    subscription_period = call.data.split("_")[1]

    # Создаем словарь с ценами для разных периодов
    subscription_prices = {
        "1": {"label": "Подписка на 1 месяц", "amount": 199},
        "2": {"label": "Подписка на 2 месяца", "amount": 399},
        "3": {"label": "Подписка на 3 месяца -5% скидка", "amount": 569},
        "4": {"label": "Подписка на 4 месяца - 10% скидка", "amount": 720},
        "5": {"label": "Подписка на 5 месяцев - 10% скидка", "amount": 900},
        "6": {"label": "Подписка на 6 месяцев -20% скидка", "amount": 960},
        "7": {"label": "Подписка на 7 месяцев -20% скидка", "amount": 1120},
        "8": {"label": "Подписка на 8 месяцев - 25% скидка", "amount": 1200},
        "9": {"label": "Подписка на 9 месяцев - 25% скидка", "amount": 1350},
        "10": {"label": "Подписка на 10 месяцев -30% скидка", "amount": 1400},
        "11": {"label": "Подписка на 11 месяцев -30% скидка", "amount": 1540},
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

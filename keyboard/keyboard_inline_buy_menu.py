from handlers.config import bot
from telebot import types
from handlers.callback_action_handler import process_callback
from handlers.config import TOKEN_PAY_MASTER
def keyboard_inline_buy(call):
    # Создаем клавиатуру с вариантами подписки
    subscription_keyboard = types.InlineKeyboardMarkup()

    # Добавляем кнопки для разных вариантов подписки
    one_month_button = types.InlineKeyboardButton("1 месяц - 199₽", callback_data="subscribe_1")
    three_months_button = types.InlineKeyboardButton("3 месяца - 569₽ (-5%)", callback_data="subscribe_3")
    six_months_button = types.InlineKeyboardButton("6 месяцев - 1020₽ (-15%)", callback_data="subscribe_6")
    nine_months_button = types.InlineKeyboardButton("9 месяцев - 1350₽ (-25%)", callback_data="subscribe_9")
    twelve_months_button = types.InlineKeyboardButton("12 месяцев - 1560₽ (-35%)", callback_data="subscribe_12")


    subscription_keyboard.row(one_month_button)
    subscription_keyboard.row(three_months_button)
    subscription_keyboard.row(six_months_button)
    subscription_keyboard.row(nine_months_button)
    subscription_keyboard.row(twelve_months_button)
    subscription_keyboard.add(types.InlineKeyboardButton("Главное меню", callback_data="main_menu"))

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
        "3": {"label": "Подписка на 3 месяца -5% скидка", "amount": 569},
        "6": {"label": "Подписка на 6 месяцев -15% скидка", "amount": 1020},
        "9": {"label": "Подписка на 6 месяцев -25% скидка", "amount": 1350},
        "12": {"label": "Подписка на 12 месяцев -35% скидка", "amount": 1560}
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

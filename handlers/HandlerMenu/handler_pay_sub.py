import telebot
from telebot.types import LabeledPrice, ShippingOption
from handlers.config import bot
from handlers.config import TOKEN_PAY_MASTER

PRICES = [
    LabeledPrice(label='Подписка на 1 месяц', amount=199),
    LabeledPrice(label='Подписка на 2 месяца', amount=399),
    LabeledPrice(label='Подписка на 3 месяца -5% скидка', amount=569),
    LabeledPrice(label='Подписка на 4 месяца - 10% скидка', amount=720),
    LabeledPrice(label='Подписка на 5 месяцев - 10% скидка', amount=900),
    LabeledPrice(label='Подписка на 6 месяцев -20% скидка', amount=960),
    LabeledPrice(label='Подписка на 7 месяцев -20% скидка', amount=1120),
    LabeledPrice(label='Подписка на 8 месяца -25% скидка', amount=1200),
    LabeledPrice(label='Подписка на 9 месяцев -25% скидка', amount=1350),
    LabeledPrice(label='Подписка на 10 месяцев -30% скидка', amount=1400),
    LabeledPrice(label='Подписка на 11 месяцев -30% скидка', amount=1540),
    LabeledPrice(label='Подписка на 12 месяцев -35% скидка', amount=1560),
]

@bot.message_handler(commands=['subscribe'])
def send_invoice(message):
    chat_id = message.chat.id
    title = "Подписка на сервис"
    description = "Выберите подходящий вариант подписки"

    # Отправляем инвойс
    bot.send_invoice(
        chat_id=chat_id,
        title=title,
        description=description,
        provider_token=TOKEN_PAY_MASTER,
        currency='RUB',
        prices=PRICES,
        start_parameter='test-invoice-payload',
        invoice_payload='custom-invoice-payload'
    )
# Обработка pre_checkout_query (подтверждение оплаты)
@bot.pre_checkout_query_handler(func=lambda query: True)
def process_pre_checkout_query(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

# Обработка успешной оплаты
@bot.message_handler(content_types=['successful_payment'])
def process_successful_payment(message):
    bot.send_message(message.chat.id, "Спасибо за оплату! Ваша подписка активирована.")

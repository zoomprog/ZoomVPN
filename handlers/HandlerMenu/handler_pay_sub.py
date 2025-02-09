from handlers.config import bot
from database.mongoDB import coll
from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging


@bot.pre_checkout_query_handler(func=lambda query: True)
def process_pre_checkout_query(pre_checkout_query):
    logging.info(f"Pre-checkout query received: {pre_checkout_query}")
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


# Обработка успешной оплаты
@bot.message_handler(content_types=['successful_payment'])
def process_successful_payment(message):
    logging.info(f"Successful payment received: {message.successful_payment}")

    # Получаем invoice_payload из successful_payment
    payload = message.successful_payment.invoice_payload
    subscription_period = payload.split("_")[1]  # Например, "subscribe_1" -> "1"

    # Словарь для расчета количества месяцев
    subscription_periods = {
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "7": 7,
        "8": 8,
        "9": 9,
        "10": 10,
        "11": 11,
        "12": 12
    }

    if subscription_period not in subscription_periods:
        bot.send_message(message.chat.id, "Произошла ошибка при оформлении подписки.")
        return

    # Количество месяцев новой подписки
    months = subscription_periods[subscription_period]

    # Telegram ID пользователя
    user_id = message.chat.id

    # Проверяем, существует ли пользователь в базе данных
    user_data = coll.find_one({"telegram_id": user_id})

    if user_data and "subscription_expiry_date" in user_data and user_data["subscription_expiry_date"] is not None:
        # Если пользователь уже имеет активную подписку, добавляем месяцы к текущей дате окончания
        current_expiry_date = user_data["subscription_expiry_date"]
        new_expiry_date = current_expiry_date + relativedelta(months=months)

        # Суммируем общее количество месяцев подписки
        total_months = user_data.get("subscription_months", 0) + months

        # Обновляем данные подписки в базе данных
        coll.update_one(
            {"telegram_id": user_id},
            {
                "$set": {
                    "subscription_status": "активна",
                    "subscription_expiry_date": new_expiry_date,
                    "subscription_months": total_months
                }
            }
        )
        logging.info(
            f"Updated subscription for user {user_id}. New end date: {new_expiry_date}, Total months: {total_months}")
    else:
        # Если пользователя нет или у него нет активной подписки, создаем новую подписку
        current_date = datetime.now()
        new_expiry_date = current_date + relativedelta(months=months)

        # Создаем или обновляем документ пользователя
        coll.update_one(
            {"telegram_id": user_id},
            {
                "$set": {
                    "subscription_status": "активна",
                    "subscription_expiry_date": new_expiry_date,
                    "subscription_months": months
                }
            },
            upsert=True
        )
        logging.info(
            f"Created or updated subscription for user {user_id}. End date: {new_expiry_date}, Months: {months}")

    # Отправляем сообщение пользователю
    bot.send_message(
        message.chat.id,
        f"Новая дата окончания подписки: {new_expiry_date.strftime('%d.%m.%Y')}"
    )
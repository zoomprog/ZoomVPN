from handlers.config import bot
from database.mongoDB import coll
from database.mongo_connect_ssh import ssh
from datetime import datetime
from dateutil.relativedelta import relativedelta
from keyboard.keyboard_inline_alpha2_choice import create_inline_alpha2_button_choice
import logging


@bot.pre_checkout_query_handler(func=lambda query: True)
def process_pre_checkout_query(pre_checkout_query):
    logging.info(f"Pre-checkout query received: {pre_checkout_query}")
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


# Обработка успешной оплаты
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
        "3": 3,
        "6": 6,
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
        total_months = user_data.get("subscription_months", 0)

        # Проверяем, не превышает ли общее количество месяцев 12
        if total_months >= 12:
            bot.send_message(
                message.chat.id,
                "Вы уже достигли максимального срока подписки (12 месяцев). Дополнительные покупки недоступны."
            )
            return

        # Вычисляем новую дату окончания подписки
        new_expiry_date = current_expiry_date + relativedelta(months=months)
        total_months += months

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
            f"Updated subscription for user {user_id}. New end date: {new_expiry_date}, Total months: {total_months}"
        )
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
            f"Created or updated subscription for user {user_id}. End date: {new_expiry_date}, Months: {months}"
        )

    # Отправляем сообщение пользователю
    bot.send_message(
        message.chat.id,
        f"Новая дата окончания подписки: {new_expiry_date.strftime('%d.%m.%Y')}"
    )

    # Отправляем клавиатуру для выбора страны
    bot.send_message(
        message.chat.id,
        "Выберите страну для подключения Zoom VPN:",
        reply_markup=create_inline_alpha2_button_choice()
    )


# Обработка выбора страны
# Обработка выбора страны
@bot.callback_query_handler(func=lambda call: call.data in ["ru_ssh_profile", "fi_ssh_profile"])
def handle_country_selection(call):
    user_id = call.from_user.id
    selected_profile = call.data  # ru_ssh_profile или fi_ssh_profile

    # Сохраняем выбранный профиль SSH в базе данных
    coll.update_one(
        {"telegram_id": user_id},
        {"$set": {"ssh_alpha2": selected_profile}},  # Добавляем значение в массив ssh_alpha2
        upsert=True
    )

    amount_users = ssh.find_one({"alpha2": selected_profile})
    if amount_users:
        # Проверка, что amount_users <= 5
        if amount_users.get("amount_users", 0) <= 5:
            ssh.update_one(
                {"alpha2": selected_profile},
                {"$inc": {"amount_users": 1}},  # Увеличиваем значение в количестве пользователей
                upsert=True
            )
        else:
            # Если количество пользователей больше 5, отправляем сообщение и возвращаем к выбору сервера
            bot.send_message(
                call.message.chat.id,
                "На данный сервер достигнуто максимальное количество пользователей. Пожалуйста, выберите другой сервер.",
                reply_markup=create_inline_alpha2_button_choice()
            )
            return  # Прерываем выполнение функции, чтобы не продолжать дальше
    else:
        print("Документ с alpha2 == 'ru_ssh_profile' не найден")

    # Определяем название страны для ответа пользователю
    country_name = "Россия" if selected_profile == "ru_ssh_profile" else "Финляндия"

    # Подтверждаем выбор пользователя
    bot.edit_message_text(
        f"Вы выбрали сервер в {country_name}.",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id
    )

    # Логирование выбора страны
    logging.info(f"User {user_id} selected SSH profile: {selected_profile}")
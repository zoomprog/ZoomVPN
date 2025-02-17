from database.mongoDB import coll  # Импортируем коллекцию MongoDB
from handlers.config import bot  # Импортируем Telegram-бота
from keyboard.profile.information_profile import inline_keyboard_profile_qr_or_file



def handler_profile_user(call):
    user_id = call.from_user.id  # Получаем ID пользователя из CallbackQuery
    user = coll.find_one({"telegram_id": user_id})  # Находим пользователя в базе данных

    if user:
        # Извлекаем данные из документа
        subscription_status = user.get("subscription_status", "Неактивна")
        subscription_expiry_date = user.get("subscription_expiry_date", None)
        subscription_months = user.get("subscription_months", 0)

        if subscription_status == "активна" and subscription_expiry_date:
            # Преобразуем дату окончания подписки в читаемый формат
            expiry_date_formatted = subscription_expiry_date.strftime("%d.%m.%Y")

            # Формируем сообщение
            mess_profile_vpn_user = f"""
🚨 ЛИЧНЫЙ КАБИНЕТ VPN 🚨
🌟 У вас активна подписка на VPN сервис!
⏳ Срок действия: {subscription_months} месяцев
📅 Дата окончания подписки: {expiry_date_formatted}
🔒 Настройте безопасное подключение уже сегодня!
🌐 Доступ к глобальной сети без ограничений
🛡️ 100% защита ваших данных
❗️ Не забудьте продлить подписку до указанной даты для непрерывного использования сервиса
                """
            # Отправляем сообщение пользователю
            bot.send_message(
                call.message.chat.id,
                text=mess_profile_vpn_user,
                reply_markup=inline_keyboard_profile_qr_or_file(call),
                parse_mode='Markdown'
            )
        else:
            # Если подписка неактивна
            bot.send_message(call.message.chat.id, "⚠️ Ваша подписка на VPN неактивна. Приобретите подписку для доступа к сервису.")
    else:
        # Если пользователь не найден
        bot.send_message(call.message.chat.id, "❌ Пользователь не найден в системе.")
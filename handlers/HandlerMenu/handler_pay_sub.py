# from telebot.apihelper import send_message
# from handlers.config import bot
# from database.mongoDB import coll
# from database.mongo_connect_ssh import ssh
# from database.mongo_config_and_QRCode import config_and_QRCode
# from datetime import datetime
# from dateutil.relativedelta import relativedelta
# from keyboard.pay.alpha2_choice import create_inline_alpha2_button_choice
# import logging
# import os
#
# # Настройка логирования
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
#
# # Обработка запроса на оплату
# @bot.pre_checkout_query_handler(func=lambda query: True)
# def process_pre_checkout_query(pre_checkout_query):
#     logging.info(f"Pre-checkout query received: {pre_checkout_query}")
#     bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
#
# def get_config_name_by_telegram_id(telegram_id):
#     """
#     Возвращает qrcode_name для указанного telegram_id.
#     :param telegram_id: Telegram ID пользователя.
#     :return: Значение qrcode_name или None, если документ не найден.
#     """
#     try:
#         config = config_and_QRCode.find_one({"telegram_id": telegram_id})
#         if config and "config_name" in config:
#             logging.info(f"Found config_name for user {telegram_id}: {config['config_name']}")
#             return config["config_name"]
#         else:
#             logging.warning(f"No config_name found for user {telegram_id}")
#             return None
#     except Exception as e:
#         logging.error(f"Error while fetching config_name for user {telegram_id}: {e}")
#         return None
# # Функция для получения qrcode_name по telegram_id
# def get_qrcode_name_by_telegram_id(telegram_id):
#     """
#     Возвращает qrcode_name для указанного telegram_id.
#     :param telegram_id: Telegram ID пользователя.
#     :return: Значение qrcode_name или None, если документ не найден.
#     """
#     try:
#         config = config_and_QRCode.find_one({"telegram_id": telegram_id})
#         if config and "qrcode_name" in config:
#             logging.info(f"Found qrcode_name for user {telegram_id}: {config['qrcode_name']}")
#             return config["qrcode_name"]
#         else:
#             logging.warning(f"No qrcode_name found for user {telegram_id}")
#             return None
#     except Exception as e:
#         logging.error(f"Error while fetching qrcode_name for user {telegram_id}: {e}")
#         return None
#
# # Функция для добавления telegram_id в Config_and_QRCode
# def add_telegram_id_to_config(selected_profile, user_id):
#     """
#     Добавляет telegram_id пользователя в первый свободный документ в коллекции Config_and_QRCode.
#     Если telegram_id уже существует для данного профиля, ничего не делает.
#     :param selected_profile: Выбранный профиль (например, "ru_ssh_profile").
#     :param user_id: Telegram ID пользователя.
#     :return: True, если удалось добавить или пользователь уже привязан, иначе False.
#     """
#     # Проверяем, существует ли уже запись с этим telegram_id и selected_profile
#     existing_config = config_and_QRCode.find_one({
#         "telegram_id": user_id,
#         "alpha2_name": selected_profile
#     })
#     if existing_config:
#         logging.info(f"Telegram ID {user_id} already exists for alpha2_name {selected_profile}")
#         return True
#
#     # Находим первый свободный документ для выбранного профиля
#     free_config = config_and_QRCode.find_one({
#         "$or": [
#             {"telegram_id": {"$exists": False}},  # Поле отсутствует
#             {"telegram_id": None},               # Поле равно None
#             {"telegram_id": ""},                 # Поле равно пустой строке
#             {"telegram_id": 0}                   # Поле равно 0
#         ],
#         "alpha2_name": selected_profile          # alpha2_name должно соответствовать выбранному профилю
#     })
#
#     if free_config:
#         config_and_QRCode.update_one(
#             {"_id": free_config["_id"]},         # Обновляем найденный документ
#             {"$set": {"telegram_id": user_id}}   # Устанавливаем telegram_id
#         )
#         logging.info(f"Added telegram_id {user_id} to config with alpha2_name {selected_profile}")
#         return True
#     else:
#         logging.warning(f"No available config found for alpha2_name {selected_profile}")
#         return False
#
# # Функция для сброса telegram_id в предыдущем конфиге
# def reset_telegram_id_for_user(user_id):
#     """
#     Сбрасывает telegram_id пользователя в предыдущем конфиге.
#     :param user_id: Telegram ID пользователя.
#     """
#     previous_config = config_and_QRCode.find_one({"telegram_id": user_id})
#     if previous_config:
#         config_and_QRCode.update_one(
#             {"_id": previous_config["_id"]},
#             {"$set": {"telegram_id": None}}  # Сбрасываем значение telegram_id
#         )
#         logging.info(f"Reset telegram_id for user {user_id} in config with alpha2_name {previous_config['alpha2_name']}")
#
# # Обработка успешной оплаты
# @bot.message_handler(content_types=['successful_payment'])
# def process_successful_payment(message):
#     logging.info(f"Successful payment received: {message.successful_payment}")
#     payload = message.successful_payment.invoice_payload
#     subscription_period = payload.split("_")[1]  # Например, "subscribe_1" -> "1"
#
#     subscription_periods = {
#         "1": 1,
#         "3": 3,
#         "6": 6,
#         "12": 12
#     }
#
#     if subscription_period not in subscription_periods:
#         bot.send_message(message.chat.id, "Произошла ошибка при оформлении подписки.")
#         return
#
#     months = subscription_periods[subscription_period]
#     user_id = message.chat.id
#
#     user_data = coll.find_one({"telegram_id": user_id})
#
#     if user_data and "subscription_expiry_date" in user_data and user_data["subscription_expiry_date"] is not None:
#         current_expiry_date = user_data["subscription_expiry_date"]
#         total_months = user_data.get("subscription_months", 0)
#
#         if total_months >= 12:
#             bot.send_message(
#                 message.chat.id,
#                 "Вы уже достигли максимального срока подписки (12 месяцев). Дополнительные покупки недоступны."
#             )
#             return
#
#         new_expiry_date = current_expiry_date + relativedelta(months=months)
#         total_months += months
#
#         coll.update_one(
#             {"telegram_id": user_id},
#             {
#                 "$set": {
#                     "subscription_status": "активна",
#                     "subscription_expiry_date": new_expiry_date,
#                     "subscription_months": total_months
#                 }
#             }
#         )
#         logging.info(
#             f"Updated subscription for user {user_id}. New end date: {new_expiry_date}, Total months: {total_months}"
#         )
#     else:
#         current_date = datetime.now()
#         new_expiry_date = current_date + relativedelta(months=months)
#
#         coll.update_one(
#             {"telegram_id": user_id},
#             {
#                 "$set": {
#                     "subscription_status": "активна",
#                     "subscription_expiry_date": new_expiry_date,
#                     "subscription_months": months
#                 }
#             },
#             upsert=True
#         )
#         logging.info(
#             f"Created or updated subscription for user {user_id}. End date: {new_expiry_date}, Months: {months}"
#         )
#
#     bot.send_message(
#         message.chat.id,
#         f"Новая дата окончания подписки: {new_expiry_date.strftime('%d.%m.%Y')}"
#     )
#
#     bot.send_message(
#         message.chat.id,
#         "Выберите страну для подключения Zoom VPN:",
#         reply_markup=create_inline_alpha2_button_choice()
#     )
#
# # Обработка выбора страны
# @bot.callback_query_handler(func=lambda call: call.data in ["ru_ssh_profile", "fi_ssh_profile"])
# def handle_country_selection(call):
#     user_id = call.from_user.id
#     selected_profile = call.data  # ru_ssh_profile или fi_ssh_profile
#
#     user_data = coll.find_one({"telegram_id": user_id})
#     previous_profile = user_data.get("ssh_alpha2") if user_data else None
#
#     selected_server = ssh.find_one({"alpha2": selected_profile})
#     if not selected_server:
#         bot.send_message(
#             call.message.chat.id,
#             "Выбранный сервер недоступен. Пожалуйста, попробуйте позже."
#         )
#         return
#
#     current_amount_users = selected_server.get("amount_users", 0)
#     if current_amount_users >= 5 and selected_profile != previous_profile:
#         bot.send_message(
#             call.message.chat.id,
#             "На данный сервер достигнуто максимальное количество пользователей. Пожалуйста, выберите другой сервер.",
#             reply_markup=create_inline_alpha2_button_choice()
#         )
#         return
#
#     if previous_profile and previous_profile != selected_profile:
#         reset_telegram_id_for_user(user_id)
#
#         # Уменьшаем счетчик amount_users для старого сервера
#         ssh.update_one(
#             {"alpha2": previous_profile},
#             {"$inc": {"amount_users": -1}}
#         )
#
#     coll.update_one(
#         {"telegram_id": user_id},
#         {"$set": {"ssh_alpha2": selected_profile}},  # Устанавливаем новый профиль SSH
#         upsert=True
#     )
#
#     if selected_profile != previous_profile:
#         ssh.update_one(
#             {"alpha2": selected_profile},
#             {"$inc": {"amount_users": 1}}
#         )
#
#     if not add_telegram_id_to_config(selected_profile, user_id):
#         bot.send_message(
#             call.message.chat.id,
#             "На данный момент нет доступных конфигураций для выбранного сервера. Пожалуйста, попробуйте позже."
#         )
#         return
#
#     country_name = "Россия" if selected_profile == "ru_ssh_profile" else "Финляндия"
#     bot.edit_message_text(
#         f"Вы выбрали сервер в {country_name}.",
#         chat_id=call.message.chat.id,
#         message_id=call.message.message_id
#     )
#
#     qrcode_name = get_qrcode_name_by_telegram_id(user_id)
#     if qrcode_name:
#         base_path = "./config_SSH_parsing/download_config"
#         file_path = os.path.join(base_path, selected_profile, "qr", qrcode_name)
#
#         if not os.path.exists(file_path):
#             bot.send_message(user_id, "QR-код не найден. Пожалуйста, проверьте настройки.")
#             return
#
#         try:
#             with open(file_path, 'rb') as photo:
#                 bot.send_photo(user_id, photo, caption="Вот ваш QR-код")
#         except Exception as e:
#             bot.send_message(user_id, f"Произошла ошибка при отправке QR-кода: {e}")
#     else:
#         bot.send_message(user_id, "QR-код не найден для вашего Telegram ID.")
#
#     config_name = get_config_name_by_telegram_id(user_id)
#     if config_name:
#         base_path = "./config_SSH_parsing/download_config"
#         file_path = os.path.join(base_path, selected_profile, "config", config_name)
#
#         # Проверяем, существует ли файл
#         if not os.path.exists(file_path):
#             bot.send_message(user_id, "Конфиг не найден. Пожалуйста, проверьте настройки.")
#             return
#
#         # Отправляем файл пользователю
#         try:
#             with open(file_path, 'rb') as document:
#                 bot.send_document(user_id, document, caption="Вот ваш конфигурационный файл")
#         except Exception as e:
#             bot.send_message(user_id, f"Произошла ошибка при отправке конфига: {e}")
#     else:
#         bot.send_message(user_id, "Конфиг не найден для вашего Telegram ID.")
#
#     logging.info(f"User {user_id} selected SSH profile: {selected_profile}")
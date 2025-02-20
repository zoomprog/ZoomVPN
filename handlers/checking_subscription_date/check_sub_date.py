from database.mongoDB import coll
from database.mongo_connect_ssh import ssh
from database.mongo_config_and_QRCode import config_and_QRCode
from datetime import datetime, timedelta
from handlers.config import bot
import logging
from messages.push import push_pay_sub_24h

# Настройка логирования (только в консоль)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]  # Вывод логов в консоль
)

def check_subscription():
    current_date_time = datetime.now()
    tomorrow = current_date_time + timedelta(days=1)

    # Получаем всех пользователей из базы данных users
    users = coll.find()

    for user in users:
        subscription_end_date = user.get('subscription_expiry_date')
        notification_sent = user.get('notification_sent', False)  # Проверяем, было ли отправлено уведомление

        # Проверяем, что дата подписки существует
        if subscription_end_date:
            if isinstance(subscription_end_date, str):
                try:
                    subscription_end_date = datetime.strptime(subscription_end_date, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    logging.error(f"Неверный формат даты для пользователя {user.get('telegram_id') or 'неизвестный'}")
                    continue

            # Проверяем, заканчивается ли подписка завтра и не отправлено ли уже уведомление
            if subscription_end_date.date() == tomorrow.date() and not notification_sent:
                telegram_id = user.get('telegram_id')
                if telegram_id:
                    bot.send_message(telegram_id, text=push_pay_sub_24h)
                    logging.info(f"Отправлено уведомление о конце подписки пользователю {telegram_id}")

                    # Обновляем статус отправки уведомления
                    coll.update_one(
                        {'_id': user['_id']},
                        {'$set': {'notification_sent': True}}
                    )
                else:
                    logging.warning(f"Не удалось отправить уведомление: отсутствует telegram_id для пользователя {user.get('_id')}")

            # Проверяем, прошла ли дата подписки
            if subscription_end_date < current_date_time:
                telegram_id = user.get('telegram_id')

                # Обновляем статус подписки в таблице users
                coll.update_one(
                    {'_id': user['_id']},
                    {
                        '$set': {
                            'subscription_status': 'нет подписки',
                            'subscription_months': 0,
                            'ssh_alpha2': None,
                            'subscription_expiry_date': None,
                            'notification_sent': False
                        }
                    }
                )
                logging.info(f"Статус подписки обновлен для пользователя {user.get('_id')}")

                # Обновляем поле amount в таблице ssh_servers
                ssh_alpha2 = user.get('ssh_alpha2')
                if ssh_alpha2:
                    # Находим SSH-сервер по alpha2
                    ssh_server = ssh.find_one({'alpha2': ssh_alpha2})
                    if ssh_server:
                        current_amount = ssh_server.get('amount_users', 0)
                        if current_amount > 0:
                            ssh.update_one(
                                {'_id': ssh_server['_id']},  # Используем _id найденного сервера
                                {'$inc': {'amount_users': -1}}  # Уменьшаем amount на 1
                            )
                            logging.info(f"Уменьшено значение amount для SSH-сервера {ssh_alpha2} на 1")
                        else:
                            logging.warning(f"Значение amount для SSH-сервера {ssh_alpha2} уже равно 0")
                    else:
                        logging.warning(f"SSH-сервер с alpha2={ssh_alpha2} не найден")
                else:
                    logging.warning(f"Отсутствует ssh_alpha2 для пользователя {user.get('_id')}")

                # Убераем занятый qrcode и file
                telegram_id = user.get('telegram_id')
                if telegram_id:
                    telegram_id_config_and_QRCode = config_and_QRCode.find_one({'telegram_id': telegram_id})
                    if telegram_id_config_and_QRCode:
                        config_and_QRCode.update_one(
                            {'telegram_id': telegram_id},
                            {'$set': {'telegram_id': 0}}  # Устанавливаем telegram_id равным 0
                        )
        else:
            logging.warning(f"Пропущен пользователь {user.get('_id')}: отсутствует subscription_end_date")
import paramiko
import os
import qrcode
from database.mongo_connect_ssh import ssh
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Подсчет документов напрямую через count_documents
document_count = ssh.count_documents({"alpha2": "ru_ssh_profile"})
if document_count == 0:
    logging.error("Не найдено профилей SSH с alpha2 'ru_ssh_profile'")
    exit(1)

# Получение данных из MongoDB
documents = ssh.find({"alpha2": "ru_ssh_profile"})

# Обработка каждого документа
for doc in documents:
    alpha2 = doc.get("alpha2")
    hostname = doc.get("hostname")
    port = doc.get("port")
    username = doc.get("username")
    password = doc.get("password")
    amount_users = doc.get("amount_users")

    if not all([hostname, port, username, password]):
        logging.error("Недостаточно данных для подключения к серверу")
        continue

    logging.info(f"Обработка профиля: {alpha2}")

    # Настройки подключения
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, port=port, username=username, password=password)
        logging.info("Успешное подключение к серверу")
    except paramiko.AuthenticationException:
        logging.error("Ошибка аутентификации. Проверьте имя пользователя и пароль.")
        continue
    except paramiko.SSHException as ssh_ex:
        logging.error(f"Ошибка SSH: {ssh_ex}")
        continue
    except paramiko.ssh_exception.NoValidConnectionsError:
        logging.error("Не удалось установить соединение. Проверьте адрес сервера и порт.")
        continue
    except Exception as e:
        logging.error(f"Произошла неизвестная ошибка: {e}")
        continue

    try:
        # Открытие SFTP-сессии для скачивания файлов
        sftp = client.open_sftp()

        # Удаленная директория, где находятся файлы .conf
        remote_directory = '/root/'

        # Локальная базовая директория для сохранения файлов
        local_base_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), 'download_config'))

        # Создание локальной директории download_config/config, если её нет
        config_directory = os.path.join(local_base_directory, 'ru/config')
        if not os.path.exists(config_directory):
            os.makedirs(config_directory)
            logging.info(f"Создана директория: {config_directory}")

        # Получение списка файлов в удаленной директории
        remote_files = sftp.listdir(remote_directory)

        # Фильтрация только файлов с расширением .conf, исключая wghub.conf
        conf_files = [f for f in remote_files if f.endswith('.conf') and f != 'wghub.conf']

        # Скачивание файлов
        for remote_file in conf_files:
            remote_file_path = os.path.join(remote_directory, remote_file)  # Полный путь к удаленному файлу
            local_file_path = os.path.join(config_directory, remote_file)  # Полный путь к локальному файлу

            try:
                sftp.get(remote_file_path, local_file_path)  # Скачиваем файл
                logging.info(f"Файл {remote_file} успешно скачан в {local_file_path}")
            except FileNotFoundError:
                logging.error(f"Файл {remote_file_path} не найден на удалённом сервере")
            except Exception as e:
                logging.error(f"Ошибка при скачивании файла {remote_file_path}: {e}")

    except Exception as e:
        logging.error(f"Ошибка при работе с SFTP: {e}")
    finally:
        # Закрытие SFTP-сессии и SSH-соединения
        if 'sftp' in locals() and sftp:
            sftp.close()
        client.close()

# Функция создания QR-кодов из .conf-файлов
def create_qr_codes_from_configs(config_dir, output_dir):
    # Создание папки для QR-кодов, если её нет
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        logging.info(f"Создана директория для QR-кодов: {output_dir}")

    # Перебор всех .conf-файлов в указанной директории
    if not os.path.exists(config_dir) or not os.listdir(config_dir):
        logging.error(f"Директория {config_dir} пуста или не существует")
        return

    for config_file in os.listdir(config_dir):
        if config_file.endswith('.conf'):
            config_file_path = os.path.join(config_dir, config_file)

            with open(config_file_path, 'r') as file:
                config_data = file.read().strip()

            if not config_data:
                logging.warning(f"Файл {config_file} пустой. Пропускаем...")
                continue

            # Создание QR-кода
            qr = qrcode.QRCode(
                version=None,  # Автоматическое определение версии
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4
            )
            qr.add_data(config_data)
            qr.make(fit=True)

            # Сохранение QR-кода в виде PNG
            img = qr.make_image(fill_color="black", back_color="white")
            output_file_path = os.path.join(output_dir, f"{os.path.splitext(config_file)[0]}.png")
            img.save(output_file_path)
            logging.info(f"QR-код для файла {config_file} создан и сохранён как {output_file_path}")

# Вызов функции для создания QR-кодов
png_directory = os.path.join(local_base_directory, 'ru/png')
create_qr_codes_from_configs(config_directory, png_directory)
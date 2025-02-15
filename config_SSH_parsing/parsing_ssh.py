import paramiko
import os
import qrcode
from database.mongo_connect_ssh import ssh
from database.mongo_config_and_QRCode import config_and_QRCode
import logging
from PIL import Image
# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Функция для создания QR-кода из .conf-файла
def create_qr_code(config_file_path, output_dir, logo_path=None):
    """
    Создает QR-код с минималистичным дизайном.
    :param config_file_path: Путь к файлу с данными для QR-кода.
    :param output_dir: Директория для сохранения QR-кода.
    :param logo_path: Путь к логотипу (опционально).
    :return: Путь к сохраненному QR-коду.
    """
    # Чтение данных из файла
    with open(config_file_path, 'r') as file:
        config_data = file.read().strip()
    if not config_data:
        logging.warning(f"Файл {config_file_path} пустой. Пропускаем...")
        return None

    # Создание QR-кода
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # Высокий уровень коррекции ошибок
        box_size=10,
        border=2  # Уменьшаем границу для более компактного вида
    )
    qr.add_data(config_data)
    qr.make(fit=True)

    # Создание изображения QR-кода
    img = qr.make_image(fill_color="#000000", back_color="#FFFFFF")  # Черно-белый QR-код

    # Добавление логотипа (если указан)
    if logo_path and os.path.exists(logo_path):
        logo = Image.open(logo_path)
        logo_size = 50  # Размер логотипа
        logo = logo.resize((logo_size, logo_size), Image.ANTIALIAS)

        # Позиционирование логотипа в центре QR-кода
        img_width, img_height = img.size
        logo_position = (
            (img_width - logo_size) // 2,
            (img_height - logo_size) // 2
        )

        # Наложение логотипа на QR-код
        img.paste(logo, logo_position)

    # Сохранение QR-кода
    output_file_path = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(config_file_path))[0]}.png")
    img.save(output_file_path)
    logging.info(f"QR-код создан: {output_file_path}")
    return output_file_path


# Основная функция для обработки SSH-профилей
def process_ssh_profiles():
    # Получение всех профилей SSH
    ssh_profiles = ssh.find()

    for profile in ssh_profiles:
        alpha2 = profile.get("alpha2")
        hostname = profile.get("hostname")
        port = profile.get("port")
        username = profile.get("username")
        password = profile.get("password")

        if not all([alpha2, hostname, port, username, password]):
            logging.error(f"Недостаточно данных для профиля {alpha2}. Пропускаем...")
            continue

        logging.info(f"Обработка профиля: {alpha2}")

        try:
            # Подключение к SSH-серверу
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname, port=port, username=username, password=password)

            # Открытие SFTP-сессии
            sftp = ssh_client.open_sftp()
            remote_directory = '/root/'  # Директория с конфигами на сервере
            local_base_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), 'download_config'))

            # Создание локальной директории для конфигов
            config_directory = os.path.join(local_base_directory, alpha2, 'config')
            if not os.path.exists(config_directory):
                os.makedirs(config_directory)

            # Создание локальной директории для QR-кодов
            qr_directory = os.path.join(local_base_directory, alpha2, 'qr')
            if not os.path.exists(qr_directory):
                os.makedirs(qr_directory)

            # Скачивание .conf-файлов
            remote_files = sftp.listdir(remote_directory)
            conf_files = [f for f in remote_files if f.endswith('.conf') and f != 'wghub.conf']

            for remote_file in conf_files:
                remote_file_path = os.path.join(remote_directory, remote_file)
                local_file_path = os.path.join(config_directory, remote_file)

                try:
                    sftp.get(remote_file_path, local_file_path)
                    logging.info(f"Файл {remote_file} успешно скачан в {local_file_path}")

                    # Создание QR-кода
                    qr_file_path = create_qr_code(local_file_path, qr_directory)
                    if qr_file_path:
                        # Проверка наличия записи в базе данных
                        config_name = os.path.basename(local_file_path)
                        qrcode_name = os.path.basename(qr_file_path)

                        existing_record = config_and_QRCode.find_one({
                            "qrcode_name": qrcode_name,
                            "config_name": config_name,
                            "alpha2_name": alpha2
                        })

                        if existing_record:
                            logging.info(f"Запись уже существует: {config_name}, {qrcode_name}. Пропускаем...")
                            continue

                        # Сохранение информации в ConfigAndQRCode
                        config_and_QRCode.insert_one({
                            "qrcode_name": qrcode_name,
                            "alpha2_name": alpha2,
                            "config_name": config_name,
                            "telegram_id": 0  # Можно добавить telegram_id позже
                        })
                        logging.info(f"Новая запись сохранена в ConfigAndQRCode: {config_name}, {qrcode_name}")

                except FileNotFoundError:
                    logging.error(f"Файл {remote_file_path} не найден на удалённом сервере")
                except Exception as e:
                    logging.error(f"Ошибка при обработке файла {remote_file}: {e}")

            sftp.close()
            ssh_client.close()

        except Exception as e:
            logging.error(f"Ошибка при подключении к профилю {alpha2}: {e}")
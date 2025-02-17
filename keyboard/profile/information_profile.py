from telebot import types
from handlers.config import bot
from database.mongo_config_and_QRCode import config_and_QRCode
import logging

def inline_keyboard_profile_qr_or_file(call):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    qr = types.InlineKeyboardButton("QR-код", callback_data="qr_user_profile_conclusion")
    file = types.InlineKeyboardButton("Файл", callback_data="file_user_profile_conclusion")
    main_menu = types.InlineKeyboardButton("Главное меню", callback_data="main_menu")
    keyboard.add(qr,file)
    keyboard.add(main_menu)
    return keyboard
def qr_user_conclusion(telegram_id):
    try:
        config = config_and_QRCode.find_one({"telegram_id": telegram_id})
        if config and "qrcode_name" in config:
            logging.info(f"Found qrcode_name for user {telegram_id}: {config['qrcode_name']}")
            return config["qrcode_name"]
        else:
            logging.warning(f"No qrcode_name found for user {telegram_id}")
            return None
    except Exception as e:
        logging.error(f"Error while fetching qrcode_name for user {telegram_id}: {e}")
        return None
def file_user_conclusion(telegram_id):
    try:
        config = config_and_QRCode.find_one({"telegram_id": telegram_id})
        if config and "config_name" in config:
            logging.info(f"Found config_name for user {telegram_id}: {config['config_name']}")
            return config["config_name"]
        else:
            logging.warning(f"No config_name found for user {telegram_id}")
            return None
    except Exception as e:
        logging.error(f"Error while fetching config_name for user {telegram_id}: {e}")
        return None
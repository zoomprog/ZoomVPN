from pymongo import MongoClient
from handlers.config import TOKEN_MONGO

# Подключение к MongoDB
try:
    client = MongoClient(TOKEN_MONGO)
    client.admin.command('ping')  # Проверка доступности MongoDB
    print("Подключение к MongoDB успешно")
except Exception as e:
    print(f"Ошибка подключения к MongoDB: {e}")
    exit(1)

db = client.VPN  # База данных
ssh = db.SSH     # Коллекция

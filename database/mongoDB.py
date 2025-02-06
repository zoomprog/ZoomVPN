from pymongo import MongoClient
from handlers.config import TOKEN_MONGO

# Подключение к MongoDB

client = MongoClient(TOKEN_MONGO)
db = client.VPN
coll = db.users
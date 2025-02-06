from handlers.config import bot
from handlers.starthandler import start
from keyboard.keyboardInlineStartMessage import create_inline_keyboard
from handlers.callback_handler import handle_callback

# Запуск бота
if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling(non_stop=True)
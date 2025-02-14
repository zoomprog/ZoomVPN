from handlers.config import bot
from handlers.starthandler import start
from keyboard.keyboardInlineStartMessage import create_inline_keyboard
from handlers.callback_handler import handle_callback
from config_SSH_parsing.parsing_ssh import process_ssh_profiles
import threading,time

# Функция для периодического выполнения задачи
def scheduled_task():
    while True:
        print("Запуск процесса обработки SSH-профилей...")
        try:
            process_ssh_profiles()  # Вызов вашей функции
        except Exception as e:
            print(f"Ошибка при выполнении задачи: {e}")
        # Ждём 2 часа (7200 секунд)
        time.sleep(1800)

# Запуск задачи в отдельном потоке
def start_scheduled_task():
    thread = threading.Thread(target=scheduled_task, daemon=True)
    thread.start()

# Запуск бота
if __name__ == '__main__':
    print("Бот запущен...")
    start_scheduled_task()  # Запускаем фоновую задачу
    bot.polling(non_stop=True)  # Запускаем основной цикл бота
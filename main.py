from handlers.config import bot
from handlers.starthandler import start
from keyboard.vpn_menu.main_menu import create_inline_keyboard
from handlers.callback_handler import handle_callback
from config_SSH_parsing.parsing_ssh import process_ssh_profiles
from handlers.checking_subscription_date.check_sub_date import check_subscription
import threading
import time

# Функция для периодического выполнения задачи обработки SSH-профилей
def scheduled_task():
    while True:
        print("Запуск процесса обработки SSH-профилей...")
        try:
            process_ssh_profiles()  # Вызов вашей функции
        except Exception as e:
            print(f"Ошибка при выполнении задачи обработки SSH-профилей: {e}")
        # Ждём 2 часа (7200 секунд)
        time.sleep(7200)

# Функция для периодической проверки актуальности подписки
def scheduled_task_sub_check():
    while True:
        print("Запуск процесса проверки актуальности подписки...")
        try:
            check_subscription()  # Вызов вашей функции
        except Exception as e:
            print(f"Ошибка при выполнении задачи проверки подписки: {e}")
        # Ждём 1 час (3600 секунд)
        time.sleep(3600)

# Запуск задачи в отдельном потоке
def start_scheduled_task(task_func):
    thread = threading.Thread(target=task_func, daemon=True)
    thread.start()

# Запуск бота
if __name__ == '__main__':
    print("Бот запущен...")

    # Запускаем фоновые задачи в отдельных потоках
    start_scheduled_task(scheduled_task)  # Задача обработки SSH-профилей
    start_scheduled_task(scheduled_task_sub_check)  # Задача проверки подписки

    # Запускаем основной цикл бота
    bot.polling(non_stop=True)
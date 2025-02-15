from handlers.config import bot
from handlers.HandlerMenu.handler_language_select import handle_language_selection
from handlers.HandlerMenu.handler_help import handle_halp
from keyboard.keyboardInlineStartMessage import create_inline_keyboard
from telebot import types
import logging
from handlers.HandlerMenu.handler_pay_sub import process_pre_checkout_query,process_successful_payment
from keyboard.keyboard_inline_buy_menu import keyboard_inline_buy,keyboard_inline_payment
from handlers.callback_action_handler import process_callback
from handlers.HandlerMenu.back_main_menu import main_menu
from messages.messages import help_Connection_Instructions_qr, help_Connection_Instructions_file
from keyboard.keyboard_inline_help_connect import create_inline_help_connect
from keyboard.keyboard_back_menu import create_inline_back_menu
from handlers.HandlerMenu.help_menu import doesnt_work_vpn
# Настройка логирования для отладки
logging.basicConfig(level=logging.INFO)





# Обработчик нажатий инлайн-кнопок
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    try:
        if call.data == "buy_extend":
            keyboard_inline_buy(call)

        elif call.data.startswith("subscribe_"):
            keyboard_inline_payment(call)

        elif call.data == "help":
            handle_halp(call)  # Вызов функции помощи
        elif call.data == "help_how_to_connect":
            bot.send_message(call.message.chat.id, text="Cпособ подключения к VPN", reply_markup=create_inline_help_connect(),parse_mode='Markdown')
        elif call.data == "qr_connect_help":
            bot.send_message(
                call.message.chat.id,
                text=help_Connection_Instructions_qr,
                reply_markup=create_inline_back_menu(),
                parse_mode='Markdown'
            )
        elif call.data == "file_connect_help":
            bot.send_message(
                call.message.chat.id,
                text=help_Connection_Instructions_file,
                reply_markup=create_inline_back_menu(),
                parse_mode='Markdown'
            )
        elif call.data == "vpn_not_working":
            doesnt_work_vpn(call)
        elif call.data == "contact_with_me":
            bot.send_message(
                call.message.chat.id,
                text="C предложениями о сотрудничестве, улучшении функционала и по другим вопросам, пишите мне @zoomkaXXX",
                parse_mode='Markdown'
            )
        elif call.data == "active_keys":
            process_callback(call, "Вы выбрали опцию 'Мои активные ключи'.", "Выбрано: Мои активные ключи")

        elif call.data == "change_location":
            process_callback(call, "Вы выбрали опцию 'Изменить локацию'.", "Выбрано: Изменить локацию")

        elif call.data == "change_protocol":
            process_callback(call, "Вы выбрали опцию 'Изменить протокол'.", "Выбрано: Изменить протокол")

        elif call.data == "donate":
            process_callback(call, "Вы выбрали опцию 'Пожертвовать'.", "Выбрано: Пожертвовать")

        elif call.data == "about_vpn":
            process_callback(call, "Вы выбрали опцию 'Всё о ZoomVPN'.", "Выбрано: Всё о ZoomVPN")

        elif call.data == "invite":
            process_callback(call, "Вы выбрали опцию 'Пригласить'.", "Выбрано: Пригласить")

        elif call.data == "main_menu":  # Проверяем "Главное меню" до языков
            main_menu(call)

        elif call.data in ["ru", "en", "de", "fr"]:  # Языки проверяем после "Главное меню"
            language_mapping = {
                "ru": "русский",
                "en": "английский",
                "de": "немецкий",
                "fr": "французский"
            }
            selected_language = language_mapping.get(call.data)
            if selected_language:
                process_callback(
                    call,
                    f"Ты выбрал {selected_language} язык! В разработке!",
                    f"Вы выбрали: {selected_language} язык",
                    parse_mode='HTML'
                )
            else:
                process_callback(call, "Выбранный язык не поддерживается.", "Неизвестный язык")

        else:
            process_callback(call, "Неизвестная команда. Пожалуйста, выберите одну из доступных опций.",
                             "Неизвестная команда")

    except Exception as e:
        bot.send_message(call.message.chat.id, f"Произошла ошибка: {e}")
        logging.error(f"Error in callback handler: {e}")



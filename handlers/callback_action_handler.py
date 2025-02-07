from handlers.config import bot
# Вспомогательная функция для обработки общих действий
def process_callback(call, message_text, answer_text=None, parse_mode=None):
    if answer_text:
        bot.answer_callback_query(call.id, answer_text)
    bot.send_message(call.message.chat.id, message_text, parse_mode=parse_mode)
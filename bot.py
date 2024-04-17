import logging
from telebot import TeleBot

from config import TELEGRAM_TOKEN
from speechkit import text_to_speech
from database import Database
from utils import is_tts_symbol_limit

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename='logs.log',
    filemode="a",
    datefmt="%Y-%m-%d %H:%M:%S"
)

bot = TeleBot(TELEGRAM_TOKEN)

db = Database()
db.create_table()


@bot.message_handler(commands=['tts'])
def tts_handler(message):
    user_id = message.from_user.id
    bot.send_message(user_id,
                     'Отправь следующим сообщеним текст, чтобы я его озвучил!')
    bot.register_next_step_handler(message, tts)


def tts(message):
    user_id = message.from_user.id
    text = message.text

    # Проверка, что сообщение действительно текстовое
    if message.content_type != 'text':
        bot.send_message(user_id, 'Отправь текстовое сообщение')
        return

        # Считаем символы в тексте и проверяем сумму потраченных символов
    text_symbol = is_tts_symbol_limit(user_id, bot, text, db)
    if text_symbol is None:
        return

    # Записываем сообщение и кол-во символов в БД
    db.insert_row(user_id, text, text_symbol)

    # Получаем статус и содержимое ответа от SpeechKit
    status, content = text_to_speech(text)

    # Если статус True - отправляем голосовое сообщение, иначе - сообщение
    # об ошибке
    if status:
        bot.send_voice(user_id, content)
    else:
        bot.send_message(user_id, content)


bot.polling()

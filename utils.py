from config import MAX_USER_TTS_SYMBOLS, MAX_TTS_SYMBOLS


def is_tts_symbol_limit(user_id, bot, text, db):

    text_symbols = len(text)

    # Функция из БД для подсчёта всех потраченных пользователем символов
    all_symbols = db.count_all_symbol(user_id) + text_symbols

    # Сравниваем all_symbols с количеством доступных пользователю символов
    if all_symbols >= MAX_USER_TTS_SYMBOLS:
        msg = f"Превышен общий лимит SpeechKit TTS {MAX_USER_TTS_SYMBOLS}. Использовано: {all_symbols} символов. Доступно: {MAX_USER_TTS_SYMBOLS - all_symbols}"
        bot.send_message(user_id, msg)
        return None

    # Сравниваем количество символов в тексте с максимальным количеством символов в тексте
    if text_symbols >= MAX_TTS_SYMBOLS:
        msg = f"Превышен лимит SpeechKit TTS на запрос {MAX_TTS_SYMBOLS}, в сообщении {text_symbols} символов"
        bot.send_message(user_id, msg)
        return None
    return len(text)

import sqlite3
import logging


class Database:
    def __init__(self, db_name="speech_kit.db"):
        self.db_name = db_name

    def prepare_db(self):
        try:
            conn = sqlite3.connect(self.db_name)
            logging.info('Database is on')
            return conn
        except sqlite3.DatabaseError as e:
            logging.error(f'Ошибка sqlite {e}')
            return None
        except sqlite3.Error as e:
            logging.error(f'Ошибка sqlite {e}')
            return None
        except Exception as e:
            logging.error(f'Неизвестная ошибка {e}')
            return None

    def create_table(self):
        conn = self.prepare_db()
        cursor = conn.cursor()
        create_table_query = """
         CREATE TABLE IF NOT EXISTS messages (
             id INTEGER PRIMARY KEY, 
             user_id INTEGER,
             username TEXT,
             message TEXT,
             tts_symbols INTEGER DEFAULT 0,
             stt_blocks INTEGER DEFAULT 0
         )
         """
        cursor.execute(create_table_query)
        conn.commit()
        logging.info('Таблица messages успешно создана')
        conn.close()

    def insert_row(self, user_id, message, tts_symbols):
        try:
            # Подключаемся к базе
            conn = self.prepare_db()
            cursor = conn.cursor()
            # Вставляем в таблицу новое сообщение
            cursor.execute(
                '''INSERT INTO messages (user_id, message, tts_symbols)VALUES (?, ?, ?)''',
                (user_id, message, tts_symbols))
            # Сохраняем изменения
            conn.commit()
        except Exception as e:  # обрабатываем ошибку и записываем её в переменную <e>
            print(f"Error: {e}")  # выводим ошибку в консоль

    def count_all_symbol(self, user_id):
        try:
            conn = self.prepare_db()
            cursor = conn.cursor()
            cursor.execute('''SELECT SUM(tts_symbols) FROM messages WHERE user_id=?''', (user_id,))
            data = cursor.fetchone()
            conn.close()
            if data and data[0]:
                return data[0]
            else:
                return 0
        except Exception as e:
            print(f"Error: {e}")

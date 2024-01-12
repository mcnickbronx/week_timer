import sqlite3
import  os
import datetime

conn = sqlite3.connect('data.db')

def get_today_date():
    return datetime.datetime.now().strftime("%d.%m.%Y")


def check_and_create_db(db_name='data.db'):
    db_path = os.path.join(os.getcwd(), "src", "data.db")
    if not os.path.exists(db_path):
        # Если файла нет, создаем его и добавляем таблицу
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        # Создание таблицы с первичным ключом - сегодняшней датой
        c.execute('''
            CREATE TABLE IF NOT EXISTS timer (
                date TEXT PRIMARY KEY,
                duration INTEGER
            )
        ''')
        conn.commit()
        conn.close()
        print(f"База данных '{db_path}' создана.")
    else:
        print(f"База данных '{db_path}' уже существует.")


# Функция для добавления или обновления записи таймера
def add_or_update_timer(duration):
    date = get_today_date()
    db_path = os.path.join(os.getcwd(), "src", "data.db")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Проверяем, существует ли уже запись на сегодняшнюю дату
    c.execute("SELECT duration FROM timer WHERE date = ?", (date,))
    result = c.fetchone()

    if result:
        # Если запись существует, прибавляем duration к существующему значению и обновляем запись
        current_duration = result[0]
        new_duration = current_duration + duration
        c.execute("UPDATE timer SET duration = ? WHERE date = ?",
                  (new_duration, date))
    else:
        # Если записи нет, добавляем новую
        c.execute("INSERT INTO timer (date, duration) VALUES (?, ?)",
                  (date, duration))
    conn.commit()


def get_duration_and_convert():
    # Подключаемся к базе данных
    date = get_today_date()
    db_path = os.path.join(os.getcwd(), "src", "data.db")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Получаем duration для указанной даты
    c.execute("SELECT duration FROM timer WHERE date = ?", (date,))
    result = c.fetchone()

    # Закрываем соединение с базой данных
    conn.close()

    if result:
        duration_in_seconds = result[0]
        # Конвертируем секунды в часы, минуты и секунды
        hours = duration_in_seconds // 3600
        minutes = (duration_in_seconds % 3600) // 60
        seconds = duration_in_seconds % 60
        return f'{hours}:{minutes:02}'
    else:
        return '...'
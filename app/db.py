'''
Набор функций работы с базой для учета вермени.
Пока не используется в проекте.
'''

import sqlite3
import  os
import datetime

conn = sqlite3.connect('data.db')

def get_today_date():
    return datetime.datetime.now().strftime("%d.%m.%Y")


def check_and_create_db(db_name='data.db'):
    db_path = os.path.join(os.getcwd(), "src", "data.db")

    # Если файла нет, создаем его и добавляем таблицу
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Создание таблицы с первичным ключом - сегодняшней датой
    c.execute('''
        CREATE TABLE IF NOT EXISTS timer (
            date TEXT PRIMARY KEY,
            duration INTEGER,
            time TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS timer_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timer_date TEXT,
            start_time TEXT,
            end_time TEXT,
            FOREIGN KEY(timer_date) REFERENCES timer(date)
        )
    ''')
    conn.commit()
    conn.close()

def sec_to_time(duration):
    hours = duration // 3600
    minutes = (duration % 3600) // 60
    seconds = duration % 60
    time = f'{hours}:{minutes}:{seconds}'
    return time

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

        time = sec_to_time(new_duration)

        c.execute("UPDATE timer SET duration = ?, time = ? WHERE date = ?",
                  (new_duration, time, date))
    else:
        time = sec_to_time(duration)
        # Если записи нет, добавляем новую
        c.execute("INSERT INTO timer (date, duration, time) VALUES (?, ?, ?)",
                  (date, duration, time))
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
        # Конвертируем секунды в часы, минуты
        hours = duration_in_seconds // 3600
        minutes = (duration_in_seconds % 3600) // 60
        return f'{hours}:{minutes:02}'
    else:
        return '...'


def add_timer_history(start, end):
    # Подключаемся к базе данных
    db_path = os.path.join(os.getcwd(), "src", "data.db")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Получаем дату начала и окончания
    start_date = start.strftime("%Y%m%d")
    end_date = end.strftime("%Y%m%d")

    if start_date == end_date:
        # Если даты совпадают, добавляем одну запись
        c.execute("INSERT INTO timer_history (timer_date, start_time, end_time) VALUES (?, ?, ?)",
                  (start_date, start.strftime("%H:%M:%S"), end.strftime("%H:%M:%S")))
    else:
        # Если даты различаются, добавляем две записи
        # Первая запись до полуночи первого дня
        c.execute("INSERT INTO timer_history (timer_date, start_time, end_time) VALUES (?, ?, ?)",
                  (start_date, start.strftime("%H:%M:%S"), '23:59:59'))
        # Вторая запись начиная с полуночи следующего дня
        c.execute("INSERT INTO timer_history (timer_date, start_time, end_time) VALUES (?, ?, ?)",
                  (end_date, '00:00:00', end.strftime("%H:%M:%S")))

    conn.commit()
    conn.close()


def start_timer_session(start):
    db_path = os.path.join(os.getcwd(), "src", "data.db")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    start_date = start.strftime("%d.%m.%Y")
    start_time = start.strftime("%H:%M:%S")

    # Вставляем начальное время, предполагая, что end_time будет добавлен позже
    c.execute("INSERT INTO timer_history (timer_date, start_time) VALUES (?, ?)",
              (start_date, start_time))

    conn.commit()
    conn.close()


def end_timer_session(start, end):
    db_path = os.path.join(os.getcwd(), "src", "data.db")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    start_date = start.strftime("%d.%m.%Y")
    end_date = end.strftime("%d.%m.%Y")

    end_time = end.strftime("%H:%M:%S")

    # Проверяем, заканчивается ли сессия в тот же день, что и началась
    if start_date == end_date:
        # Обновляем запись, добавляя end_time
        c.execute("UPDATE timer_history SET end_time = ? WHERE timer_date = ? AND start_time = ?",
                  (end_time, start_date, start.strftime("%H:%M:%S")))
    else:
        # Если сессия заканчивается в другой день, создаем новую запись
        c.execute("INSERT INTO timer_history (timer_date, start_time, end_time) VALUES (?, ?, ?)",
                  (end_date, '00:00:00', end_time))

        c.execute("UPDATE timer_history SET end_time = ? WHERE timer_date = ? AND start_time = ?",
                  ('23:59:59', start_date, start.strftime("%H:%M:%S")))

    conn.commit()
    conn.close()
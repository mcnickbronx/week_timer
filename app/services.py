import requests
from requests.exceptions import Timeout
import datetime
import configparser

config = configparser.ConfigParser()  # создаём объекта парсера
config.read("settings.ini")

API_KEYS = config["Config"]["API_KEY"].split(',')
ID_USER = config["Config"]["ID_USER"]


def to_time(time):
    return f'{time // 60:02}:{time % 60:02}'


def get_ticket_time():
    '''
    Обращение ко всем апи пространств из конфига Week
    :return:
    tasks_curent - текущий счетчик времени
    time_all_tikets - сумма за день
    Если возвращается [], 0 - есть ошибка
    '''
    tasks = []
    for api_key in API_KEYS:
        headers = {
            'authorization': 'Bearer ' + api_key,
        }
        try:
            response = requests.get(f'https://api.weeek.net/public/v1/tm/tasks?userId={ID_USER}&perPage=500', headers=headers)
        except Exception as e:
            print(e)
            print("Запрос прошел с ошибкой")
            return ([], 0)

        if response.status_code == 200:
            tasks += response.json()['tasks']
        else:
            return ([], 0)

    tasks_append = {}
    today = datetime.date.today()

    time_all_tikets_i = 0  # для подсчета минут за сегодня
    id = 0  # Запишем ид задачь по порядку
    for task in tasks:

        time_count = 0  # последние минуты задачи
        time_count_all = 0  # минуты по всей задаче

        for w in task['workloads']:
            time_count = int(w['duration'])  # Заберу последнюю
            time_count_all += time_count

            date = datetime.datetime.strptime(w["date"], "%Y-%m-%d").date()
            if date == datetime.date.today():
                time_all_tikets_i += time_count

        task_item = {'title': task['title'], 'time': time_count, 'time_all': time_count_all}
        id += 1
        tasks_append[id] = task_item

    time_all_tikets = time_all_tikets_i
    return (tasks_append, time_all_tikets)
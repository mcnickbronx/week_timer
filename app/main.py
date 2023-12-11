#!python3
import threading
import time
import pystray
from PIL import Image, ImageFont, ImageDraw
import os
import requests
import datetime
import configparser

config = configparser.ConfigParser()  # создаём объекта парсера
config.read("settings.ini")

API_KEYS = config["Config"]["API_KEY"].split(',')
ID_USER = config["Config"]["ID_USER"]

icon = None  # Глобальный icon
stop = False  # Признак глобальной остановки


def set_icon(time):
    time = f'{time:02}'
    blank_image = Image.new('RGB', (64, 64), '#111')
    # blank_image = Image.open("./img/ico2.png")
    img_draw = ImageDraw.Draw(blank_image)
    # img_draw.rectangle((70, 50, 270, 200), outline='red', fill='blue')
    font_path = os.path.join(os.getcwd(), "src", "Roboto-Bold.ttf")
    font = ImageFont.truetype(font_path, 55)
    img_draw.text((2, 2), time, fill='orange', font=font)
    icon.icon = blank_image
    # blank_image.save('sample-out.png')


def unset_icon():
    image_path = os.path.join(os.getcwd(), "src", "ico1.png")
    image = Image.open(image_path)
    # image = Image.new('RGB', (64, 64), '#eee')
    icon.icon = image
    print('unset_icon')


def creat_menu(mess):
    # создаст объект меню с заголовком сообщения
    menu = pystray.Menu(
        pystray.MenuItem(mess, after_click),
        pystray.MenuItem("Выход", after_click))
    return menu

def update_title(message):
    icon._title = message
    icon._update_title()

    icon._menu = creat_menu(message)
    icon._update_menu()


def send_notify(message, title):
    pass
    # icon.notify(message, title) Нотифай отключил


def after_click(self, query):
    global stop
    if str(query) == "":
        pass
    elif str(query) == "Выход":
        stop = True
        icon.stop()

def to_time(time):
    return f'{time // 60:02}:{time % 60:02}'


def get_ticket_time():
    tasks = []
    for api_key in API_KEYS:

        headers = {
            'authorization': 'Bearer ' + api_key,
        }

        response = requests.get(f'https://api.weeek.net/public/v1/tm/tasks?userId={ID_USER}&perPage=500', headers=headers)

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

            date = datetime.datetime.strptime(w["date"], "%d.%m.%Y").date()
            if date == datetime.date.today():
                time_all_tikets_i += time_count

        task_item = {'title': task['title'], 'time': time_count, 'time_all': time_count_all}
        # tasks_append[task['id']] = task_item
        id += 1
        tasks_append[id] = task_item

    time_all_tikets = time_all_tikets_i
    return (tasks_append, time_all_tikets)



# Основная программа
def start_week():

    time.sleep(2)
    print(icon)

    tasks_init = {}
    tasks_curent = {}
    time_all_tikets = 0  # все минуты сегодня

    tasks_init, time_all_tikets = get_ticket_time()

    message = f'За день: {to_time(time_all_tikets)}'
    update_title(message)
    # unset_icon()

    i_not_change = 0
    is_start_timer = False
    while stop == False:
        time.sleep(5)
        tasks_curent, time_all_tikets = get_ticket_time()

        if tasks_curent:
            if len(tasks_curent) != len(tasks_init):
                print('Поменялось количество задач!')
                tasks_init = tasks_curent

            is_change = False
            count_change = 0
            i = 0
            for key, task in tasks_curent.items():
                # print(f'Текущее {task}')
                # print(f'Сравниваем {tasks_init[key]} {key=}')
                # print(f"{task['time']} {tasks_init[key]['time']}")
                if task['time'] != tasks_init[key]['time']:
                    tasks_init[key]['time'] = task['time']  # Выравниваем
                    print('Время идет!')
                    set_icon(task['time'])
                    is_change = True
                    count_change += 1
                    print(f'{count_change=}')
                    if not is_start_timer:
                        # send_notify(
                        #     f"{task['title']} \n ------------ \n Всего за день: {to_time(time_all_tikets)} \n Всего по задаче: {to_time(task['time_all'])}",
                        #     "Запуск задачи!")
                        is_start_timer = True

                    message = f"За день: {to_time(time_all_tikets)}"
                    # message = f"За день: {to_time(time_all_tikets)} Всего: {to_time(task['time_all'])} Таймер: {to_time(task['time'])}"
                    update_title(message)

            if count_change > 1:
                print('Внимание! Несколько таймеров!')
                message = f"Внимание! Запущено {count_change} задач."
                update_title(message)
                send_notify(message)

            if is_change:
                i_not_change = 0
            else:
                i_not_change += 1

            print(f'{i_not_change=}')

            if i_not_change > 12:
                # message = f'За день: {to_time(time_all_tikets)}'
                # update_title(message)

                if is_start_timer:
                    unset_icon()
                    send_notify(f"Нат запущенных задач. \n Всего за день: {to_time(time_all_tikets)}", "Внимание!")
                is_start_timer = False
        else:
            update_title('Сбой апи! Новая попытка...')
            send_notify(f"Сбой апи!", "Внимание!")

def start_icon():
    global icon
    image_path = os.path.join(os.getcwd(), "src", "ico1.png")
    image = Image.open(image_path)
    # image = Image.new('RGB', (64, 64), '#eee')
    menu = creat_menu('Старт!')
    icon = pystray.Icon("WeekTimer", image, "Timer", menu=menu)

    threading.Thread(target=start_week).start()  # Запуск основной програмы в другом потоке

    icon.run()


start_icon()

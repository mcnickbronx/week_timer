#!python3
import threading
import time
import pystray
from PIL import Image, ImageFont, ImageDraw
import os

from services import *

icon = None  # Глобальный icon
stop = False  # Признак глобальной остановки


def set_icon(time):
    time = f'{time:02}'
    blank_image = Image.new('RGB', (64, 64), '#111')
    img_draw = ImageDraw.Draw(blank_image)
    font_path = os.path.join(os.getcwd(), "src", "Roboto-Bold.ttf")
    font = ImageFont.truetype(font_path, 55)
    img_draw.text((2, 2), time, fill='orange', font=font)
    icon.icon = blank_image


def unset_icon():
    image_path = os.path.join(os.getcwd(), "src", "ico1.png")
    image = Image.open(image_path)
    icon.icon = image


def err_icon():
    image_path = os.path.join(os.getcwd(), "src", "ico3.png")
    image = Image.open(image_path)
    icon.icon = image


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


# Основная программа
def start_week():
    '''
    Основной цикл проверки включенных счетчиков.
    '''
    try:
        time.sleep(2)
        print(icon)

        tasks_init = {}
        tasks_curent = {}
        time_all_tikets = 0  # все минуты сегодня

        tasks_init, time_all_tikets = get_ticket_time()

        message = f'За день: {to_time(time_all_tikets)}'
        update_title(message)

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
                    if task['time'] != tasks_init[key]['time']:
                        tasks_init[key]['time'] = task['time']  # Выравниваем
                        print('Время идет!')
                        set_icon(task['time'])
                        is_change = True
                        count_change += 1
                        print(f'{count_change=}')
                        if not is_start_timer:
                            is_start_timer = True

                        message = f"За день: {to_time(time_all_tikets)}"
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
                    if is_start_timer:
                        unset_icon()
                        send_notify(f"Нат запущенных задач. \n Всего за день: {to_time(time_all_tikets)}", "Внимание!")
                    is_start_timer = False
            else:
                update_title('Сбой апи! Новая попытка...')
                send_notify(f"Сбой апи!", "Внимание!")

    except Exception as e:
        print(e)
        err_icon()
        update_title('Ошибка, смотрите консоль')

def start_icon():
    global icon
    image_path = os.path.join(os.getcwd(), "src", "ico1.png")
    image = Image.open(image_path)
    menu = creat_menu('Старт!')
    icon = pystray.Icon("WeekTimer", image, "Timer", menu=menu)

    threading.Thread(target=start_week).start()  # Запуск основной програмы в другом потоке

    icon.run()


start_icon()

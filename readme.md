# Week Timer
Утилита которая показывает запущенную задачу в week.net в системном трее.

![Screenshot_46](https://github.com/mcnickbronx/week_timer/assets/17063709/870c01ae-4c6b-4121-88fe-d483050b5286)

![Screenshot_47](https://github.com/mcnickbronx/week_timer/assets/17063709/0f5c4438-84ff-4c2d-9661-6436c75c0ccb)

![Screenshot_48](https://github.com/mcnickbronx/week_timer/assets/17063709/28d60ed5-5457-48d2-bf6e-b5052ae1edad)

## Поддержка OS
Работает на Windows, macOS, Linux

Для работы необходимо что бы в системе был установлен Python и нужные зависимости через pip (pystray Pillow requests).
Тестировалось на 3.11, но должно работать и сменьшей версией.
На macOS возможно придется обновить Python.

## Использование программы

Таймер по апи считывает все ваши задачи и время по ним. При включенном таймере в Week таймер отражает минуты, при выключенном, будет иконка серого цвета.

Считает общее время по всем задачам за сегодняшенее число. Что бы увидеть сколько проработано сегодня, нужно подвести курсор к таймеру и сделать правый клик. На Windows можно просто подвести курсор.

Из за технических особенностей API Week **отклик таймера 1 минута**. Это означает что после включения таймера в Week или его отключения, таймер в трее реагирует через 1 минуту. Только в некоторых исключениях, может включиться быстрее.

*Важно!* Если задача закрыта, она не попадет в общее время за сегодня.

Таймер который запущен сейчас отражается в трее в виде минут. На часы не делится.

### Рабочее время
Программа имеет отдельный таймер рабочего дня, независимый от Weeek. Что бы начать отсчет рабочего времени в меню
нужно нажать Вкл. таймер раб. дня., отключить можно нажав на меню Выкл. таймер раб. дня.

Меню обновлятся через минуту.

### Возможные проблемы
1. Если API будет недоступен, например из за неверно заполненного ключа. То при клике на иконку будет отражена ошибка о недоступности API. В этом случае нужно проверить правильно ли заполнен файл settings.ini
2. Программа может запуститься с ошибкой, о том что не найдер файл картинки иконки. Это может быть, если перед запуском скрипта Вы не перешли в папку app. Запускать скрипт Python нужно от туда.
3. Обратите внимание на версию Python при запуске. У вас может быть ситуация что Python доступен только по команде Python3. В начале файла main.py есть команда #!python3 которая указывает на версию интерпритатора Python.
4. Не установлены глобально пакеты pystray Pillow requests. Тогда программа будет ругаться на их отсутсвие. Если у вас команда запуска Питона Python3, то скорее всего пактеы нужно устанавливать через pip3.
# Установка

Установите все пакеты через pip (или pip3) из файла
requirements.txt

Или установите из файла командой
```
pip install -r requirements.txt
```
или вручную
```
pip install pystray Pillow requests
```
## Конфигураяция

Для конфигурации используется файл
**settings.ini**
данный файл необходимо создать в корне папки *app*
пример оформления файла находится в **settings_demo.ini**

Заполните данные двумя ключами

**API_KEY**

Найти его можно в настройке рабочего пространства Week раздел API.
Апи выдается на каждое рабочее пространство.
[Подробнее на сайте Week](https://weeek.net/ru/help/workspace/integracii/api)

Внимание! Можноиспользовать несколько ключей от разных рабочих пространств через запятую слитно.
см. settings_demo.ini. Если нужен только один ключ, запишите его без запятой.

**ID_USER**

Данный ID нужен что бы собирать только задачи конкретного пользователя.
1. Что бы найти свой ID зайдите на сайте (не в приложении) на доску с задачами.
2. В фильтре выберете себя исполнителем
3. В аресной строке будет ссылка вида *app.weeek.net/ws/433533?assignees={ВАШ ИД}*
4. Скопируйте его в свой файл конфигурации в раздел ID_USER

## Запуск

Для запуска **обязательно** необходимо в консоли прейтие в папку *app*
И далее запустить файл main.py

```
cd {вашпуть}\app
python main.py
```
Можно создать bat-скрипт или bash-скрипт который будет запускать Таймер.
Можно поставить для удосбства в автозагрузку

Запуск без терминала (работает только на Windows)
```
cd app
python run.py
```


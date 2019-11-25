import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard
from datetime import datetime
import requests
from vk_api import VkUpload
import time
import json
import random


# ПАРСЕРЫ
from bs4 import BeautifulSoup as bs

headers = {'accept': 'image/webp,*/*', 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0'}


def img_parse(base_url,headers):
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'html.parser')
        div = soup.find_all('div', attrs={'id': 'content1'})
        for div in div:
                src = div.find('img', attrs={'id': None})['src']
    return src

# парсер 1 колонки таблицы расписания
def vavt_schedule_parse_1(check_url,headers):
    session = requests.Session()
    request = session.get(check_url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'html.parser')
        td = soup.find('td', {'width': '34%', 'valign':'top'})
        tags = td.find_all('a')
        for tag in tags:
            if tag.text == cours_name1:
                href = tag.get('href')
                return href
            elif tag.text == cours_name2:
                href = tag.get('href')
                return href

# парсер 2 колонки таблицы расписания
def vavt_schedule_parse_2(check_url,headers):
    session = requests.Session()
    request = session.get(check_url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'html.parser')
        td = soup.find('td', {'width': '33%', 'valign':'top'})
        tags = td.find_all('a')
        for tag in tags:
            if tag.text == cours_name2:
                href = tag.get('href')
                return href
            elif tag.text == cours_name1:
                href = tag.get('href')
                return href

# парсер 100 постов с Рэддита
def get_100_posts(domain):
    token = '832dc122832dc122832dc122108347de838832d832dc122df91b3ef04393e22fc459181'
    api_version = 5.92
    all_posts = []

    response = requests.get('https://api.vk.com/method/wall.get',
                 params = {
                     'access_token': token,
                     'v': api_version,
                     'domain': domain,
                     'count': 100,
                 }
                 )

    data = response.json()['response']['items']
    all_posts.extend(data)
    time.sleep(1)
    return all_posts

# парсер и рандомайзер
def pick_one_meme(data):
    list = []
    for post in data:
        try:
            if post['attachments'][0]['type']:
                img_url = post['attachments'][0]['photo']['sizes'][-1]['url']
                text = post['text']
                all_urls = {'img_url':img_url, 'text':text}
                list.append(all_urls)

            else:
                img_url = 'pass'
        except:
            pass

    random_meme = (list[random.randint(1,99)])
    return random_meme

#Для блица
Formulas = ['Стационарный временной ряд', 'Белый шум',
            'Уравнение процесса авторегрессии AR(p)',
            'Уравнение сезонной авторегрессии первого порядка SAR(1) для квартальных данных:',
            'Коррелограмма процесса AR(1):',
            'Уравнение процесса скользящего среднего MA(q):',
            'Коррелограмма процесса MA(1):',
            'Условие стационарности процесса ARMA(p,q)',
            'Условие обратимости процесса MA(q):',
            'Автокорреляция AC:', 'Частная автокорреляция PAC:',
            'Автокорреляционная функция ACF:',
            'Частная автокорреляционная функция PACF:',
            'Выборочная автокорреляционная функция SACF',
            'Выборочная частная автокорреляционная функция SPACF',
            'Оператор запаздывания:', 'Дифференцирование временного ряда',
            'Оператор дифференцирования временного ряда',
            'Временной ряд типа ARIMA(p, k, q),',
            'Передифференцированный временной ряд',
            'Эффект Слуцкого', 'Процесс случайного блуждания:',
            'Процесс случайного блуждания со сносом (дрейфом):',
            'Стохастический тренд', 'Класс TS временных рядов',
            'Класс DS временных рядов', 'Гипотеза единичного корня',
            'Информационный критерий Акаике:', 'Информационный критерий Шварца:',
            'Статистика Бокса–Пирса', 'Статистика Льюнг–Бокса',
            'Критерии Дики–Фуллера', 'Процедура Кохрейна:',
            'Коинтегрированные временные ряды',
            'Ранг коинтеграции', 'Панельные данные',
            'Сбалансированная панель', 'Модель пула',
            'Модель со случайными эффектами', 'Модель с фиксированными эффектами']


# Авторизация
token="ba4af0edc1a9fa6b9dd776c8e3e025b28197440b82e3831cde7e3b9f7aaa080f19b2edfa4960cb26fdf58"
#ТЕСТОВАЯ ГРУППА token="e147ebea3ffb3b669cb3e4349d805cf5d5a441f6853fc718d9066f1f09fe080da4feea4d5d99a9d253745"
vk_session = vk_api.VkApi(token = token)

session = requests.Session()

session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

# Создаем клавиатуру
def create_keyboard(response):
    keyboard = VkKeyboard(one_time=True)

    if response == 'доступные команды':
        return keyboard.get_empty_keyboard()
    elif response == 'хватит':
        return keyboard.get_empty_keyboard()

    keyboard = keyboard.get_keyboard()
    return keyboard


def get_button(label, color, payload=""):
    return {
        "action": {
            "type": "text",
            "payload": json.dumps(payload),
            "label": label},
        "color": color
     }


keyboard1 = {
    "one_time": True,
    "buttons": [

        [get_button(label="Инструкция", color="primary")]

        ]
    }

keyboard2 = {
    "one_time": True,
    "buttons": [

        [get_button(label="Доступные команды", color="primary")]

        ]
    }

keyboard3 = {
    "one_time": True,
    "buttons": [

        [get_button(label="Ещё", color="primary")],
        [get_button(label="Хватит", color="primary")]

        ]
    }

keyboard4 = {
    "one_time": True,
    "buttons": [

        [get_button(label="Ещё!", color="primary")],
        [get_button(label="Хватит", color="primary")]

        ]
    }

keyboard5 = {
    "one_time": True,
    "buttons": [

        [get_button(label="Ещё...", color="primary")],
        [get_button(label="Проверка", color="primary")]

        ]
    }

keyboard7 = {
    "one_time": True,
    "buttons": [

        [get_button(label="Ещёёё", color="primary")],
        [get_button(label="Хватит", color="primary")]

        ]
    }

keyboard8 = {
    "one_time": True,
    "buttons": [

        [get_button(label="Поддержка", color="primary")],
        [get_button(label="Доступные команды", color="primary")]

        ]
    }

keyboard1 = json.dumps(keyboard1, ensure_ascii=False).encode('utf-8')
keyboard2 = json.dumps(keyboard2, ensure_ascii=False).encode('utf-8')
keyboard3 = json.dumps(keyboard3, ensure_ascii=False).encode('utf-8')
keyboard4 = json.dumps(keyboard4, ensure_ascii=False).encode('utf-8')
keyboard5 = json.dumps(keyboard5, ensure_ascii=False).encode('utf-8')
keyboard7 = json.dumps(keyboard7, ensure_ascii=False).encode('utf-8')
keyboard8 = json.dumps(keyboard8, ensure_ascii=False).encode('utf-8')
keyboard1 = str(keyboard1.decode('utf-8'))
keyboard2 = str(keyboard2.decode('utf-8'))
keyboard3 = str(keyboard3.decode('utf-8'))
keyboard4 = str(keyboard4.decode('utf-8'))
keyboard5 = str(keyboard5.decode('utf-8'))
keyboard7 = str(keyboard7.decode('utf-8'))
keyboard8 = str(keyboard8.decode('utf-8'))


# ОСНОВНАЯ ЧАСТЬ БОТА
while True:
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            response = event.text.lower()
            keyboard = create_keyboard(response)
            if event.from_user and not event.from_me:
                try:
                    print('id: ' + str(event.user_id) + '   Текст сообщения: ' + str(event.text) + str(datetime.strftime(datetime.now(), "   %H:%M:%S")))
                    checker = vk_session.method('groups.isMember', {'group_id': '148978264', 'user_id': event.user_id})
                    if checker == 1:
                        if response == "начать":
                            # приветствие для Софьи
                            if event.user_id == 79247291:
                                vk_session.method('messages.send',
                                                  {'user_id': event.user_id,
                                                   'message': 'Привет, солнце 😽 \nГлянь инструкцию 😉',
                                                   'keyboard': keyboard1, 'random_id': 0})


                            else:
                                vk_session.method('messages.send',
                                                  {'user_id': event.user_id,
                                               'message': 'Приветствую! Я создан, чтобы ты всегда имел под рукой свое учебное расписание. Посмотри инструкцию к пользованию :)\nВНИМАНИЕ: бот работает в тестовом режиме!',
                                               'keyboard':keyboard1, 'random_id': 0})



                        # ФЭМ
                        elif response == "фэм1" or response == "фэм 1" or response == "фэм2" or response == "фэм 2" or response == "фэм3" or response == "фэм 3" or response == "фэм4" or response == "фэм 4" or response == "фэм1м" or response == "фэм1 м":
                            url_part = 'http://fem.vavt.ru'
                            check_url = url_part + '/schedule'

                            if response == "фэм1" or response == "фэм 1":
                                cours_name1 = '1 курс  очная форма'
                                cours_name2 = '1 курс   очная форма'
                            elif response == "фэм2" or response == "фэм 2":
                                cours_name1 = '2 курс  очная форма'
                                cours_name2 = '2 курс  очная форма'
                            elif response == "фэм3" or response == "фэм 3":
                                cours_name1 = '3 курс   очная форма'
                                cours_name2 = '3 курс  очная форма'
                            elif response == 'фэм4' or response == 'фэм 4':
                                cours_name1 = '4 курс   очная форма'
                                cours_name2 = '4 курс   очная форма'
                            elif response == "фэм1м" or response == "фэм1 м":
                                cours_name1 = '1 курс (магистратура)  '
                                cours_name2 = '1 курс (магистратура) очная форма обучения  очная форма'

                            if event.user_id == 79247291:
                                vk_session.method('messages.send',
                                              {'user_id': event.user_id, 'message': 'Секундочку 😉', 'random_id': 0})
                            else:
                                vk_session.method('messages.send',
                                                  {'user_id': event.user_id, 'message': 'Секунду...', 'random_id': 0})
                            try:
                                base_url = url_part + vavt_schedule_parse_1(check_url, headers)
                                attachments1 = []
                                upload1 = VkUpload(vk_session)
                                image_url1 = url_part + img_parse(base_url, headers)
                                image1 = session.get(image_url1, stream=True)
                                photo1 = upload1.photo_messages(photos=image1.raw)[0]
                                attachments1.append('photo{}_{}'.format(photo1['owner_id'], photo1['id']))


                                if event.user_id == 79247291:
                                    vk_session.method('messages.send',
                                                  {'user_id': event.user_id,
                                                   'message': 'Муррр 😽\nА вот и расписание на неделю:',
                                                   'attachment': attachments1, 'random_id': 0})
                                else:
                                    vk_session.method('messages.send',
                                                  {'user_id': event.user_id, 'message': 'Вуаля! Расписание на текущую неделю:',
                                                   'attachment': attachments1,
                                                   'random_id': 0})

                                vk_session.method('messages.send',
                                                  {'user_id': event.user_id,
                                                   'message': 'Проверяю сайт на наличие расписания на следующую неделю...',
                                                   'random_id': 0})
                            except:
                                pass

                            try:
                                base_url = url_part + vavt_schedule_parse_2(check_url, headers)

                                attachments2 = []
                                upload2 = VkUpload(vk_session)
                                image_url2 = url_part + img_parse(base_url, headers)
                                image2 = session.get(image_url2, stream=True)
                                photo2 = upload2.photo_messages(photos=image2.raw)[0]
                                attachments2.append('photo{}_{}'.format(photo2['owner_id'], photo2['id']))
                                vk_session.method('messages.send',
                                                  {'user_id': event.user_id, 'message': 'Нашел! Вот оно:',
                                                   'attachment': attachments2,
                                                   'random_id': 0})


                            except:
                                vk_session.method('messages.send',
                                                  {'user_id': event.user_id,
                                                   'message': 'Error 404: file not found.\nЕще не выложили:)',
                                                   'random_id': 0})


                        # МПФ
                        elif response == "мпф1" or response == "мпф 1" or response == "мпф1сп" or response == "мпф1 сп" or response == "мпф 1 сп" or \
                                response == "мпф2" or response == "мпф 2" or response == "мпф2сп" or response == "мпф2 сп" or response == "мпф 2 сп" or \
                                response == "мпф3" or response == "мпф 3" or response == "мпф3сп" or response == "мпф3 сп" or response == "мпф 3 сп" or \
                                response == 'мпф41' or response == 'мпф 41' or response == 'мпф42' or response == 'мпф 42' or response == "мпф1м" or response == "мпф1 м":
                            url_part = 'http://mpf.vavt.ru'
                            check_url = url_part + '/schedule'

                            if response == "мпф1" or response == "мпф 1":
                                cours_name1 = '1 курс  очная форма'
                                cours_name2 = '1 курс  очная форма'
                            if response == "мпф1сп" or response == "мпф1 сп" or response == "мпф 1 сп":
                                cours_name1 = '1 курс (сетевой профиль "Международно-правовой с углубленным изучением иностранного языка и права европейских организаций"  очная форма'
                                cours_name2 = '1 курс (сетевой профиль "Международно-правовой с углубленным изучением иностранного языка и права европейских организаций"   очная форма'
                            elif response == "мпф2" or response == "мпф 2":
                                cours_name1 = '2 курс  очная форма'
                                cours_name2 = '2 курс   очная форма'
                            elif response == "мпф2сп" or response == "мпф2 сп" or response == "мпф 2 сп":
                                cours_name1 = '2 курс (сетевой профиль "Международно-правовой с углубленным изучением иностранного языка и права европейских организаций"  очная форма'
                                cours_name2 = '2 курс (сетевой профиль "Международно-правовой с углубленным изучением иностранного языка и права европейских организаций")  очная форма'
                            elif response == "мпф3" or response == "мпф 3":
                                cours_name1 = '3 курс  очная форма'
                                cours_name2 = '3 курс  очная форма'
                            elif response == "мпф3сп" or response == "мпф3 сп" or response == "мпф 3 сп":
                                cours_name1 = '3 курс (сетевой профиль "международно-правовой с углубленным изучением иностранного языка и права европейских организаций)  '
                                cours_name2 = '3 курс (сетевой профиль "Международно-правовой с углубленным изучением иностранного языка и права европейских организаций"  очная форма'
                            elif response == 'мпф41' or response == 'мпф 41':
                                cours_name1 = '4 курс (1 поток)   очная форма'
                                cours_name2 = '4 курс (1 поток)   очная форма'
                            elif response == 'мпф42' or response == 'мпф 42':
                                cours_name1 = '4 курс (2 поток)  очная форма'
                                cours_name2 = '4 курс (2 поток)  очная форма'
                            elif response == "мпф1м" or response == "мпф1 м":
                                cours_name1 = '1 курс (магистратура)   очная форма'
                                cours_name2 = '1 курс (магистратура) очная форма обучения  очная форма'

                            vk_session.method('messages.send',
                                              {'user_id': event.user_id, 'message': 'Секунду...', 'random_id': 0})
                            try:
                                base_url = url_part + vavt_schedule_parse_1(check_url, headers)

                                attachments1 = []
                                upload1 = VkUpload(vk_session)
                                image_url1 = url_part + img_parse(base_url, headers)
                                image1 = session.get(image_url1, stream=True)
                                photo1 = upload1.photo_messages(photos=image1.raw)[0]
                                attachments1.append('photo{}_{}'.format(photo1['owner_id'], photo1['id']))
                                vk_session.method('messages.send',
                                                  {'user_id': event.user_id,
                                                   'message': 'Вуаля! Расписание на текущую неделю:',
                                                   'attachment': attachments1,
                                                   'random_id': 0})

                                vk_session.method('messages.send',
                                                  {'user_id': event.user_id,
                                                   'message': 'Проверяю сайт на наличие расписания на следующую неделю...',
                                                   'random_id': 0})
                            except:
                                pass

                            try:
                                base_url = url_part + vavt_schedule_parse_2(check_url, headers)

                                attachments2 = []
                                upload2 = VkUpload(vk_session)
                                image_url2 = url_part + img_parse(base_url, headers)
                                image2 = session.get(image_url2, stream=True)
                                photo2 = upload2.photo_messages(photos=image2.raw)[0]
                                attachments2.append('photo{}_{}'.format(photo2['owner_id'], photo2['id']))
                                vk_session.method('messages.send',
                                                  {'user_id': event.user_id, 'message': 'Нашел! Вот оно:',
                                                   'attachment': attachments2,
                                                   'random_id': 0})
                            except:
                                vk_session.method('messages.send',
                                                  {'user_id': event.user_id,
                                                   'message': 'Error 404: file not found.\nЕще не выложили:)',
                                                   'random_id': 0})


                        # ФВМ
                        elif response == "фвм1" or response == "фвм 1" or response == "фвм2" or response == "фвм 2" or\
                                response == "фвм3" or response == "фвм 3" or response == 'фвм4' or response == 'фвм 4' or\
                                response == 'фвм1м':
                            #url_part = 'http://fvm.vavt.ru'
                            #check_url = url_part + '/schedule'

                            if response == "фвм1" or response == "фвм 1":
                                cours_name1 = '1 курс  очная форма'
                                cours_name2 = cours_name1
                                url_part = 'http://fvm.vavt.ru'
                            elif response == "фвм2" or response == "фвм 2":
                                cours_name1 = '2 курс  очная форма'
                                cours_name2 = cours_name1
                                url_part = 'http://fvm.vavt.ru'
                            elif response == "фвм3" or response == "фвм 3":
                                cours_name1 = '3 курс  очная форма'
                                cours_name2 = cours_name1
                                url_part = 'http://fvm.vavt.ru'
                            elif response == 'фвм4' or response == 'фвм 4':
                                cours_name1 = '4 курс  очная форма'
                                cours_name2 = cours_name1
                                url_part = 'http://fvm.vavt.ru'
                            elif response == 'фвм1м':
                                cours_name1 = '1 курс  очная форма'
                                cours_name2 = '1 курс  '
                                url_part = 'http://mgm.vavt.ru'

                            check_url = url_part + '/schedule'
                            vk_session.method('messages.send',
                                              {'user_id': event.user_id, 'message': 'Секунду...', 'random_id': 0})
                            try:
                                base_url = url_part + vavt_schedule_parse_1(check_url, headers)

                                attachments1 = []
                                upload1 = VkUpload(vk_session)
                                image_url1 = url_part + img_parse(base_url, headers)
                                image1 = session.get(image_url1, stream=True)
                                photo1 = upload1.photo_messages(photos=image1.raw)[0]
                                attachments1.append('photo{}_{}'.format(photo1['owner_id'], photo1['id']))
                                vk_session.method('messages.send',
                                                  {'user_id': event.user_id, 'message': 'Вуаля! Расписание на текущую неделю:',
                                                   'attachment': attachments1,
                                                   'random_id': 0})

                                vk_session.method('messages.send',
                                                  {'user_id': event.user_id,
                                                   'message': 'Проверяю сайт на наличие расписания на следующую неделю...',
                                                   'random_id': 0})
                            except:
                                pass

                            try:
                                base_url = url_part + vavt_schedule_parse_2(check_url, headers)

                                attachments2 = []
                                upload2 = VkUpload(vk_session)
                                image_url2 = url_part + img_parse(base_url, headers)
                                image2 = session.get(image_url2, stream=True)
                                photo2 = upload2.photo_messages(photos=image2.raw)[0]
                                attachments2.append('photo{}_{}'.format(photo2['owner_id'], photo2['id']))
                                vk_session.method('messages.send',
                                                  {'user_id': event.user_id, 'message': 'Нашел! Вот оно:',
                                                   'attachment': attachments2,
                                                   'random_id': 0})
                            except:
                                vk_session.method('messages.send',
                                                  {'user_id': event.user_id,
                                                   'message': 'Error 404: file not found.\nЕще не выложили:)',
                                                   'random_id': 0})


                        # ФМФ
                        elif response == "фмф1" or response == "фмф 1" or response == "фмф2" or response == "фмф 2" or response == "фмф3" or response == "фмф 3" or response == 'фмф1м' or response == 'фмф1 м' or response == 'фмф4' or response == 'фмф 4':
                            url_part = 'http://fmf.vavt.ru'
                            check_url = url_part + '/schedule'

                            if response == "фмф1" or response == "фмф 1":
                                cours_name1 = '1 курс   очная форма'
                                cours_name2 = '1 курс  очная форма'
                            elif response == "фмф2" or response == "фмф 2":
                                cours_name1 = '2 курс  очная форма'
                                cours_name2 = '2 курс  очная форма'
                            elif response == "фмф3" or response == "фмф 3":
                                cours_name1 = '3 курс   очная форма'
                                cours_name2 = '3 курс  очная форма'
                            elif response == 'фмф4' or response == 'фмф 4':
                                cours_name1 = '4 курс  очная форма'
                                cours_name2 = '4 курс  очная форма'
                            elif response == 'фмф1м' or response == 'фмф1 м':
                                cours_name1 = '1 курс (магистратура)   '
                                cours_name2 = '1 курс (магистратура) очная форма обучения  очная форма'

                            vk_session.method('messages.send',
                                              {'user_id': event.user_id, 'message': 'Секунду...', 'random_id': 0})
                            try:
                                base_url = url_part + vavt_schedule_parse_1(check_url, headers)

                                attachments1 = []
                                upload1 = VkUpload(vk_session)
                                image_url1 = url_part + img_parse(base_url, headers)
                                image1 = session.get(image_url1, stream=True)
                                photo1 = upload1.photo_messages(photos=image1.raw)[0]
                                attachments1.append('photo{}_{}'.format(photo1['owner_id'], photo1['id']))
                                vk_session.method('messages.send',
                                                  {'user_id': event.user_id,
                                                   'message': 'Вуаля! Расписание на текущую неделю:',
                                                   'attachment': attachments1,
                                                   'random_id': 0})

                                vk_session.method('messages.send',
                                                  {'user_id': event.user_id,
                                                   'message': 'Проверяю сайт на наличие расписания на следующую неделю...',
                                                   'random_id': 0})
                            except:
                                pass

                            try:
                                base_url = url_part + vavt_schedule_parse_2(check_url, headers)

                                attachments2 = []
                                upload2 = VkUpload(vk_session)
                                image_url2 = url_part + img_parse(base_url, headers)
                                image2 = session.get(image_url2, stream=True)
                                photo2 = upload2.photo_messages(photos=image2.raw)[0]
                                attachments2.append('photo{}_{}'.format(photo2['owner_id'], photo2['id']))
                                vk_session.method('messages.send',
                                                  {'user_id': event.user_id, 'message': 'Нашел! Вот оно:',
                                                   'attachment': attachments2,
                                                   'random_id': 0})
                            except:
                                vk_session.method('messages.send',
                                                  {'user_id': event.user_id,
                                                   'message': 'Error 404: file not found.\nЕще не выложили:)',
                                                   'random_id': 0})


                        elif response == 'привет' or response == 'привет!':
                            vk_session.method('messages.send',
                                              {'user_id': event.user_id, 'message': 'Здравствуй! \nДля начала работы посмотри инструкцию.', 'keyboard': keyboard1, 'random_id': 0})

                        elif response == 'как дела' or response == 'как дела?':
                            vk_session.method('messages.send',
                                              {'user_id': event.user_id, 'message': 'Хорошо, спасибо)', 'random_id': 0})

                        elif response == 'спасибо' or response == 'спасибо!' or response == 'спасибо)' or response == 'спc':
                            vk_session.method('messages.send',
                                              {'user_id': event.user_id, 'message': 'Всегда рад помочь 😊', 'random_id': 0})

                        # поддержка
                        elif response == 'поддержка':
                            vk_session.method('messages.send',
                                              {'user_id': 146133671,
                                               'message': 'Поддержка!!! от https://vk.com/id%s' % event.user_id,
                                               'random_id': 0})
                            vk_session.method('messages.send',
                                              {'user_id': event.user_id,
                                               'message': 'Спасибо за обращение!\nС Вами скоро свяжутся.', 'random_id': 0})

                        elif response == 'инструкция':
                            vk_session.method('messages.send',
                                              {'user_id': event.user_id, 'message' :'Напиши название своего факультета и курс.\nЕсли ты учишься на МПФ, то можешь '
                                                                                    'дописать после курса "сп", и тогда откроется расписание сетевого профиля. '
                                                                                    'Для третьекурсников МПФ цифра 1 или 2 после курса означает поток.\n'
                                                                                    'Если ты магистрант, то добавь букву "м" после номера курса.\n\n'
                                                                                    'В случае, если бот работает некорректно, напиши "Поддержка".\n\n'
                                                                                    'Ты также можешь посмотреть подробный список команд, нажав на кнопку внизу или написав "Доступные команды".\n'
                                                                                    'Приятного пользования!', 'keyboard': keyboard2, 'random_id': 0})

                        elif response == 'доступные команды':
                            vk_session.method('messages.send',
                                              {'user_id': event.user_id,'message' :'Список доступных команд (бакалавриат):\n'
                                                                                    'фэм1\nфэм2\nфэм3\nфэм4\n–––––\nмпф1\nмпф1сп\nмпф2\nмпф2сп\nмпф3\nмпф3сп\nмпф41\nмпф42\n–––––\n'
                                                                                    'фвм1\nфвм2\nфвм3\nфвм4\n–––––\nфмф1\nфмф2\nфмф3\nфмф4\n\n'
                                                                                    'Список доступных команд (магистратура):\nфэм1м\nмпф1м\nфвм1м\nфмф1м\n\nОбщие команды:\nПоддержка\nИнструкция\nСпасибо', 'keyboard':keyboard,'random_id': 0})

                        elif response == 'работаешь?':
                            vk_session.method('messages.send',
                                              {'user_id': event.user_id,'message' :'Работаю.','random_id': 0})

                        elif response == 'бот' or response == 'бот?' or response == 'бот!':
                            vk_session.method('messages.send',
                                              {'user_id': event.user_id,'message' :'Что?','random_id': 0})

                        elif response == 'что делаешь' or response == 'что делаешь?' or response == 'че делаешь' or response == 'че делаешь?':
                            vk_session.method('messages.send',
                                              {'user_id': event.user_id,'message' :'Работаю.','random_id': 0})


                        elif response == '9gag' or response == 'ещё!' or response == 'еще!':
                            vk_session.method('messages.send',
                                              {'user_id': event.user_id, 'message': 'Ищу годный мемас...', 'random_id': 0})
                            all_posts = get_100_posts('ru9gag')
                            one = pick_one_meme(all_posts)
                            attachment = []
                            upload1 = VkUpload(vk_session)
                            image_url1 = one['img_url']
                            image1 = session.get(image_url1, stream=True)
                            photo1 = upload1.photo_messages(photos=image1.raw)[0]
                            attachment.append('photo{}_{}'.format(photo1['owner_id'], photo1['id']))
                            vk_session.method('messages.send',
                                              {'user_id': event.user_id, 'message': 'Лови)',
                                               'random_id': 0})
                            vk_session.method('messages.send',
                                              {'user_id': event.user_id,
                                               'message': one['text'],
                                               'keyboard': keyboard4,
                                               'attachment': attachment,
                                               'random_id': 0})
                            vk_session.method('messages.send',
                                              {'user_id': event.user_id, 'message': 'From: https://vk.com/ru9gag',
                                               'random_id': 0})


                        elif response == 'блиц' or response == 'ещё...':
                            formula_number = random.randint(0,39)
                            vk_session.method('messages.send',
                                              {'user_id': event.user_id,
                                               'message': Formulas[formula_number],
                                               'keyboard': keyboard5,
                                               'random_id': 0})

                        elif response == 'проверка':

                            vk_session.method('messages.send',
                                              {'user_id': event.user_id,
                                               'attachment': 'doc146133671_502577312',
                                               'keyboard': keyboard5,
                                               'random_id': 0})



                        elif response == 'mem' or response == 'ещёёё' or response == 'ещеее':
                            vk_session.method('messages.send',
                                              {'user_id': event.user_id, 'message': 'Ищу годный мемас...', 'random_id': 0})
                            all_posts = get_100_posts('pretty_british')
                            one = pick_one_meme(all_posts)
                            attachment = []
                            upload1 = VkUpload(vk_session)
                            image_url1 = one['img_url']
                            image1 = session.get(image_url1, stream=True)
                            photo1 = upload1.photo_messages(photos=image1.raw)[0]
                            attachment.append('photo{}_{}'.format(photo1['owner_id'], photo1['id']))
                            vk_session.method('messages.send',
                                              {'user_id': event.user_id, 'message': 'Лови)',
                                               'random_id': 0})
                            vk_session.method('messages.send',
                                              {'user_id': event.user_id,
                                               'message': one['text'],
                                               'keyboard': keyboard7,
                                               'attachment': attachment,
                                               'random_id': 0})
                            vk_session.method('messages.send',
                                              {'user_id': event.user_id, 'message': 'From: https://vk.com/pretty_british',
                                               'random_id': 0})

                        elif response == 'хватит':
                            vk_session.method('messages.send',
                                              {'user_id': event.user_id, 'message': 'Убираю клавиатуру...', 'keyboard':keyboard, 'random_id': 0})


                        else:
                            vk_session.method('messages.send',
                                              {'user_id': event.user_id, 'message': 'Я не понимаю... \nНажми "Доступные команды", чтобы увидеть список команд.','keyboard':keyboard2, 'random_id': 0})
                    else:
                        vk_session.method('messages.send',
                                      {'user_id': event.user_id,
                                       'message': 'Чтобы пользоваться ботом, необходимо быть участником сообщества https://vk.com/vavtschedulebot. Подпишитесь и нажмите "Инструкция".', 'keyboard':keyboard1, 'random_id': 0})
                    time.sleep(10)


                except Exception as e:

                    print('error', e)

                except:
                    vk_session.method('messages.send',
                                      {'user_id': event.user_id,
                                       'message': 'Ой-ой, что-то пошло не так... Возможно, это случилось из-за смены расписания на сайте ВАВТ. Попробуйте снова, а если не получится, напишите "Поддержка". Мы скоро все починим ✨', 'keyboard':keyboard8,
                                       'random_id': 0})
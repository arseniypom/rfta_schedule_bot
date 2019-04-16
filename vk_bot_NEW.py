import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard
from datetime import datetime
import requests
from vk_api import VkUpload
import time
import json


# ПАРСЕРЫ
from bs4 import BeautifulSoup as bs

headers = {'accept': 'image/webp,*/*', 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0'}
check_url = 'http://fem.vavt.ru/schedule'

def img_parse(base_url,headers):
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'html.parser')
        div = soup.find_all('div', attrs={'id': 'content1'})
        for div in div:
                src = div.find('img', attrs={'id': None})['src']
    return src

def vavt_schedule_parse_1(check_url,headers):
    session = requests.Session()
    request = session.get(check_url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'html.parser')
        td = soup.find('td', {'width': '34%', 'valign':'top'})
        tags = td.find_all('a')
        for tag in tags:
            if tag.text == cours_name:
                href = tag.get('href')
                return href


def vavt_schedule_parse_2(check_url,headers):
    session = requests.Session()
    request = session.get(check_url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'html.parser')
        td = soup.find('td', {'width': '33%', 'valign':'top'})
        tags = td.find_all('a')
        for tag in tags:
            if tag.text == cours_name:
                href = tag.get('href')
                return href


# Авторизация
token= "token"
vk_session = vk_api.VkApi(token = token)

session = requests.Session()

session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

# Создаем клавиатуру
def create_keyboard(response):
    keyboard = VkKeyboard(one_time=True)

    if response == 'доступные команды':
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


keyboard1 = json.dumps(keyboard1, ensure_ascii=False).encode('utf-8')
keyboard2 = json.dumps(keyboard2, ensure_ascii=False).encode('utf-8')
keyboard1 = str(keyboard1.decode('utf-8'))
keyboard2 = str(keyboard2.decode('utf-8'))


# ОСНОВНАЯ ЧАСТЬ БОТА
while True:
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            response = event.text.lower()
            keyboard = create_keyboard(response)

            if event.from_user and not event.from_me:
                print('id: ' + str(event.user_id) + '   Текст сообщения: ' + str(event.text) + str(datetime.strftime(datetime.now(), "   %H:%M:%S")))
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

                elif response == 'привет' or response == 'привет!':
                    vk_session.method('messages.send',
                                      {'user_id': event.user_id, 'message': 'Здравствуй! \nДля начала работы посмотри инструкцию.', 'keyboard': keyboard1, 'random_id': 0})

                elif response == 'как дела' or response == 'как дела?':
                    vk_session.method('messages.send',
                                      {'user_id': event.user_id, 'message': 'Хорошо, спасибо)', 'random_id': 0})

                elif response == 'спасибо' or response == 'спасибо!' or response == 'спасибо)' or response == 'спc':
                    vk_session.method('messages.send',
                                      {'user_id': event.user_id, 'message': 'Всегда рад помочь 😊', 'random_id': 0})


                # ФЭМ
                elif response == "фэм1" or response == "фэм 1" or response == "фэм2" or response == "фэм 2" or response == "фэм3" or response == "фэм 3" or response == "фэм1м" or response == "фэм1 м":
                    url_part = 'http://fem.vavt.ru'
                    check_url = url_part + '/schedule'

                    if response == "фэм1" or response == "фэм 1":
                        cours_name = '1 курс  очная форма'
                    elif response == "фэм2" or response == "фэм 2":
                        cours_name = '2 курс  '
                    elif response == "фэм3" or response == "фэм 3":
                        cours_name = '3 курс   очная форма'
                    #elif response == 'фэм4' or response == 'фэм 4':
                        #cours_name =
                    elif response == "фэм1м" or response == "фэм1 м":
                        cours_name = '1 курс (магистратура)  '

                    vk_session.method('messages.send',
                                      {'user_id': event.user_id, 'message': 'Секунду...', 'random_id': 0})

                    base_url = url_part + vavt_schedule_parse_1(check_url, headers)

                    attachments1 = []
                    upload1 = VkUpload(vk_session)
                    image_url1 = url_part + img_parse(base_url,headers)
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

                    try:
                        base_url = url_part + vavt_schedule_parse_2(check_url, headers)

                        attachments2 = []
                        upload2 = VkUpload(vk_session)
                        image_url2 = url_part + img_parse(base_url,headers)
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
                                           'message': 'Error 404 not found.\nЕще не выложили:)',
                                           'random_id': 0})

                # МПФ
                elif response == "мпф1" or response == "мпф 1" or response == "мпф1сп" or response == "мпф1 сп" or response == "мпф 1 сп" or \
                        response == "мпф2" or response == "мпф 2" or response == "мпф2сп" or response == "мпф2 сп" or response == "мпф 2 сп" or \
                        response == "мпф31" or response == "мпф 31" or response == "мпф32" or response == "мпф 32" or response == 'мпф4' or \
                        response == 'мпф 4' or response == "мпф1м" or response == "мпф1 м":
                    url_part = 'http://mpf.vavt.ru'
                    check_url = url_part + '/schedule'
                    if response == "мпф1" or response == "мпф 1":
                        cours_name = '1 курс  очная форма'
                    if response == "мпф1сп" or response == "мпф1 сп" or response == "мпф 1 сп":
                        cours_name = '1 курс (сетевой профиль "Международно-правовой с углубленным изучением иностранного языка и права европейских организаций"  очная форма'
                    elif response == "мпф2" or response == "мпф 2":
                        cours_name = '2 курс  очная форма'
                    elif response == "мпф2сп" or response == "мпф2 сп" or response == "мпф 2 сп":
                        cours_name = '2 курс (сетевой профиль "Международно-правовой с углубленным изучением иностранного языка и права европейских организаций"  очная форма'
                    elif response == "мпф31" or response == "мпф 31":
                        cours_name = '3 курс (1 поток) очная форма  '
                    elif response == "мпф32" or response == "мпф 32":
                        cours_name = '3 курс (2 поток) очная форма  '
                    #elif response == 'мпф4' or response == 'мпф 4':
                        #cours_name =
                    elif response == "мпф1м" or response == "мпф1 м":
                        cours_name = '1 курс (магистратура)   очная форма'

                    vk_session.method('messages.send',
                                      {'user_id': event.user_id, 'message': 'Секунду...', 'random_id': 0})
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
                                           'message': 'Error 404 not found.\nЕще не выложили:)',
                                           'random_id': 0})

                # ФВМ
                elif response == "фвм1" or response == "фвм 1" or response == "фвм2" or response == "фвм 2" or response == "фвм3" or response == "фвм 3" or response == 'фвм4' or response == 'фвм 4':
                    url_part = 'http://fvm.vavt.ru'
                    check_url = url_part + '/schedule'
                    if response == "фвм1" or response == "фвм 1":
                        cours_name = '1 курс  очная форма'
                    elif response == "фвм2" or response == "фвм 2":
                        cours_name = '2 курс  очная форма'
                    elif response == "фвм3" or response == "фвм 3":
                        cours_name = '3 курс  очная форма'
                    #elif response == 'фвм4' or response == 'фвм 4':
                        #cours_name =

                    vk_session.method('messages.send',
                                      {'user_id': event.user_id, 'message': 'Секунду...', 'random_id': 0})
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
                                           'message': 'Error 404 not found.\nЕще не выложили:)',
                                           'random_id': 0})


                # ФМФ
                elif response == "фмф1" or response == "фмф 1" or response == "фмф2" or response == "фмф 2" or response == "фмф3" or response == "фмф 3" or response == 'фмф1м' or response == 'фмф1 м' or response == 'фмф4' or response == 'фмф 4':
                    url_part = 'http://fmf.vavt.ru'
                    check_url = url_part + '/schedule'
                    if response == "фмф1" or response == "фмф 1":
                        cours_name = '1 курс   очная форма'
                    elif response == "фмф2" or response == "фмф 2":
                        cours_name = '2 курс  очная форма'
                    elif response == "фмф3" or response == "фмф 3":
                        cours_name = '3 курс   очная форма'
                    #elif response == 'фмф4' or response == 'фмф 4':
                        #cours_name =
                    elif response == 'фмф1м' or response == 'фмф1 м':
                        cours_name = '1 курс (магистратура)   '

                    vk_session.method('messages.send',
                                      {'user_id': event.user_id, 'message': 'Секунду...', 'random_id': 0})
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
                                           'message': 'Error 404 not found.\nЕще не выложили:)',
                                           'random_id': 0})



                elif response == 'инструкция':
                    vk_session.method('messages.send',
                                      {'user_id': event.user_id, 'message' :'Напиши название своего факультета и курс.\nЕсли ты учишься на МПФ, то можешь '
                                                                            'дописать после курса "сп", и тогда откроется расписание сетевого профиля. '
                                                                            'Для третьекурсников МПФ цифра 1 или 2 после курса означает поток.\n'
                                                                            'Если ты магистрант, то добавь букву "м" после номера курса.\n'
                                                                            'Ты так же можешь посмотреть подробный список команд, нажав на кнопку внизу или написав "Доступные команды".\n'
                                                                            'Приятного пользования!', 'keyboard': keyboard2, 'random_id': 0})

                elif response == 'доступные команды':
                    vk_session.method('messages.send',
                                      {'user_id': event.user_id,'message' :'Список доступных команд (бакалавриат):\n'
                                                                            'фэм1\nфэм2\nфэм3\n–––––\nмпф1\nмпф1сп\nмпф2\nмпф2сп\nмпф31\nмпф32\n –––––\n'
                                                                            'фвм1\nфвм2\nфвм3\n–––––\nфмф1\nфмф2\nфмф3\n\n'
                                                                            'Список доступных команд (магистратура):\nфэм1м\nмпф1м\nфмф1м', 'keyboard':keyboard,'random_id': 0})

                elif response == 'работаешь?':
                    vk_session.method('messages.send',
                                      {'user_id': event.user_id,'message' :'Работаю.','random_id': 0})

                elif response == 'бот' or response == 'бот?' or response == 'бот!':
                    vk_session.method('messages.send',
                                      {'user_id': event.user_id,'message' :'Что?','random_id': 0})

                elif response == 'что делаешь' or response == 'что делаешь?' or response == 'че делаешь' or response == 'че делаешь?':
                    vk_session.method('messages.send',
                                      {'user_id': event.user_id,'message' :'Работаю.','random_id': 0})

                else:
                    vk_session.method('messages.send',
                                      {'user_id': event.user_id, 'message': 'Я не понимаю... \nНажми "Доступные команды", чтобы увидеть список команд.','keyboard':keyboard2, 'random_id': 0})
            time.sleep(1)
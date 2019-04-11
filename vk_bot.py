import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard
from datetime import datetime
import requests
from vk_api import VkUpload
import time
import json


# ПАРСЕР
from bs4 import BeautifulSoup as bs

headers = {'accept': 'image/webp,*/*', 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0'}

def vavt_parse(base_url,headers):
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'html.parser')
        div = soup.find_all('div', attrs={'id': 'content1'})
        for div in div:
                src = div.find('img', attrs={'id': None})['src']
    return src


# Авторизация
token= "093cec9b35649097590a75cab9a1765ca8e6441c274374015e8122fd5cf77b32d267588f3368743e35453"
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

                elif response == 'привет':
                    vk_session.method('messages.send',
                                      {'user_id': event.user_id, 'message': 'Здравствуй! \nДля начала работы посмотри инструкцию.', 'keyboard': keyboard1, 'random_id': 0})

                elif response == 'спасибо' or response == 'спасибо!' or response == 'спасибо)' or response == 'спc':
                    vk_session.method('messages.send',
                                      {'user_id': event.user_id, 'message': 'Всегда рад помочь 😊', 'random_id': 0})


                # ФЭМ
                elif response == "фэм1" or response == "фэм 1" or response == "фэм2" or response == "фэм 2" or response == "фэм3" or response == "фэм 3" or response == "фэм1м" or response == "фэм1 м":
                    url_part = 'http://fem.vavt.ru'
                    if response == "фэм1" or response == "фэм 1":
                        base_url1 = 'http://fem.vavt.ru/schedule/by_id/fem_4_12_1'
                        #base_url2 =
                    elif response == "фэм2" or response == "фэм 2":
                        base_url1 = 'http://fem.vavt.ru/schedule/by_id/fbfbf'
                        #base_url2 =
                    elif response == "фэм3" or response == "фэм 3":
                        base_url1 = 'http://fem.vavt.ru/wred/schedule.nsf/by_id/fem3-1'
                        #base_url2 =
                    #elif response == 'фэм4' or response == 'фэм 4':
                        #base_url1 = None
                        #base_url2 =
                    elif response == "фэм1м" or response == "фэм1 м":
                        base_url1 = 'http://fem.vavt.ru/schedule/by_id/saochka'
                        #base_url2 =

                    vk_session.method('messages.send',
                                      {'user_id': event.user_id, 'message': 'Секунду...', 'random_id': 0})
                    attachments1 = []
                    #attachments2 = []
                    upload1 = VkUpload(vk_session)
                    #upload2 = VkUpload(vk_session)
                    image_url1 = url_part + vavt_parse(base_url1, headers)
                    #image_url2 = url_part + vavt_parse(base_url2, headers)
                    image1 = session.get(image_url1, stream=True)
                    #image2 = session.get(image_url2, stream=True)
                    photo1 = upload1.photo_messages(photos=image1.raw)[0]
                    #photo2 = upload2.photo_messages(photos=image2.raw)[0]
                    attachments1.append('photo{}_{}'.format(photo1['owner_id'], photo1['id']))
                    #attachments2.append('photo{}_{}'.format(photo2['owner_id'], photo2['id']))
                    vk_session.method('messages.send',
                                      {'user_id': event.user_id, 'message': 'Вуаля!', 'attachment': attachments1,
                                       'random_id': 0})
                    #vk_session.method('messages.send',
                                      #{'user_id': event.user_id, 'attachment': attachments2,
                                      # 'random_id': 0})

                # МПФ
                elif response == "мпф1" or response == "мпф 1" or response == "мпф1сп" or response == "мпф1 сп" or response == "мпф 1 сп" or \
                        response == "мпф2" or response == "мпф 2" or response == "мпф2сп" or response == "мпф2 сп" or response == "мпф 2 сп" or \
                        response == "мпф31" or response == "мпф 31" or response == "мпф32" or response == "мпф 32" or response == 'мпф4' or \
                        response == 'мпф 4' or response == "мпф1м" or response == "мпф1 м":
                    url_part = 'http://mpf.vavt.ru'
                    if response == "мпф1" or response == "мпф 1":
                        base_url1 = 'http://mpf.vavt.ru/schedule/by_id/mpf1_14_10'
                        #base-url2 =
                    elif response == "мпф2" or response == "мпф 2":
                        base_url1 = 'http://mpf.vavt.ru/schedule/by_id/mpf_4_13'
                        #base_url2 =
                    elif response == "мпф2сп" or response == "мпф2 сп" or response == "мпф 2 сп":
                        base_url1 = 'http://mpf.vavt.ru/schedule/by_id/,l,;l'
                        #base_url2 =
                    elif response == "мпф31" or response == "мпф 31":
                        base_url1 = 'http://mpf.vavt.ru/schedule/by_id/mpf_5_12'
                        #base_url2 =
                    elif response == "мпф32" or response == "мпф 32":
                        base_url1 = 'http://mpf.vavt.ru/schedule/by_id/mpf_3_13'
                        #base_url2 =
                    #elif response == 'мпф4' or response == 'мпф 4':
                        #base_url1 = None
                        #base_url2 =
                    elif response == "мпф1м" or response == "мпф1 м":
                        base_url1 = 'http://mpf.vavt.ru/schedule/by_id/axaxa'
                        #base_url2 =

                    vk_session.method('messages.send',
                                      {'user_id': event.user_id, 'message': 'Секунду...', 'random_id': 0})
                    attachments1 = []
                    # attachments2 = []
                    upload1 = VkUpload(vk_session)
                    # upload2 = VkUpload(vk_session)
                    image_url1 = url_part + vavt_parse(base_url1, headers)
                    # image_url2 = url_part + vavt_parse(base_url2, headers)
                    image1 = session.get(image_url1, stream=True)
                    # image2 = session.get(image_url2, stream=True)
                    photo1 = upload1.photo_messages(photos=image1.raw)[0]
                    # photo2 = upload2.photo_messages(photos=image2.raw)[0]
                    attachments1.append('photo{}_{}'.format(photo1['owner_id'], photo1['id']))
                    # attachments2.append('photo{}_{}'.format(photo2['owner_id'], photo2['id']))
                    vk_session.method('messages.send',
                                      {'user_id': event.user_id, 'message': 'Вуаля!', 'attachment': attachments1,
                                       'random_id': 0})
                    # vk_session.method('messages.send',
                    # {'user_id': event.user_id, 'attachment': attachments2,
                    # 'random_id': 0})

                # ФВМ
                elif response == "фвм1" or response == "фвм 1" or response == "фвм2" or response == "фвм 2" or response == "фвм3" or response == "фвм 3" or response == 'фвм4' or response == 'фвм 4':
                    url_part = 'http://fvm.vavt.ru'
                    if response == "фвм1" or response == "фвм 1":
                        base_url1 = 'http://fvm.vavt.ru/schedule/by_id/fvm1_1712_2112'
                        #base_url2 =
                    elif response == "фвм2" or response == "фвм 2":
                        base_url1 = 'http://fvm.vavt.ru/schedule/by_id/fvm_2_1712_2112'
                        #base_url2 =
                    elif response == "фвм3" or response == "фвм 3":
                        base_url1 = 'http://fvm.vavt.ru/schedule/by_id/fvm_3_1012_0712'
                        #base_url2 =
                    #elif response == 'фвм4' or response == 'фвм 4':
                        #base_url1 = None
                        #base_url2 =

                    vk_session.method('messages.send',
                                      {'user_id': event.user_id, 'message': 'Секунду...', 'random_id': 0})
                    attachments1 = []
                    # attachments2 = []
                    upload1 = VkUpload(vk_session)
                    # upload2 = VkUpload(vk_session)
                    image_url1 = url_part + vavt_parse(base_url1, headers)
                    # image_url2 = url_part + vavt_parse(base_url2, headers)
                    image1 = session.get(image_url1, stream=True)
                    # image2 = session.get(image_url2, stream=True)
                    photo1 = upload1.photo_messages(photos=image1.raw)[0]
                    # photo2 = upload2.photo_messages(photos=image2.raw)[0]
                    attachments1.append('photo{}_{}'.format(photo1['owner_id'], photo1['id']))
                    # attachments2.append('photo{}_{}'.format(photo2['owner_id'], photo2['id']))
                    vk_session.method('messages.send',
                                      {'user_id': event.user_id, 'message': 'Вуаля!', 'attachment': attachments1,
                                       'random_id': 0})
                    # vk_session.method('messages.send',
                    # {'user_id': event.user_id, 'attachment': attachments2,
                    # 'random_id': 0})


                # ФМФ
                elif response == "фмф1" or response == "фмф 1" or response == "фмф2" or response == "фмф 2" or response == "фмф3" or response == "фмф 3" or response == 'фмф1м' or response == 'фмф1 м' or response == 'фмф4' or response == 'фмф 4':
                    url_part = 'http://fmf.vavt.ru'
                    if response == "фмф1" or response == "фмф 1":
                        base_url1 = 'http://fmf.vavt.ru/schedule/by_id/wsaea'
                        #base_url2 =
                    elif response == "фмф2" or response == "фмф 2":
                        base_url1 = 'http://fmf.vavt.ru/schedule/by_id/adad'
                        # base_url2 =
                    elif response == "фмф3" or response == "фмф 3":
                        base_url1 = 'http://fmf.vavt.ru/schedule/by_id/j,j,'
                        # base_url2 =
                    #elif response == 'фмф4' or response == 'фмф 4':
                        #base_url1 = None
                        #base_url2 =
                    elif response == 'фмф1м' or response == 'фмф1 м':
                        base_url1 = 'http://fmf.vavt.ru/schedule/by_id/fmf1_12'
                        # base_url2 =

                    vk_session.method('messages.send',
                                      {'user_id': event.user_id, 'message': 'Секунду...', 'random_id': 0})
                    attachments1 = []
                    # attachments2 = []
                    upload1 = VkUpload(vk_session)
                    # upload2 = VkUpload(vk_session)
                    image_url1 = url_part + vavt_parse(base_url1, headers)
                    # image_url2 = url_part + vavt_parse(base_url2, headers)
                    image1 = session.get(image_url1, stream=True)
                    # image2 = session.get(image_url2, stream=True)
                    photo1 = upload1.photo_messages(photos=image1.raw)[0]
                    # photo2 = upload2.photo_messages(photos=image2.raw)[0]
                    attachments1.append('photo{}_{}'.format(photo1['owner_id'], photo1['id']))
                    # attachments2.append('photo{}_{}'.format(photo2['owner_id'], photo2['id']))
                    vk_session.method('messages.send',
                                      {'user_id': event.user_id, 'message': 'Вуаля!', 'attachment': attachments1,
                                       'random_id': 0})
                    # vk_session.method('messages.send',
                    # {'user_id': event.user_id, 'attachment': attachments2,
                    # 'random_id': 0})

                elif response == 'инструкция':
                    vk_session.method('messages.send',
                                      {'user_id': event.user_id, 'message' :'Напиши название своего факультета и курс.\n Если ты учишься на МПФ, для тебя также доступны'
                                                                            'другие команды, например, если дописать после курса "сп", то откроется расписание сетевого профиля.'
                                                                            'Для третьекурсников МПФ цифра 1 или 2 после курса означает поток.\n'
                                                                            'Если ты магистрант, то добавь букву "м" после номера курса.\n'
                                                                            'Ты так же можешь посмотреть подробный список команд, нажав на кнопку внизу или написав "Доступные команды".\n'
                                                                            'Приятного пользования!', 'keyboard': keyboard2, 'random_id': 0})

                elif response == 'доступные команды':
                    vk_session.method('messages.send',
                                      {'user_id': event.user_id,'message' :'Список доступных команд (бакалавриат):\n'
                                                                            'фэм1\nфэм2\nфэм3\n–––––\nмпф1\nмпф1сп\nмпф2\nмпф2сп\nмпф31\nмпф32\n –––––\n'
                                                                            'фвм1\nфвм2\nфвм3\n–––––\nфмф1\nфмф2\nфмф3\n'
                                                                            'Список доступных команд (магистратура):\nфэм1м\nмпф1м\nфмф1м', 'keyboard':keyboard,'random_id': 0})

                else:
                    vk_session.method('messages.send',
                                      {'user_id': event.user_id, 'message': 'Я не понимаю... \nНажми "Доступные команды", чтобы увидеть список команд.','keyboard':keyboard2, 'random_id': 0})
            time.sleep(1)
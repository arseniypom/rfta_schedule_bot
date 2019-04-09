from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import vk_api
from datetime import datetime
import requests
from vk_api import VkUpload
import time


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
    if response == 'начать':
        keyboard.add_button('Инструкция', color=VkKeyboardColor.PRIMARY)
    elif response == 'инструкция':
        return keyboard.get_empty_keyboard()

    keyboard = keyboard.get_keyboard()
    return keyboard

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
                                           'keyboard': keyboard, 'random_id': 0})
                    else:
                        vk_session.method('messages.send',
                                      {'user_id': event.user_id, 'message': 'Приветствую! Я создан, чтобы ты всегда имел под рукой свое учебное расписание. Посмотри инструкцию к пользованию :) '
                                                                            '\nВНИМАНИЕ: бот работает в тестовом режиме!', 'keyboard': keyboard, 'random_id': 0})

                elif response == 'привет':
                    vk_session.method('messages.send',
                                      {'user_id': event.user_id, 'message': 'Здравствуй! \nДля начала работы напиши "начать"', 'random_id': 0})

                elif response == 'спасибо' or response == 'спасибо!':
                    vk_session.method('messages.send',
                                      {'user_id': event.user_id, 'message': 'Всегда рад помочь 😊', 'random_id': 0})


                # ФЭМ
                elif response == "фэм1" or response == "фэм 1" or response == "фэм2" or response == "фэм 2" or response == "фэм3" or response == "фэм 3" or response == "фэм1м" or response == "фэм1 м":
                    url_part = 'http://fem.vavt.ru'
                    if response == "фэм1" or response == "фэм 1":
                        base_url = 'http://fem.vavt.ru/schedule/by_id/fem_4_12_1'
                    elif response == "фэм2" or response == "фэм 2":
                        base_url = 'http://fem.vavt.ru/schedule/by_id/fbfbf'
                    elif response == "фэм3" or response == "фэм 3":
                        base_url = 'http://fem.vavt.ru/wred/schedule.nsf/by_id/fem3-1'
                    elif response == "фэм1м" or response == "фэм1 м":
                        base_url = 'http://fem.vavt.ru/schedule/by_id/saochka'

                    vk_session.method('messages.send',
                                      {'user_id': event.user_id, 'message': 'Секунду...', 'random_id': 0})
                    attachments = []
                    upload = VkUpload(vk_session)
                    image_url = url_part + vavt_parse(base_url, headers)
                    image = session.get(image_url, stream=True)
                    photo = upload.photo_messages(photos=image.raw)[0]
                    attachments.append('photo{}_{}'.format(photo['owner_id'], photo['id']))
                    vk_session.method('messages.send',
                                      {'user_id': event.user_id, 'message': 'Вуаля!', 'attachment': attachments,
                                       'random_id': 0})

                # МПФ
                elif response == "мпф1" or response == "мпф 1" or response == "мпф1сп" or response == "мпф1 сп" or response == "мпф 1 сп" or \
                        response == "мпф2" or response == "мпф 2" or response == "мпф2сп" or response == "мпф2 сп" or response == "мпф 2 сп" or \
                        response == "мпф31" or response == "мпф 31" or response == "мпф32" or response == "мпф 32" or response == "мпф1м" or response == "мпф1 м":
                    url_part = 'http://mpf.vavt.ru'
                    if response == "мпф1" or response == "мпф 1":
                        base_url = 'http://mpf.vavt.ru/schedule/by_id/mpf1_14_10'
                    elif response == "мпф1сп" or response == "мпф1 сп" or response == "мпф 1 сп":
                        base_url = 'http://mpf.vavt.ru/schedule/by_id/mpf4_03_14'
                    elif response == "мпф2" or response == "мпф 2":
                        base_url = 'http://mpf.vavt.ru/schedule/by_id/mpf_4_13'
                    elif response == "мпф2сп" or response == "мпф2 сп" or response == "мпф 2 сп":
                        base_url = 'http://mpf.vavt.ru/schedule/by_id/,l,;l'
                    elif response == "мпф31" or response == "мпф 31":
                        base_url = 'http://mpf.vavt.ru/schedule/by_id/mpf_5_12'
                    elif response == "мпф32" or response == "мпф 32":
                        base_url = 'http://mpf.vavt.ru/schedule/by_id/mpf_3_13'
                    elif response == "мпф1м" or response == "мпф1 м":
                        base_url = 'http://mpf.vavt.ru/schedule/by_id/axaxa'

                    vk_session.method('messages.send',
                                      {'user_id': event.user_id, 'message': 'Секунду...', 'random_id': 0})
                    attachments = []
                    upload = VkUpload(vk_session)
                    image_url = url_part + vavt_parse(base_url, headers)
                    image = session.get(image_url, stream=True)
                    photo = upload.photo_messages(photos=image.raw)[0]
                    attachments.append('photo{}_{}'.format(photo['owner_id'], photo['id']))
                    vk_session.method('messages.send',
                                      {'user_id': event.user_id, 'message': 'Вуаля!', 'attachment': attachments,
                                       'random_id': 0})

                # ФВМ
                elif response == "фвм1" or response == "фвм 1" or response == "фвм2" or response == "фвм 2" or response == "фвм3" or response == "фвм 3":
                    url_part = 'http://fvm.vavt.ru'
                    if response == "фвм1" or response == "фвм 1":
                        base_url = 'http://fvm.vavt.ru/schedule/by_id/fvm1_1712_2112'
                    elif response == "фвм2" or response == "фвм 2":
                        base_url = 'http://fvm.vavt.ru/schedule/by_id/fvm_2_1712_2112'
                    elif response == "фвм3" or response == "фвм 3":
                        base_url = 'http://fvm.vavt.ru/schedule/by_id/fvm_3_1012_0712'

                    vk_session.method('messages.send',
                                      {'user_id': event.user_id, 'message': 'Секунду...', 'random_id': 0})
                    attachments = []
                    upload = VkUpload(vk_session)
                    image_url = url_part + vavt_parse(base_url, headers)
                    image = session.get(image_url, stream=True)
                    photo = upload.photo_messages(photos=image.raw)[0]
                    attachments.append('photo{}_{}'.format(photo['owner_id'], photo['id']))
                    vk_session.method('messages.send',
                                      {'user_id': event.user_id, 'message': 'Вуаля!', 'attachment': attachments,
                                       'random_id': 0})


                # ФМФ
                elif response == "фмф1" or response == "фмф 1" or response == "фмф2" or response == "фмф 2" or response == "фмф3" or response == "фмф 3" or response == 'фмф1м' or response == 'фмф1 м':
                    url_part = 'http://fmf.vavt.ru'
                    if response == "фмф1" or response == "фмф 1":
                        base_url = 'http://fmf.vavt.ru/schedule/by_id/wsaea'
                    elif response == "фмф2" or response == "фмф 2":
                        base_url = 'http://fmf.vavt.ru/schedule/by_id/adad'
                    elif response == "фмф3" or response == "фмф 3":
                        base_url = 'http://fmf.vavt.ru/schedule/by_id/j,j,'
                    elif response == 'фмф1м' or response == 'фмф1 м':
                        base_url = 'http://fmf.vavt.ru/schedule/by_id/fmf1_12'

                    vk_session.method('messages.send',
                                      {'user_id': event.user_id, 'message': 'Секунду...', 'random_id': 0})
                    attachments = []
                    upload = VkUpload(vk_session)
                    image_url = url_part + vavt_parse(base_url, headers)
                    image = session.get(image_url, stream=True)
                    photo = upload.photo_messages(photos=image.raw)[0]
                    attachments.append('photo{}_{}'.format(photo['owner_id'], photo['id']))
                    vk_session.method('messages.send',
                                      {'user_id': event.user_id, 'message': 'Вуаля!', 'attachment': attachments,
                                       'random_id': 0})

                elif response == 'инструкция':
                    vk_session.method('messages.send',
                                      {'user_id': event.user_id, 'message' :'Напиши название своего факультета и курс. \nНапример: фэм3 '
                                                                            '\nЕсли ты учишься в магистратуре, добавь в конце букву "м". \nНапример: фэм1м', 'keyboard': keyboard, 'random_id': 0})
                else:
                    vk_session.method('messages.send',
                                      {'user_id': event.user_id, 'message': 'Я не понимаю... \nДля начала работы напиши "начать"', 'random_id': 0})
            time.sleep(1)
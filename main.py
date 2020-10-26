import vk_api, json, random, pymysql
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
import requests


vk_session  = vk_api.VkApi(token = "")
vk          = vk_session.get_api()
longpoll    = VkLongPoll(vk_session)

def sender (id, text):
    vk.messages.send(user_id = id, message = text, random_id = 0, keyboard = keyboard)

def send_stick (id, number):
    vk.messages.send(user_id = id, sticker_id = number, random_id = 0)

def send_foto (id, url):
    vk.messages.send(user_id = id, attachment = url, random_id = 0)

def send_video (id, url):
    vk.messages.send(user_id = id, attachment = url, random_id = 0)

def read_from_txt ():
    with open ('rand_answer.txt', 'r', encoding='utf-8') as file:
        x = file.readlines()
        print(x[3])

def adder (x):
    file = open('data.txt', 'a',encoding='utf-8')
    file.write(f'{x}\n')
    file.close()

def check (x):
    file = open('data.txt', 'r',encoding='utf-8')
    if str(x) in file.read():
        return 1
    else:
        return 0
    file.close()

def get_but(text, color):
    return {
        "action": {
            "type": "text",
            "payload": "{\"buttom\": \"" + "1" + "\"}",
            "label": f"{text}"
        },
        "color": f"{color}"
    }

keyboard = {
    "one_time": True,
    "buttons": [
        [get_but('Помощь', 'secondary')],
        [get_but('Да', 'positive')],
        [get_but('Нет', 'negative')]
    ]
}
keyboard = json.dumps(keyboard,ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))


def get_keyboard():
    keyboard = {
        "one_time": True,
        "buttons": [
            [get_but('Помощь', 'secondary')],
            [get_but('Да', 'positive')],
            [get_but('Нет', 'negative')]
        ]
    }
    keyboard = json.dumps(keyboard,ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))

    return keyboard


keyboard2 = {
    "one_time": True,
    "buttons": [
        [get_but('ДА', 'positive')],
        [get_but('Нет', 'negative')]
    ]
}
keyboard2 = json.dumps(keyboard2,ensure_ascii=False).encode('utf-8')
keyboard2 = str(keyboard2.decode('utf-8'))


def get_connection():
    connection = pymysql.connect(host='you_host',
                                 user='you_user',
                                 password='you_password',
                                 db='you_db',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection



unanswered = vk_session.method("messages.getConversations",{"filter":"unanswered"})
def check_unanswered():
    if  unanswered["count"] >= 1 :
        id = unanswered['items'][0]['last_message']['from_id']
        sender(id, 'Прости, я спал. Что ты хотел?')


#########################################
#Подключим новый модуль random
import random
def random_mode():
    #Получаем рандомное число в районе от 1 до 200
    return random.choice(["Live","Dead"])

def add_to_database(function_mode, x):
    #Создаем новую сессию
    connection = get_connection()
    #Будем получать информацию от сюда
    cursor = connection.cursor()
    #Наш запрос
    sql = "INSERT INTO mode (Id_User, Mode) VALUES (%s, %s) ON DUPLICATE KEY UPDATE Mode = %s"
    #Выполняем наш запрос и вставляем свои значения
    cursor.execute(sql, (x, function_mode, function_mode))
    #Делаем коммит
    connection.commit()
    #Закрываем подключение
    connection.close()
    #Возвращаем результат
    return function_mode
###########################################



def main():

    for event in longpoll.listen() :

        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:

                id = event.user_id
                msg = event.text.lower()

                if msg == 'привет' :
                    add_to_database(random_mode(), id)

                if msg == 'помощь':
                    sender(id, 'Смотри что я умею 	&#128522;')
                    send_stick(id, 64)
                    read_from_txt()


                if (msg != 'привет' and msg != 'помощь'):
                    sender(id, 'Помнишь, как в одном из фильмов про негра и роботов: \n Извини, в ответах я ограничен. Правильно задавай вопросы')
                    send_video(id, 'video-35875205_456240291')
                    # sender(id, msg.upper())
while True:
    check_unanswered()
    main()




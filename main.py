import vk_api, json, random, pymysql
import config
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
import requests


vk_session  = vk_api.VkApi(token = config.TOKEN)
vk          = vk_session.get_api()
longpoll    = VkLongPoll(vk_session)

def sender (id, text):
    vk.messages.send(user_id = id, message = text, random_id = get_random_id(), keyboard = keyboard)

def send_stick (id, number):
    vk.messages.send(user_id = id, sticker_id = number, random_id = get_random_id())

def send_foto (id, url):
    vk.messages.send(user_id = id, attachment = url, random_id = get_random_id())

def send_video (id, url):
    vk.messages.send(user_id = id, attachment = url, random_id = get_random_id())

def read_from_txt ():
    with open ('rand_answer.txt', 'r', encoding='utf-8') as file:
        x = file.readlines()
        answer = x[random.randint(0,3)]
        return answer


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

###########################################

unanswered = vk_session.method("messages.getConversations",{"filter":"unanswered"})
def check_unanswered():
    if  unanswered["count"] >= 1 :
        id = unanswered['items'][0]['last_message']['from_id']
        sender(id, 'Прости, я спал. Что ты хотел?')


#########################################
###########################################



def main():

    for event in longpoll.listen() :

        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:

                id = event.user_id
                msg = event.text.lower()


                if msg == 'помощь':
                    send_stick(id, 64)
                    sender(id, read_from_txt())


                if (msg != 'привет' and msg != 'помощь'):
                    sender(id, 'Помнишь, как в одном из фильмов про негра и роботов: \n Извини, в ответах я ограничен. Правильно задавай вопросы')
                    send_video(id, 'video-35875205_456240291')

while True:
    check_unanswered()
    main()




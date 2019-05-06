from flask import Flask, request
import logging
import random
import json
import pprint

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, filename='/home/margis902/mysite/app.log', #записываю логи
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')

with open("/home/margis902/mysite/tests wrong.json", "r", ) as read_file:
    info_i = json.load(read_file)
sessionStorage = {}


sessionStorage = {}


@app.route('/', methods=['POST'])
def main():
    logging.info('Request: %r', request.json)
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(response, request.json)
    logging.info('Request: %r', response)
    return json.dumps(response)

def handle_dialog(res, req):
    user_id = req['session']['user_id']
    res['response']['buttons'] = []

    if req['session']['new']:      #дружественный интерфейс так сказать
        res['response']['text'] = 'Привет! Назови свое имя!'
        sessionStorage[user_id] = {
            'first_name': None
        }
        return
    if sessionStorage[user_id]['first_name'] is None:           #ищем имя.
        first_name = get_first_name(req)

        if first_name is None:                # если не нашли, то сообщаем пользователю что не расслышали.
            res['response']['text'] = \
                'Не расслышала имя. Повтори, пожалуйста!'
        # если нашли, то приветствуем пользователя.
        # И спрашиваем какой город он хочет увидеть.
        else:
            sessionStorage[user_id]['first_name'] = first_name
            res['response'][
                'text'] = 'Приятно познакомиться, ' + first_name.title() \
                          + '. Начинаем'
            # получаем варианты buttons из ключей нашего словаря cities
            res['response']['buttons'] = [
                {
                    'title': city.title(),
                    'hide': True
                } for city in cities
            ]

    if req['session']['new']:
        res['response']['text'] = \
            'Привет начинающий программист. Этот тест проверит твоё умение читать простейший код. Если хочешь узнать ещё, ты только спроси'
        res['response']['buttons'].extend(info_i["buttons"]['mainmenu'])
        sessionStorage[user_id] = {
            'steps': 0
        }
        return
    if sessionStorage[user_id]['steps'] == 0:
        res['response']['buttons'].extend(info_i["buttons"]['mainmenu'])
    if 'помощь' in list(map(lambda x: x.lower(), req['request']['nlu']["tokens"])):
        res['response'][
            'text'] = 'Тест Рейвена включает в себя 60 впросов. Время на решение заданий ограничено 20 минутами.' \
                      ' Расчитан для людей возрастом от 8 до 65 лет. Все результаты приблизительны.'
    return


def get_first_name(req):
    for entity in req['request']['nlu']['entities']:
        if entity['type'] == 'YANDEX.FIO':
            return entity['value'].get('first_name', None)

def get_text(num): #функция дающая текст
    if num >= 0 and num <= 8:
        return ['tests'][str(num)]
    else:
        if num < 0:
            return info_i['tests']['0']
        else:
            return info_i['history']['8']

def true_ans(num)


if __name__ == '__main__':
    app.run()
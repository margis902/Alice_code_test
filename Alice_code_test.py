from flask import Flask, request
import logging
import json

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, filename='/home/margis902/mysite/app.log')

with open("/home/margis902/mysite/lessons.json", "r", ) as read_file:
    info_i = json.load(read_file)

sessionStorage = {}

HI = 'Привет начинающий программист. Этот навык даст тебе приблизительное представление о замечательном языке программирования - Python'


def text(num):  # берём текст и смотрим чтобы всё было нормально
    print(info_i)
    if num >= 0 and num <= 9:
        return info_i['lessons'][str(num)]
    else:
        if num < 0:
            return info_i['lessons']['0']
        else:
            return info_i['lessons']['9']


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


def handle_dialog(req, res):
    user_id = req['session']['user_id']
    res['response']['buttons'] = []
    if req['session']['new']:
        sessionStorage[user_id] = {
            'number': -1,
            'start': False}
        res['response']['text'] = HI
        res['response']['buttons'] = buttons('start')
        return
    if not sessionStorage[user_id]['start'] and req['request']['original_utterance'].lower() in ['да']:  # команда для старта
        res['response']['text'] = 'Скажите: начать обучение'
        res['response']['buttons'] = buttons('first')
        sessionStorage[user_id]['start'] = True

    elif not sessionStorage[user_id]['start'] and req['request']['original_utterance'].lower() in ['нет']:  # на случай отказа юзверя
        res['response']['text'] = 'оставайся в неведение'
        res['response']['end_session'] = False
        return

    elif 'начать обучение' in req['request']['original_utterance'].lower() and sessionStorage[user_id]['start']:  # происходит сразу после команды начинания
        res['response']['text'] = text(sessionStorage[user_id]['number'])
        sessionStorage[user_id]['number'] += 1
        res['response']['buttons'] = buttons()
        print(res['response']['text'])

    elif req['request']['original_utterance'].lower() == 'СЛЕДУЮЩИЙ!' and sessionStorage[user_id]['number'] >= 0:  # перелистывание
        res['response']['text'] = text(sessionStorage[user_id]['number'])
        sessionStorage[user_id]['number'] += 1
        res['response']['buttons'] = buttons()
        print(res['response']['text'])


def buttons(key='standart'):
    if key == 'standart':
        but = {'title': 'СЛЕДУЮЩИЙ!', 'hide': False}
    elif key == 'start':
        but = [{'title': 'Да', 'hide': True},
               {'title': 'Нет', 'hide': True}]
    elif key == 'first':
        but = {'title': 'начать обучение', 'hide': True}

    return but


if __name__ == '__main__':
    app.run()

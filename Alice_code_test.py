from flask import Flask, request
import logging
import json

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, filename='/home/margis902/mysite/app.log', #записываю логи
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')

with open("/home/margis902/mysite/lessons.json", "r", ) as read_file:
    info_i = json.load(read_file)


sessionStorage = {}


HI = 'Привет начинающий программист. Этот тест проверит твоё умение читать простейший код. Если хочешь узнать ещё, ты только спроси'


def get_text(num):
    print(info_i)
    if num >= 0 and num <= 8:
        return info_i['lessons'][str(num)]
    else:
        if num < 0:
            return info_i['lessons']['0']
        else:
            return info_i['lessons']['8']



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







def buttons(key = 'standart'):
    if key == 'standart':
        but = {'title': 'СЛЕДУЮЩИЙ!', 'hide': False}
    elif key == 'start':
        but = [{'title': 'Да', 'hide': True},
                {'title': 'Нет', 'hide': True}]
    elif key == 'first':
        but = {'title': 'начать тестирование', 'hide': True}


    return but
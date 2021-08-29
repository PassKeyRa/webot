from app import app
from app import mongo
from flask import render_template
import json, random, string


def get_mes():
    return '{}'


def send_mes(mes):
    pass


def id_generator(size=32, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def queue_handler():
    while True:
        try:
            queue_request = get_mes()
            request = json.loads(queue_request)
            if request['type'] == 'new_chat':
                new_token = id_generator()
                mongo.db.chats.insert_one({'chat_name': request['chat_name'],
                                           'chat_token': new_token,
                                           'activated': True,
                                           'messages': []})
                send_mes(json.dumps({'Status': 'OK',
                                     'url': f'/show_chat/{new_token}',
                                     'token': new_token}))

            elif request['type'] == 'add_message':
                mongo.db.chats.update_one({'chat_token': request['token']},
                                          {'$push': {'messages': request['message']}})

            elif request['type'] == 'deactivate_chat':
                mongo.db.chats.update_one({'chat_token': request['token']},
                                          {'activated': False})

        except Exception as e:
            print(f'[!] Some error: {e}')
            continue


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/show_chat/<token>')
def show_chat(token):
    chat = mongo.db.chats.find_one_or_404({"token": token})
    return render_template("show_chat.html", chat=chat)

from app import app
from app import mongo
from flask import render_template
from flask.views import View
import json, random, string
test = 1


class QueueHandler:
    @staticmethod
    def get_mes():
        global test
        if test == 0:
            return '{}'
        else:
            test -= 1
            # return json.dumps({'type': 'new_chat', 'chat_name': 'test_test'})
            return json.dumps({'type': 'add_messages', 'chat_token': '036wutcvu1hsn38jqzc8x4s327yec6pi', 'messages': [{'text': 'asdasdasd asdas asd', 'timestamp': '3232131321', 'sender_name': 'Test Testovich'}, {'text': 'dsopqw[e opqwoepoc oopeowefpm', 'timestamp': '23135438','sender_name': 'ASd Asdovich'}]})
            # return json.dumps({'type': 'delete_chat', 'chat_token': '8d18xinsr5r48diw9ms6f652htb9c9ef'})

    @staticmethod
    def send_mes(mes):
        pass

    @staticmethod
    def token_generator(size=32, chars=string.ascii_lowercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    @staticmethod
    def queue_handler():
        while True:
            try:
                queue_request = QueueHandler.get_mes()
                request = json.loads(queue_request)
                if request['type'] == 'new_chat':
                    new_token = QueueHandler.token_generator()
                    mongo.db.chats.insert_one({'chat_name': request['chat_name'],
                                               'chat_token': new_token,
                                               'messages': []})
                    QueueHandler.send_mes(json.dumps({'Status': 'OK',
                                         'url': f'/show_chat/{new_token}',
                                         'token': new_token}))

                elif request['type'] == 'add_messages':
                    for mes in request['messages']:
                        mongo.db.chats.update_one({'chat_token': request['chat_token']},
                                                  {'$push': {'messages': mes}})

                elif request['type'] == 'delete_chat':
                    mongo.db.chats.delete_one({'chat_token': request['chat_token']})

            except Exception as e:
                # print(f'[!] Some error: {e}')
                continue


class ShowChat(View):
    def dispatch_request(self, token):
        chat = mongo.db.chats.find_one_or_404({"chat_token": token})
        return render_template("show_chat.html", chat=chat)


app.add_url_rule('/show_chat/<token>', view_func=ShowChat.as_view('show_chat'))

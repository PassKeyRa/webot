from app import app
from app import mongo
from flask import render_template
from flask.views import View
import json, random, string
from app.aws_sqs_adapter import AwsSqsAdapter
from app.utils import *


class QueueHandler:
    @staticmethod
    def get_mes(sqs):
        while True:
            msg = sqs.receiveMessages()
            if msg is None:
                continue
            return msg

    @staticmethod
    def send_mes(mes, sqs, ):
        sqs.sendMessage(mes)

    @staticmethod
    def delete_queues():
        aws_access_key_id, aws_secret_access_key, region_name, _, _ = loadEnv()
        sqs_in = AwsSqsAdapter(aws_access_key_id, aws_secret_access_key, region_name)
        sqs_out = AwsSqsAdapter(aws_access_key_id, aws_secret_access_key, region_name)
        sqs_in.queueConnect('get_messages')
        sqs_out.queueConnect('send_link')
        sqs_in.queueDelete()
        sqs_out.queueDelete()

    @staticmethod
    def token_generator(size=32, chars=string.ascii_lowercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    @staticmethod
    def queue_handler():
        aws_access_key_id, aws_secret_access_key, region_name, _, _ = loadEnv()
        sqs_in = AwsSqsAdapter(aws_access_key_id, aws_secret_access_key, region_name)
        sqs_out = AwsSqsAdapter(aws_access_key_id, aws_secret_access_key, region_name)
        sqs_in.queueCreate('get_messages')
        sqs_out.queueCreate('send_link')
        sqs_in.queueConnect('get_messages')
        sqs_out.queueConnect('send_link')
        while True:
            try:
                queue_request = QueueHandler.get_mes(sqs_in)
                request = json.loads(queue_request)
                if request['type'] == 'new_chat':
                    new_token = QueueHandler.token_generator()
                    mongo.db.chats.insert_one({'chat_name': request['chat_name'],
                                               'chat_token': new_token,
                                               'messages': []})
                    QueueHandler.send_mes(json.dumps({'Status': 'OK',
                                         'url': f'/show_chat/{new_token}',
                                         'token': new_token}), sqs_out)

                elif request['type'] == 'add_messages':
                    for mes in request['messages']:
                        mongo.db.chats.update_one({'chat_token': request['chat_token']},
                                                  {'$push': {'messages': mes}})

                elif request['type'] == 'delete_chat':
                    mongo.db.chats.delete_one({'chat_token': request['chat_token']})

            except Exception as e:
                print(f'[!] Some error: {e}')
                continue


class ShowChat(View):
    def dispatch_request(self, token):
        chat = mongo.db.chats.find_one_or_404({"chat_token": token})
        return render_template("show_chat.html", chat=chat)


app.add_url_rule('/show_chat/<token>', view_func=ShowChat.as_view('show_chat'))

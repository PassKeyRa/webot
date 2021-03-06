import json
import random
import string
import time
from app.aws_sqs_adapter import AwsSqsAdapter
from app.utils import *
from app import mongo


class QueueHandler:
    @staticmethod
    def get_mes(sqs):
        while True:
            time.sleep(10)
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
                                                      'url': f'http://w3b0t.tk/show_chat/{new_token}',
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

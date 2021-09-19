from .aws_sqs.aws_sqs_adapter import AwsSqsAdapter
from .aws_sqs.utils import *


class QueueHandler:
    def __init__(self):
        self.aws_access_key_id, self.aws_secret_access_key, self.region_name, _, _ = loadEnv()
        self.sqs_in = AwsSqsAdapter(self.aws_access_key_id, self.aws_secret_access_key, self.region_name)
        self.sqs_out = AwsSqsAdapter(self.aws_access_key_id, self.aws_secret_access_key, self.region_name)
        self.sqs_out.queueConnect('get_messages')
        self.sqs_in.queueConnect('send_link')

    def send(self, data):
        self.sqs_out.sendMessage(data)

    def send_and_receive(self, data):
        self.sqs_out.sendMessage(data)
        answer = ''
        while True:
            try:
                answer = next(self.sqs_in.receiveMessages())
            except Exception:
                continue
            break
        return answer

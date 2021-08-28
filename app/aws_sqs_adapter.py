from json import loads
from os import getenv
from boto3.session import Session
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

def loadEnv():
    load_dotenv()
    aws_access_key_id = getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = getenv('AWS_SECRET_ACCESS_KEY')
    region_name = getenv('REGION_NAME')
    queue_name_in = getenv('QUEUE_NAME_IN')
    queue_name_out = getenv('QUEUE_NAME_OUT')
    return aws_access_key_id, aws_secret_access_key, region_name, queue_name_in, queue_name_out

class AwsSqsAdapter:

    def __init__(self, aws_access_key_id, aws_secret_access_key, region_name):
        try:
            self.session = Session(aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)
            self.sqs = self.session.resource('sqs')
        except Exception as e:
            logger.exception("Some error occured: {}".format(e))


    def QueueCreate(self, queue_name):
        try:
            self.queue = self.sqs.create_queue(QueueName=queue_name)
        except Exception as e:
            logger.exception("Some error occured: {}".format(e))

    def QueueConnect(self, queue_name):
        try:
            self.queue = self.sqs.get_queue_by_name(QueueName=queue_name)
        except Exception as e:
            logger.exception("Some error occured: {}".format(e))

    def SendMessage(self, message):
        try:
            self.queue.send_message(MessageBody=message)
        except Exception as e:
            logger.exception("Some error occured: {}".format(e))

    def ReceiveMessages(self):
        temp_queue = self.queue.receive_messages()
        try:
            for message in range(len(temp_queue)):
                yield loads(temp_queue[message].body)
        except Exception as e:
            logger.exception("Some error occured: {}".format(e))

    def QueueDelete(self):
        try:
            self.queue.delete()
        except Exception as e:
            logger.exception("Some error occured: {}".format(e))
            
if __name__ == "__main__":
    aws_access_key_id, aws_secret_access_key, region_name, queue_name_in, queue_name_out = loadEnv()
    incoming_sqs = AwsSqsAdapter(aws_access_key_id, aws_secret_access_key, region_name)
    incoming_sqs.QueueCreate(queue_name_in)
    incoming_sqs.QueueConnect(queue_name_in)
    incoming_sqs.SendMessage('{"test":"1234"}')
    for i in incoming_sqs.ReceiveMessages():
        print(i)
    incoming_sqs.QueueDelete()
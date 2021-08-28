from json import loads
from os import getenv
from boto3.session import Session
from dotenv import load_dotenv
from secrets import token_hex
import logging

logger = logging.getLogger(__name__)

def loadEnv():
    try:
        load_dotenv()
        aws_access_key_id = getenv('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = getenv('AWS_SECRET_ACCESS_KEY')
        region_name = getenv('REGION_NAME')
        queue_name_in = getenv('QUEUE_NAME_IN')
        queue_name_out = getenv('QUEUE_NAME_OUT')
        return aws_access_key_id, aws_secret_access_key, region_name, queue_name_in, queue_name_out
    except Exception as e:
        logger.exception("Some error occured: {}".format(e))

def testAwsSqsAdapter():
    aws_access_key_id, aws_secret_access_key, region_name, _, _ = loadEnv()
    incoming_sqs = AwsSqsAdapter(aws_access_key_id, aws_secret_access_key, region_name)
    queue_name = token_hex(8)
    incoming_sqs.QueueCreate(queue_name)
    incoming_sqs.QueueConnect(queue_name)
    incoming_sqs.SendMessage('{"val":"1337"}')
    assert int(next(incoming_sqs.ReceiveMessages())['val']) == 1337
    incoming_sqs.QueueDelete()
 

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
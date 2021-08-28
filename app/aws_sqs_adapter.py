from json import loads
from os import getenv
from boto3.session import Session
from dotenv import load_dotenv

def loadEnv():
    load_dotenv()
    aws_access_key_id = getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = getenv('AWS_SECRET_ACCESS_KEY')
    region_name = getenv('REGION_NAME')
    queue_name = getenv('QUEUE_NAME')
    return aws_access_key_id, aws_secret_access_key, region_name, queue_name

class AwsSqsAdapter:

    def __init__(self, aws_access_key_id, aws_secret_access_key, region_name):
        self.session = Session(aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)
        self.sqs = self.session.resource('sqs')

    def QueueConnect(self, queue_name):
        self.queue = self.sqs.get_queue_by_name(QueueName=queue_name)

    def SendMessage(self, message):
        self.queue.send_message(MessageBody=message)


    def ReceiveMessages(self):
        temp = self.queue.receive_messages()
        for message in range(len(temp)):
            print(loads(temp[message].body)['test'])

if __name__ == "__main__":
    aws_access_key_id, aws_secret_access_key, region_name, queue_name = loadEnv()
    test_sqs = AwsSqsAdapter(aws_access_key_id, aws_secret_access_key, region_name)
    test_sqs.QueueConnect(queue_name)
    test_sqs.SendMessage('{"test":"1234"}')
    test_sqs.ReceiveMessages()
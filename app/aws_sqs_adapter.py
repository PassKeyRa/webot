from utils import *

def testAwsSqsAdapter():
    number_of_msg = 20
    aws_access_key_id, aws_secret_access_key, region_name, _, _ = loadEnv()
    test_sqs = AwsSqsAdapter(aws_access_key_id, aws_secret_access_key, region_name)
    queue_name = token_hex(8)
    test_sqs.QueueCreate(queue_name)
    test_sqs.QueueConnect(queue_name)
    for i in range(number_of_msg):
        test_sqs.SendMessage('{"'+str(i)+'":"'+str(i)+'"}')
    msg = {}
    while len(msg) != number_of_msg:
        for x in test_sqs.ReceiveMessages():
            msg.update(loads(x))
    test_sqs.QueueDelete()
    for x in msg.keys():
        assert msg[x] == x
    assert len(msg) == number_of_msg

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
        temp_queue = self.queue.receive_messages(MaxNumberOfMessages=10)
        try:
            for message in range(len(temp_queue)):
                yield temp_queue[message].body
        except Exception as e:
            logger.exception("Some error occured: {}".format(e))

    def QueueDelete(self):
        try:
            self.queue.delete()
        except Exception as e:
            logger.exception("Some error occured: {}".format(e))
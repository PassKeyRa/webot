from .utils import *


def testAwsSqsAdapter():
    number_of_msg = 20
    aws_access_key_id, aws_secret_access_key, region_name, _, _ = loadEnv()
    test_sqs = AwsSqsAdapter(aws_access_key_id, aws_secret_access_key, region_name)
    queue_name = token_hex(8)
    test_sqs.queueCreate(queue_name)
    test_sqs.queueConnect(queue_name)
    for i in range(number_of_msg):
        test_sqs.sendMessage('{"' + str(i) + '":"' + str(i) + '"}')
    msg = {}
    while len(msg) != number_of_msg:
        msg.update(loads(test_sqs.receiveMessages()))
    test_sqs.queueDelete()
    for x in msg.keys():
        assert msg[x] == x
    assert len(msg) == number_of_msg


class AwsSqsAdapter:
    def __init__(self, aws_access_key_id, aws_secret_access_key, region_name):
        try:
            self.session = Session(aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key,
                                   region_name=region_name)
            self.sqs = self.session.resource('sqs')
        except Exception as e:
            logger.exception("Error occured when creating AWS queue object: {}".format(e))

    def queueCreate(self, queue_name):
        try:
            self.queue = self.sqs.create_queue(QueueName=queue_name)
        except Exception as e:
            logger.exception("Error occured when creating AWS queue: {}".format(e))

    def queueConnect(self, queue_name):
        try:
            self.queue = self.sqs.get_queue_by_name(QueueName=queue_name)
        except Exception as e:
            logger.exception("Error occured when connecting to AWS queue: {}".format(e))

    def sendMessage(self, message):
        try:
            self.queue.send_message(MessageBody=message)
        except Exception as e:
            logger.exception("Error occured when sending message in the AWS queue: {}".format(e))

    def receiveMessages(self):
        try:
            message_list = self.queue.receive_messages(MaxNumberOfMessages=1)
            if len(message_list) == 0:
                return None
            message_body = message_list[0].body
            # self.queue.delete_message(message_list[0])
            # self.sqs.delete_message(QueueUrl=self.queue)
            message_list[0].delete()
            return message_body
        except Exception as e:
            logger.exception("Error occured when receiving message from the AWS queue: {}".format(e))

    def queueDelete(self):
        try:
            self.queue.delete()
        except Exception as e:
            logger.exception("Error occured when deleting AWS queue: {}".format(e))

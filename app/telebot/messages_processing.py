import json


class MessagesProcessing:
    def __init__(self, token):
        self.token = token

    async def send_messages(self, client, chat, buffer_size):
        messages = []
        async for message in client.iter_messages(chat):
            messages.append({'message_id': message.id, 'message_sender': message.from_id, 'message_text': message.message})
            if len(messages) == buffer_size:
                data = json.dumps({'type': 'add_messages', 'token': self.token, 'messages': messages})
                # send data
                messages = []

    async def send_message(self, message_text, message_sender, message_id):
        message = {'message_id': message_id, 'message_sender': message_sender, 'message_text': message_text}
        data = json.dumps({'type': 'add_messages', 'token': self.token, 'messages': [message]})
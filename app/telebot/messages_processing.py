import json


class ChatMessagesProcessing:
    def __init__(self, token):
        self.token = token

    async def send_all_chat_messages(self, client, chat, buffer_size):
        messages = []
        async for message in client.iter_messages(chat):
            sender = await message.get_sender()
            sender_name = ' '.join([i for i in [sender.first_name, sender.last_name] if i])
            messages.append({'message_id': message.id, 'message_sender': sender_name, 'message_text': message.message})
            if len(messages) == buffer_size:
                data = json.dumps({'type': 'add_messages', 'token': self.token, 'messages': messages})
                print('Send messages', data)
                messages = []

    async def send_message(self, m):
        sender = await m.get_sender()
        message_id = m.id
        sender_name = ' '.join([i for i in [sender.first_name, sender.last_name] if i])
        message_text = m.text
        message = {'message_id': message_id, 'message_sender': sender_name, 'message_text': message_text}
        data = json.dumps({'type': 'add_messages', 'token': self.token, 'messages': [message]})
        print('Send messages', data)

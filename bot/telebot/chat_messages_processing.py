import json


class ChatMessagesProcessing:
    def __init__(self, queue, token=None):
        self.token = token
        self.queue = queue

    async def send_all_chat_messages(self, client, chat, buffer_size):
        if not self.token:
            return False
        messages = []
        counter = 0
        async for message in client.iter_messages(chat, reverse=True):
            if counter >= 20000:
                break # max number of messages
            sender = await message.get_sender()
            if not sender:
                continue
            sender_name = ' '.join([i for i in [sender.first_name, sender.last_name] if i])
            messages.append({'message_id': message.id, 'message_sender': sender_name, 'message_text': message.message})
            if len(messages) == buffer_size:
                data = json.dumps({'type': 'add_messages', 'chat_token': self.token, 'messages': messages})

                # temporary
                print('Send messages', data)
                self.queue.send(data)

                messages = []

            counter += 1

        if messages:
            data = json.dumps({'type': 'add_messages', 'chat_token': self.token, 'messages': messages})
            print('Send messages', data)
            self.queue.send(data)
        return True

    async def send_message(self, m):
        if not self.token:
            return False
        sender = await m.get_sender()
        message_id = m.id
        sender_name = ' '.join([i for i in [sender.first_name, sender.last_name] if i])
        message_text = m.text
        message = {'message_id': message_id, 'message_sender': sender_name, 'message_text': message_text}
        data = json.dumps({'type': 'add_messages', 'chat_token': self.token, 'messages': [message]})

        # temporary
        print('Send messages', data)
        self.queue.send(data)

        return True

    def send_new_chat(self, chat):
        data = json.dumps({'type': 'new_chat', 'chat_name': chat.title})

        # temporary
        print('Send new_chat', data)
        answer = json.loads(self.queue.send_and_receive(data))
        print(answer)
        return answer['url'], answer['token']

    def set_token(self, token):
        self.token = token

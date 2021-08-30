from telethon.sync import TelegramClient
from config import *


class MessageDumper:
    def __init__(self):
        self.bot_id = api_id
        self.bot_hash = api_hash
        self.bot_token = bot_token
        self.bot = TelegramClient('bot', self.bot_id, self.bot_hash).start(bot_token=bot_token)

    def dump_message_by_id(self, message_id):
        pass

    def dump_messages_until_id(self, message_id):
        pass

    def dump_all(self):
        pass

from telethon import TelegramClient, events
from telethon.tl.types import User, Chat, Channel, ChannelParticipantsAdmins, ChatParticipantAdmin, ChatParticipantCreator
from telethon.tl.custom.participantpermissions import ParticipantPermissions
from telethon.tl.functions.channels import GetParticipantsRequest

import os

import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

api_id = os.environ.get('API_ID')
api_hash = os.environ.get('API_HASH')
bot_name = os.environ.get('BOT_NAME', default='WeBot')

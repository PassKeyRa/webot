from telegram import Chat, Update, ChatMember, ChatMemberUpdated
from telegram.ext import Updater, CommandHandler, CallbackContext, ChatMemberHandler, MessageHandler, Filters

import os

import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

api_id = os.environ.get('API_ID',  default=None)
api_hash = os.environ.get('API_HASH',  default=None)
bot_token = os.environ.get('BOT_TOKEN')
bot_name = os.environ.get('BOT_NAME', default='WeBot')
admin_password = os.environ.get('ADMIN_PASSWORD')

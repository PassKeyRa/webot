from telegram import Chat, Update, ChatMember, ChatMemberUpdated
from telegram.ext import Updater, CommandHandler, CallbackContext, ChatMemberHandler

import os

import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

api_id = os.environ['API_ID']
api_hash = os.environ['API_HASH']
bot_token = os.environ['BOT_TOKEN']
bot_name = os.environ['BOT_NAME'] or 'WeBot'
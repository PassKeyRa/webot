import random
import string

from .chat_messages_processing import ChatMessagesProcessing
from .config import *
from .db import *
from .queue import QueueHandler


queue = QueueHandler()


async def is_group_admin(client, chat, user_id):
    async for user in client.iter_participants(chat, filter=ChannelParticipantsAdmins):
        if type(user.participant) in [ChatParticipantAdmin, ChatParticipantCreator, ChannelParticipantCreator, ChannelParticipantAdmin] and user.id == user_id:
            return True
    return False


async def chat_activate(client, chat, user_id):
    if not is_group(chat):
        await not_a_group(client, chat)
        return
    if await is_group_admin(client, chat, user_id):
        with DB() as db:
            status = db.activate_chat(chat.id, user_id)
            if status == DB_SUCCESS:
                await client.send_message(chat, "Start chat updates listening and publishing")

                url = db.get_chat_url(chat.id)
                await client.send_message(chat, "Here you can find your chat: " + url)

            elif status == DB_NEW_CHAT:

                # Here should be token getting
                # token = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(32))  # temporary
                mep = ChatMessagesProcessing(queue)
                url, token = mep.send_new_chat(chat)

                db.set_chat_token(chat.id, token)
                db.set_chat_url(chat.id, url)

                await client.send_message(chat, "Fetching previous messages")
                mep.set_token(token)
                await mep.send_all_chat_messages(client, chat, 20)
                await client.send_message(chat, "Start chat updates listening and publishing")
                await client.send_message(chat, "Here you can find your chat: " + url)

            elif status == DB_ERROR:
                await client.send_message(chat, "Server error")


async def chat_deactivate(client, chat, user_id):
    if not is_group(chat):
        await not_a_group(client, chat)
        return
    if await is_group_admin(client, chat, user_id):
        with DB() as db:
            status = db.deactivate_chat(chat.id, user_id)
            if status == DB_SUCCESS:
                await client.send_message(chat, "Stop chat updates listening and publishing")
            elif status == DB_CHAT_DOESNT_EXIST:
                await client.send_message(chat, "Chat has not ever been activated")
            elif status == DB_ERROR:
                await client.send_message(chat, "Server error")
            elif status == DB_CHAT_DEACTIVATED:
                await client.send_message(chat, "Chat has already been deactivated")


async def process_message(client, chat, message):
    if not is_group(chat):
        await not_a_group(client, chat)
        return
    with DB() as db:
        status = db.chat_activation_status(chat.id)
        if status == DB_CHAT_ACTIVATED:
            token = db.get_chat_token(chat.id)
            mep = ChatMessagesProcessing(queue, token=token)
            await mep.send_message(message)


async def start(client, chat, user_id) -> None:
    """Send a message when the command /start is issued."""
    if not is_group(chat):
        await not_a_group(client, chat)
        return
    if await is_group_admin(client, chat, user_id):
        await client.send_message(chat, "Type /help to see available commands")


def stop(chat) -> None:
    """Stop the app when the command /stop is issued."""
    pass


def is_group(chat):
    if type(chat) != Chat and type(chat) != Channel:
        return False
    return True


async def not_a_group(client, chat):
    await client.send_message(chat, "This bot can be used in groups only. Add it to a group and type /help "
                                    "(all interactions with the bot can be done by group admins)")

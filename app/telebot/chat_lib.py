from .config import *
from .db import *
from .messages_processing import MessagesProcessing


async def is_group_admin(client, chat, user_id):
    async for user in client.iter_participants(chat, filter=ChannelParticipantsAdmins):
        if type(user.participant) in [ChatParticipantAdmin, ChatParticipantCreator] and user.id == user_id:
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
                token = db.get_chat_token(chat.id)
                await client.send_message(chat, "Start chat updates listening and publishing")
                # send the link to the chat
            elif status == DB_NEW_CHAT:
                # get token
                await client.send_message(chat, "Fetching previous messages")
                mep = MessagesProcessing(db.get_chat_token(chat.id))
                await mep.send_messages(client, chat, 100)
                await client.send_message(chat, "Start chat updates listening and publishing")
                # send the link to the chat
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
            elif status == DB_NEW_CHAT:
                await client.send_message(chat, "Chat isn't activated")
            elif status == DB_ERROR:
                await client.send_message(chat, "Server error")


async def process_message(client, chat, message_text, message_sender, message_id):
    if not is_group(chat):
        await not_a_group(client, chat)
        return
    with DB() as db:
        status = db.chat_activation_status(chat.id)
        if status == DB_CHAT_ACTIVATED:
            token = db.get_chat_token(chat.id)
            if token not in [DB_CHAT_DOESNT_EXIST, DB_CHAT_DEACTIVATED, DB_ERROR]:
                # send the message using the token
                mep = MessagesProcessing(db.get_chat_token(chat.id))
                await mep.send_message(message_text, message_sender, message_id)


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
    if type(chat) != Chat:
        return False
    return True


async def not_a_group(client, chat):
    await client.send_message(chat, "This bot can be used in groups only. Add it to a group and type /help "
                                    "(all interactions with the bot can be done by group admins)")

from .config import *
from .db import *


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
        await client.send_message(chat, "Start chat updates listening and publishing")
        pass


async def chat_deactivate(client, chat, user_id):
    if not is_group(chat):
        await not_a_group(client, chat)
        return
    if await is_group_admin(client, chat, user_id):
        await client.send_message(chat, "Stop chat updates listening and publishing")


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

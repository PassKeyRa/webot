#!/usr/bin/env python3
from telebot.config import *
from telebot.chat_lib import *
from telebot.db import DB

import re

client = TelegramClient('webot', api_id, api_hash)
with DB() as db:
    db.create_chats_table()


@client.on(events.NewMessage)
async def handle_messages(event):
    logger.info("[MESSAGE] chat_id=%s message_id=%s text=%s", event.chat_id, event.id, event.raw_text)
    text = event.raw_text
    chat = await event.get_chat()
    sender = await event.get_sender()
    if re.fullmatch('/start', text):
        await start(client, chat, event.sender_id)
    elif re.fullmatch('/stop', text):
        stop(chat)
    elif re.fullmatch('/help', text):
        await client.send_message(chat, "Will be soon")
    elif re.fullmatch('/activate', text):
        await chat_activate(client, chat, event.sender_id)
    elif re.fullmatch('/deactivate', text):
        await chat_deactivate(client, chat, event.sender_id)
    else:
        await process_message(client, chat, event.message)


@client.on(events.ChatAction)
async def handler(event):
    if event.user_added:
        me = await client.get_me()
        if me.id == event.user_id:
            chat = await event.get_chat()
            logger.info("Added to the chat %s", chat.id)
    elif event.user_kicked:
        me = await client.get_me()
        if me.id == event.user_id:
            chat = await event.get_chat()
            logger.info("Removed from the chat %s", chat.id)


client.start()
client.run_until_disconnected()

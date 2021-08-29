#!/usr/bin/env python3
from telebot.config import *
from telebot.chat_lib import *


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    chat = update.effective_chat
    if chat.type == Chat.PRIVATE:
        chat.send_message("This bot can be used in groups only. Add it to a group and type /help (all interactions "
                          "with the bot can be done by group admins)")


def stop(update: Update, context: CallbackContext) -> None:
    """Stop the app when the command /stop is issued."""
    pass


def main() -> None:
    updater = Updater(bot_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    # dispatcher.add_handler(CommandHandler("stop", stop))
    dispatcher.add_handler(CommandHandler("activate", chat_activate))
    dispatcher.add_handler(CommandHandler("deactivate", chat_deactivate))
    dispatcher.add_handler(ChatMemberHandler(track_chats, ChatMemberHandler.MY_CHAT_MEMBER))

    updater.start_polling(allowed_updates=Update.ALL_TYPES)
    updater.idle()


if __name__ == "__main__":
    main()

from .config import *


def is_group_admin(update: Update):
    chat = update.effective_chat
    if chat.type == Chat.GROUP:
        if update.effective_user in [i.user for i in chat.get_administrators()]:
            return True
    return False


def chat_activate(update: Update, context: CallbackContext):
    if is_group_admin(update):
        chat = update.effective_chat
        chat.send_message("Start chat updates listening and publishing")
        # start chat updates listening and publishing
        pass


def chat_deactivate(update: Update, context: CallbackContext):
    if is_group_admin(update):
        chat = update.effective_chat
        chat.send_message("Stop chat updates listening and publishing")
        # stop chat updates listening and publishing
        pass


def status_change(chat_member: ChatMemberUpdated):
    """
    Get chat member updates. Returns a tuple with two booleans -
    if it was a chat member and if it is a chat member
    """
    status = chat_member.difference().get('status')
    if not status:
        return None

    old_is_member, new_is_member = chat_member.difference().get("is_member", (None, None))
    old_status, new_status = status
    is_member, was_member = False, False

    if old_status == ChatMember.RESTRICTED and old_is_member is True:
        was_member = True
    elif old_status in [ChatMember.MEMBER, ChatMember.CREATOR, ChatMember.ADMINISTRATOR]:
        was_member = True

    if new_status == ChatMember.RESTRICTED and new_status is True:
        is_member = True
    elif new_status in [ChatMember.MEMBER, ChatMember.CREATOR, ChatMember.ADMINISTRATOR]:
        is_member = True

    return was_member, is_member


def track_chats(update: Update, context: CallbackContext):
    """Tracks and logs the chats the bot is in"""
    changed = status_change(update.my_chat_member)
    if not changed:
        return
    was_mem, is_mem = changed

    chat = update.effective_chat
    if chat.type == Chat.PRIVATE:
        if not was_mem and is_mem:
            logger.info("Started in private chat %s", chat.id)
        else:
            logger.info("Blocked in private chat %s", chat.id)
    elif chat.type == Chat.GROUP or chat.type == Chat.SUPERGROUP:
        if not was_mem and is_mem:
            logger.info("Added to group %s", chat.id)
        else:
            logger.info("Removed from group %s", chat.id)
    if chat.type == Chat.CHANNEL:
        if not was_mem and is_mem:
            logger.info("Added to channel %s", chat.id)
        else:
            logger.info("Removed from channel %s", chat.id)


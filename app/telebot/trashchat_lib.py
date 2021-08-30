from .config import *
from .chat_lib import is_group_admin
from .db import DB


class TrashChat:
    def __init__(self):
        pass

    @staticmethod
    def admin_handler(update: Update, context: CallbackContext):
        logger.info('Trash chat manipulation, user %s %s', update.effective_user.username, update.effective_user.id)
        if is_group_admin(update) and 'admin_' + admin_password in update.message.text:
            try:
                cmd = update.message.text.strip().split(' ')[1]
                # admin command list
                if cmd == 'activate':
                    logger.info('New trash chat activated')
                    # Activate trash chat

                    with DB() as db:
                        db.activate_chat(update.effective_chat.id, update.effective_user.id)

                    update.effective_chat.send_message('Activate: success')
                elif cmd == 'deactivate':
                    logger.info('Trash chat deactivated')
                    # Deactivate trash chat

                    with DB() as db:
                        db.deactivate_chat(update.effective_chat.id, update.effective_user.id)

                    update.effective_chat.send_message('Deactivate: success')
            except IndexError as e:
                logger.error('Command is not passed')
                update.effective_chat.send_message('Pass a command as an argument')
            #except Exception as e:
            #    logger.error('Some exception occurred: ' + str(e))
            #    update.effective_chat.send_message('Error')

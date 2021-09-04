import sqlite3

# status constants
DB_NEW_CHAT = 0
DB_SUCCESS = 1
DB_ERROR = 2
DB_CHAT_ACTIVATED = 3
DB_CHAT_DEACTIVATED = 4
DB_CHAT_DOESNT_EXIST = 5


class DB:
    def __init__(self):
        self.con = sqlite3.connect('sqlite.db')
        self.cur = self.con.cursor()

    def close(self):
        self.cur.close()

    def create_chats_table(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS chats ("
                         "chat_id INTEGER PRIMARY KEY NOT NULL,"
                         "activated INTEGER,"
                         "changed_by INTEGER,"
                         "token TEXT)")

    def activate_chat(self, chat_id, changed_by):
        """
        :param chat_id: id of the chat
        :param changed_by: id of the user that changed the state
        :return: DB_NEW_CHAT if chat doesn't exist, DB_SUCCESS if exists, DB_ERROR if error
        """
        try:
            chat = list(self.cur.execute("SELECT * FROM chats WHERE chat_id=?", [chat_id]).fetchall()[0])
            self.cur.execute("UPDATE chats SET activated=1, changed_by=? WHERE chat_id=?", [changed_by, chat_id])
            return DB_SUCCESS
        except IndexError:
            self.cur.execute("INSERT INTO chats VALUES (?, ?, ?, ?)", [chat_id, 1, changed_by, '-'])
            return DB_NEW_CHAT
        except Exception as e:
            print('[activate_chat] Database processing error')
            return DB_ERROR

    def deactivate_chat(self, chat_id, changed_by):
        """
        :param chat_id: id of the chat
        :param changed_by: id of the user that changed the state
        :return: DB_NEW_CHAT if chat doesn't exist, DB_SUCCESS if exists, DB_ERROR if error
        """
        try:
            chat = list(self.cur.execute("SELECT * FROM chats WHERE chat_id=?", [chat_id]).fetchall()[0])
            self.cur.execute("UPDATE chats SET activated=0, changed_by=? WHERE chat_id=?", [changed_by, chat_id])
            return DB_SUCCESS
        except IndexError:
            self.cur.execute("INSERT INTO chats VALUES (?, ?, ?, ?)", [chat_id, 0, changed_by, '-'])
            return DB_NEW_CHAT
        except Exception as e:
            print('[deactivate_chat] Database processing error')
            return DB_ERROR

    def chat_activation_status(self, chat_id):
        try:
            activated = list(self.cur.execute("SELECT activated FROM chats WHERE chat_id=?", [chat_id]).fetchall()[0])[0]
            if activated:
                return DB_CHAT_ACTIVATED
            return DB_CHAT_DEACTIVATED
        except IndexError:
            return DB_CHAT_DOESNT_EXIST
        except Exception:
            return DB_ERROR

    def get_chat_token(self, chat_id):
        """
        :param chat_id: id of the chat
        :return: token/DB_NEW_CHAT if chat doesn't exist or token == '-'/DB_ERROR if error
        """
        try:
            token = list(self.cur.execute("SELECT token FROM chats WHERE chat_id=?", [chat_id]).fetchall()[0])[0]
            if token == '-':
                return DB_NEW_CHAT
            return token
        except IndexError:
            return DB_CHAT_DOESNT_EXIST
        except Exception as e:
            print('[get_chat_token] Database processing error')
            return DB_ERROR

    def __enter__(self):
        return self

    def __exit__(self, ext_type, exc_value, traceback):
        self.cur.close()
        if isinstance(exc_value, Exception):
            self.con.rollback()
        else:
            self.con.commit()
        self.con.close()

import sqlite3


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
                         "last_message_processed INTEGER)")

    def activate_chat(self, chat_id, changed_by):
        try:
            chat = list(self.cur.execute("SELECT * FROM chats WHERE chat_id=?", chat_id).fetchall()[0])
            if chat:
                self.cur.execute("UPDATE chats SET activated=1, changed_by=? WHERE chat_id=?", [changed_by, chat_id])
            else:
                self.cur.execute("INSERT INTO trash_chat VALUES (?, ?, ?, ?)", [chat_id, 1, changed_by, 0])
            return True
        except Exception as e:
            print('Database processing error')
            return False

    def deactivate_chat(self, chat_id, changed_by):
        try:
            chat = list(self.cur.execute("SELECT * FROM chats WHERE chat_id=?", chat_id).fetchall()[0])
            if chat:
                self.cur.execute("UPDATE chats SET activated=0, changed_by=? WHERE chat_id=?", [changed_by, chat_id])
            else:
                self.cur.execute("INSERT INTO trash_chat VALUES (?, ?, ?, ?)", [chat_id, 0, changed_by, 0])
            return True
        except Exception as e:
            print('Database processing error')
            return False

    def __enter__(self):
        return self

    def __exit__(self, ext_type, exc_value, traceback):
        self.cur.close()
        if isinstance(exc_value, Exception):
            self.con.rollback()
        else:
            self.con.commit()
        self.con.close()

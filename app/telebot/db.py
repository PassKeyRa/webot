import sqlite3


class DB:
    def __init__(self):
        self.con = sqlite3.connect('sqlite.db')
        self.cur = self.con.cursor()

    def close(self):
        self.cur.close()

    def create_groups_table(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS groups ("
                         "chat_id INTEGER PRIMARY KEY NOT NULL,"
                         "activated INTEGER,"
                         "last_message_id INTEGER)")

    def create_trash_chat_table(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS trash_chat ("
                         "chat_id INTEGER PRIMARY KEY NOT NULL,"
                         "activated INTEGER,"
                         "action_user_id INTEGER)")

    def activate_chat(self, chat_id, changer_id):
        count = list(self.cur.execute("SELECT COUNT(*) FROM trash_chat").fetchall()[0])[0]
        if count == 0:
            self.cur.execute("INSERT INTO trash_chat VALUES (?, ?, ?)", [chat_id, 1, changer_id])
        else:
            self.cur.execute("UPDATE trash_chat SET "
                             "chat_id = ?,"
                             "activated = ?,"
                             "action_user_id = ? WHERE chat_id IN "
                             "(SELECT chat_id FROM trash_chat ORDER BY chat_id LIMIT 1)", [chat_id, 1, changer_id])

    def deactivate_chat(self, chat_id, changer_id):
        count = list(self.cur.execute("SELECT COUNT(*) FROM trash_chat").fetchall()[0])[0]
        if count == 0:
            self.cur.execute("INSERT INTO trash_chat VALUES (?, ?, ?)", [chat_id, 0, changer_id])
        else:
            self.cur.execute("UPDATE trash_chat SET "
                             "chat_id = ?,"
                             "activated = ?,"
                             "action_user_id = ? WHERE chat_id IN "
                             "(SELECT chat_id FROM trash_chat ORDER BY chat_id LIMIT 1)", [chat_id, 0, changer_id])

    def __enter__(self):
        return self

    def __exit__(self, ext_type, exc_value, traceback):
        self.cur.close()
        if isinstance(exc_value, Exception):
            self.con.rollback()
        else:
            self.con.commit()
        self.con.close()

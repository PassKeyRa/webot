import sqlite3

con = sqlite3.connect('sqlite.db')
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS groups (chat_id INTEGER, activated INTEGER, last_message_id INTEGER)")

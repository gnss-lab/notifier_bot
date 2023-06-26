import sqlite3
con = sqlite3.connect("test.db")

cur = con.cursor()

# cur.execute("CREATE TABLE if not exists messages(id INTEGER PRIMARY KEY, message TEXT, read INTEGER)")

def get_messages():
	cur.execute("SELECT * from messages")
	return cur.fetchall()

def get_message(mid):
	cur.execute("SELECT * from messages WHERE id = ? LIMIT 1", (mid,))
	return cur.fetchone()

def mark_message_as_read(mid):
	cur.execute("UPDATE messages SET read = 1 WHERE id = ?", (mid,))
	con.commit()

def get_unread_messages():
	cur.execute("SELECT id, message from messages WHERE read = 0")
	return cur.fetchall()

def add_unread_message(text):
	cur.execute("INSERT INTO messages (message, read) VALUES (?, ?)", (text, 0))
	con.commit()


add_unread_message("hi2")
# print(get_messages())

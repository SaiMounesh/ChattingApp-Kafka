import sqlite3

# Create or connect to SQLite database
def create_connection():
    return sqlite3.connect('messages.db')

def create_table():
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            sender TEXT,
                            recipient TEXT,
                            message TEXT,
                            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error creating table: {e}")

def store_message(sender, recipient, message):
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO messages (sender, recipient, message) VALUES (?, ?, ?)", 
                       (sender, recipient, message))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error storing message: {e}")

def get_messages_for_user(username, page=1, page_size=10):
    try:
        conn = create_connection()
        cursor = conn.cursor()
        offset = (page - 1) * page_size
        cursor.execute('''SELECT sender, recipient, message, timestamp
                          FROM messages
                          WHERE recipient = ? OR sender = ?
                          ORDER BY timestamp DESC
                          LIMIT ? OFFSET ?''', (username, username, page_size, offset))
        messages = cursor.fetchall()
        conn.close()
        return messages
    except Exception as e:
        print(f"Error retrieving messages: {e}")
        return []

if __name__ == "__main__":
    create_table()

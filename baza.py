from datetime import datetime
import sqlite3 

def init_db():
    try:
        conn = sqlite3.connect('Taxi_users.db')
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY,
                        username TEXT,
                        first_name TEXT,
                        last_name TEXT,
                        date_joined TEXT,
                        Number INTEGER, 
                        ban INTEGER DEFAULT 0
                )''')

        conn.commit()
    except sqlite3.Error as e:
        print(f"Ошибка при создании базы данных: {e}")
    finally:
        if conn:
            conn.close()


def user_exists(user_id):
    try:
        conn = sqlite3.connect('Taxi_users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user = c.fetchone()

        return user is not None  
    except sqlite3.Error as e:
        print(f"Ошибка при проверке пользователя: {e}")
        return False
    finally:
        if conn:
            conn.close()


def add_user_to_db(user_id, username, first_name, last_name, number):
    try:
        conn = sqlite3.connect('Taxi_users.db')
        c = conn.cursor()
        c.execute('''INSERT INTO users (user_id, username, first_name, last_name, date_joined, Number) 
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  (user_id, username, first_name, last_name, 
                   datetime.now().strftime("%Y-%m-%d %H:%M:%S"), number))

        conn.commit()
    except sqlite3.Error as e:
        print(f"Ошибка при добавлении пользователя: {e}")
    finally:
        if conn:
            conn.close()


init_db()

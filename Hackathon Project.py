import sqlite3

def create_database():
    conn = sqlite3.connect('SmoothCutZ.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS Booking (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT,
                        service TEXT,
                        price TEXT,
                        date TEXT,
                        time TEXT
                    )''')

    conn.commit()
    conn.close()
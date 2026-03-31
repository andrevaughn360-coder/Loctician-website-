from flask import Flask, request, jsonify, render_template
import sqlite3
from datetime import datetime
import os

# Ensure Flask knows where templates are
template_path = os.path.join(os.path.dirname(__file__), 'templates')
app = Flask(__name__, template_folder=template_path)

DB_FILE = 'SmoothCutZ.db'

# ===== Create DB & table =====
def create_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Booking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            service TEXT NOT NULL,
            price TEXT NOT NULL,
            payment_type TEXT,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            confirmed INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

create_database()

# ===== Add booking =====
def add_booking(username, service, price, date, time, payment_type=None):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Booking (username, service, price, date, time, payment_type)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (username, service, price, date, time, payment_type))
    conn.commit()
    conn.close()

# ===== Routes =====
@app.route('/')
def main():
    return render_template('smooth_final.html')

@app.route('/book', methods=['POST'])
def book():
    data = request.get_json()

    # Validate required fields
    required = ['username', 'service', 'price', 'date', 'time']
    for field in required:
        if field not in data or not data[field]:
            return jsonify({"status": "error", "message": f"Missing field: {field}"}), 400

    # Validate date and time
    try:
        booking_datetime_str = f"{data['date']} {data['time']}"
        booking_datetime = datetime.strptime(booking_datetime_str, "%Y-%m-%d %H:%M")
        if booking_datetime < datetime.now():
            return jsonify({"status": "error", "message": "Cannot book past date/time"}), 400
    except ValueError:
        return jsonify({"status": "error", "message": "Invalid date/time format"}), 400

    # Save booking to DB
    add_booking(data['username'], data['service'], data['price'], data['date'], data['time'])

    # Log stylist confirmation (mock)
    print(f"New booking confirmed for {data['username']} on {data['date']} at {data['time']}")

    return jsonify({"status": "success"}), 200

# ===== Run server =====
if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
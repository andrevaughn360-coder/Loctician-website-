import sqlite3
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# ===== 1. Create database & table =====
def create_database():
    conn = sqlite3.connect('SmoothCutZ.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Booking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            service TEXT,
            price TEXT,
            date TEXT,
            time TEXT
        )
    ''')
    conn.commit()
    conn.close()

create_database()  # ensure DB exists

# # ===== 2. Add booking function =====
def add_booking(username, service, price, date, time):
    conn = sqlite3.connect('SmoothCutZ.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Booking (username, service, price, date, time)
        VALUES (?, ?, ?, ?, ?)
    ''', (username, service, price, date, time))
    conn.commit()
    conn.close()

# # ===== 3. Route to handle frontend bookings =====
# @app.route('/book', methods=['POST'])
# def book():
    # data = request.get_json()
    # add_booking(data['username'], data['service'], data['price'], data['date'], data['time'])
    # return jsonify({"status": "success"}), 200

# @app.route('/', methods=['POST'])
# def main():
#     data = request.get_json()
#     return "Hello World"
#     # add_booking(data['username'], data['service'], data['price'], data['date'], data['time'])
#     # return jsonify({"status": "success"}), 200

@app.route('/')
def main():
    return render_template('index.html')

# ===== 4. Run Flask server =====
if __name__ == '__main__':
    app.run(host="10.22.71.30", debug=True)

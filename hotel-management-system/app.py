from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database initialization
def init_db():
    conn = sqlite3.connect('hotel.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_type TEXT NOT NULL,
            price INTEGER NOT NULL,
            availability TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS guests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            room_id INTEGER,
            FOREIGN KEY (room_id) REFERENCES rooms (id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guest_name TEXT NOT NULL,
            comment TEXT NOT NULL
        )
    ''')
    cursor.execute('''
INSERT INTO rooms (room_type, price, availability)
VALUES
    ('Single', 100, 'Yes'),
    ('Double', 200, 'Yes'),
    ('Suite', 300, 'Yes');
''')

    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/rooms')
def rooms():
    conn = sqlite3.connect('hotel.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM rooms')
    rooms = cursor.fetchall()
    conn.close()
    return render_template('rooms.html', rooms=rooms)

@app.route('/book', methods=['POST'])
def book_room():
    name = request.form['name']
    email = request.form['email']
    room_id = request.form['room_id']
    
    conn = sqlite3.connect('hotel.db')
    cursor = conn.cursor()

    # Update room availability
    cursor.execute('UPDATE rooms SET availability = "No" WHERE id = ?', (room_id,))
    
    # Insert guest details
    cursor.execute('INSERT INTO guests (name, email, room_id) VALUES (?, ?, ?)', (name, email, room_id))
    
    conn.commit()
    conn.close()
    return redirect(url_for('rooms'))


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        name = request.form['name']
        comment = request.form['comment']
        conn = sqlite3.connect('hotel.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO feedback (guest_name, comment) VALUES (?, ?)', (name, comment))
        conn.commit()
        conn.close()
        return redirect(url_for('feedback'))
    conn = sqlite3.connect('hotel.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM feedback')
    feedbacks = cursor.fetchall()
    conn.close()
    return render_template('feedback.html', feedbacks=feedbacks)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

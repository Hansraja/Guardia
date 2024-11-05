from flask import Flask, render_template
import sqlite3
from config import DATABASE_PATH

app = Flask(__name__, static_folder='user_images/')

# Function to fetch all users from the database
def fetch_all_users():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, mobile FROM users')
    users = cursor.fetchall()
    conn.close()
    return users

# Route to display the home page
@app.route('/')
def home():
    return render_template('home.html')

# Route to display all users
@app.route('/users')
def show_users():
    users = fetch_all_users()
    return render_template('users.html', users=users)

# Route to display a user's entry logs
@app.route('/user/<int:user_id>')
def show_user_entries(user_id):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM entries WHERE user_id = ?', (user_id,))
    entries = cursor.fetchall()
    conn.close()
    return render_template('entries.html', entries=entries)

@app.route('/user_images/<path>')
def get_user_image(path):
    return app.send_static_file(path)

from flask import Flask, render_template, request, redirect, url_for
import database

app = Flask(__name__)

# Database setup
DATABASE = 'urls.db'
create_table_sql = ''' CREATE TABLE IF NOT EXISTS urls (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        original_url TEXT NOT NULL,
                                        short_code TEXT UNIQUE NOT NULL
                                    ); '''

# Create the database and table
conn = database.create_connection(DATABASE)
if conn:
    database.create_table(conn, create_table_sql)
    database.close_connection(conn)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten_url():
    original_url = request.form['original_url']  # Ensure this matches your form input's name attribute
    short_code = generate_short_code()
    # Assuming you have a function in the 'database' module to insert URLs
    database.insert_url(conn, original_url, short_code)
    # Construct the short URL
    short_url = request.host_url + short_code
    return render_template('shortened.html', short_url=short_url)

@app.route('/<short_code>')
def shortened_url(short_code):
    conn = database.create_connection(DATABASE)
    if conn:
        original_url = database.get_short_url(conn, short_code)
        database.close_connection(conn)
    if original_url:
        return redirect(original_url)
    else:
        return 'Shortened URL not found', 404

import random
import string

def generate_short_code(original_url):
    """Generates a random short code."""
    while True:
        short_code = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))
        # Check if the short code is already in use (you'll need to implement this)
        if not is_short_code_in_use(short_code):
            return short_code

def is_short_code_in_use(short_code):
    """Checks if a short code is already in use in the database."""
    conn = database.create_connection(DATABASE)
    if conn:
        sql = ''' SELECT 1 FROM urls WHERE short_code = ? '''
        cur = conn.cursor()
        cur.execute(sql, (short_code,))
        row = cur.fetchone()
        database.close_connection(conn)
        return bool(row)brew install python


if __name__ == '__main__':
    app.run(debug=True)

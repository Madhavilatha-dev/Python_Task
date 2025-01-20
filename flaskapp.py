from flask import Flask, request, jsonify, redirect
import hashlib
import sqlite3
import datetime

# Initialize Flask app
app = Flask(__name__)

# Base URL and database configuration
BASE_URL = 'http://short.ly/'
DATABASE = 'url_shortener.db'

# Initialize the database
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS urls (
                        id INTEGER PRIMARY KEY,
                        original_url TEXT NOT NULL,
                        shortened_url TEXT NOT NULL UNIQUE,
                        creation_time TEXT NOT NULL,
                        expiration_time TEXT NOT NULL,
                        access_count INTEGER DEFAULT 0,
                        password TEXT
                    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS access_logs (
                        id INTEGER PRIMARY KEY,
                        shortened_url TEXT NOT NULL,
                        access_time TEXT NOT NULL,
                        ip_address TEXT NOT NULL
                    )''')
    conn.commit()
    conn.close()

# Helper to generate a short URL
def generate_short_url(original_url):
    return hashlib.md5(original_url.encode()).hexdigest()[:6]

# API to create a short URL
@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    original_url = data.get('original_url')
    expiration_hours = data.get('expiration_hours', 24)

    if not original_url:
        return jsonify({'error': 'Original URL is required'}), 400

    # Compute expiration time
    creation_time = datetime.datetime.now()
    expiration_time = creation_time + datetime.timedelta(hours=expiration_hours)

    # Generate short URL
    short_url = generate_short_url(original_url)

    # Save to database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''INSERT OR REPLACE INTO urls (original_url, shortened_url, creation_time, expiration_time)
                      VALUES (?, ?, ?, ?)''',
                   (original_url, short_url, creation_time.isoformat(), expiration_time.isoformat()))
    conn.commit()
    conn.close()

    return jsonify({'shortened_url': f'{BASE_URL}{short_url}'}), 201

# API to redirect to the original URL
@app.route('/<short_url>', methods=['GET'])
def redirect_to_original(short_url):
    password = request.args.get('password')
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''SELECT original_url, expiration_time, password FROM urls WHERE shortened_url = ?''', (short_url,))
    result = cursor.fetchone()

    if not result:
        return jsonify({'error': 'URL not found'}), 404

    original_url, expiration_time, stored_password = result

    if datetime.datetime.fromisoformat(expiration_time) < datetime.datetime.now():
        return jsonify({'error': 'URL has expired'}), 410
    
    if stored_password != password:
        return jsonify({'error': 'Password is incorrect or missing'}), 403

    # Log the access
    cursor.execute('''INSERT INTO access_logs (shortened_url, access_time, ip_address)
                      VALUES (?, ?, ?)''',
                   (short_url, datetime.datetime.now().isoformat(), request.remote_addr))
    cursor.execute('''UPDATE urls SET access_count = access_count + 1 WHERE shortened_url = ?''', (short_url,))
    conn.commit()
    conn.close()

    return redirect(original_url)

# API to get analytics
@app.route('/analytics/<short_url>', methods=['GET'])
def get_analytics(short_url):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''SELECT original_url, creation_time, expiration_time, access_count FROM urls WHERE shortened_url = ?''', (short_url,))
    url_data = cursor.fetchone()

    if not url_data:
        return jsonify({'error': 'URL not found'}), 404

    original_url, creation_time, expiration_time, access_count = url_data
    cursor.execute('''SELECT access_time, ip_address FROM access_logs WHERE shortened_url = ?''', (short_url,))
    access_logs = cursor.fetchall()
    conn.close()

    return jsonify({
        'original_url': original_url,
        'creation_time': creation_time,
        'expiration_time': expiration_time,
        'access_count': access_count,
        'access_logs': [{'access_time': log[0], 'ip_address': log[1]} for log in access_logs]
    })

# Initialize the database and run the app
init_db()

if __name__ == '__main__':
    app.run(debug=True)

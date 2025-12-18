import flask
import sqlite3

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = flask.Flask(
    __name__,
    static_folder="static",
    static_url_path="/"
)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day"],
    storage_uri="memory://",
)

conn = sqlite3.connect('gifts.db') 
cursor = conn.cursor()  
cursor.execute('''
    CREATE TABLE IF NOT EXISTS gifts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        gift TEXT NOT NULL
    )
''')

conn.commit()
conn.close()

@app.route("/", methods=["GET"])
@limiter.exempt
def index():
    return flask.send_from_directory("static", "index.html")

@app.route("/gifts", methods=["POST"])
@limiter.limit("1 per day")
def insert_gift():
    data = flask.request.get_json()
    name = data.get('name')
    gift = data.get('gift')

    conn = sqlite3.connect('gifts.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO gifts (name, gift) VALUES (?, ?)', (name, gift))
    conn.commit()
    conn.close()

    return '', 201

@app.route("/gifts", methods=["GET"])
@limiter.limit("67 per day")
def receive_gifts():
    conn = sqlite3.connect("gifts.db")
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, gift FROM gifts')
    rows = cursor.fetchall()
    conn.close()

    gifts = [{
        'id': row[0],
        'name': row[1],
        'gift': row[2]
    } for row in rows]

    return flask.jsonify(gifts)

if __name__ == "__main__":
    from os import environ
    app.run(host='0.0.0.0', port=int(environ.get('PORT', 5000)))
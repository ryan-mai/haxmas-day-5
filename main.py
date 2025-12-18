import flask
import sqlite3

app = flask.Flask(
    __name__,
    static_folder="static",
    static_url_path="/"
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

app.get("/")
def index():
    return flask.send_from_directory("static", "index.html")

app.post("/gifts")
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

app.get("/gifts")
def recieve_gifts():
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
    app.run()
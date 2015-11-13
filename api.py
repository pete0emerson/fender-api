import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

# configuration
DATABASE = '/home/pete/db/fender.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'fender'
PASSWORD = 'fenderpw'

app = Flask(__name__)

def connect_db():
    return sqlite3.connect(DATABASE)

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.route('/db')
def db_get():
    db = get_db()
    cur = db.execute('select title, text from entries order by id desc')
    entries = cur.fetchall()
    e = []
    for entry in entries:
        e.append({'title':entry[0],'text':entry[1]})
    print "Entries: %s" % e
    return render_template('show_entries.html', entries=e)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/_status/')
def status():
    return 'OK'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)

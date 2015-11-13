import sqlite3
import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

# configuration
# path to fender db needs to be set in environmental variable
DATABASE = os.environ['FENDER_DB']
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
    cur = db.execute('select * from messages')
    entries = cur.fetchall()
    return str(entries)

@app.route('/<state>/<plate>', methods=['GET'])
def get_all_messages(state, plate):
    db = get_db()
    cur = db.execute("select * from messages where state='%s' and plate='%s'" % (state, plate))
    entries = cur.fetchall()
    return str(entries)

@app.route('/<state>/<plate>/post', methods=['POST'])
def post_message(state, plate):
    data = request.json
    msg = data['message']
    db = get_db()
    cur = db.execute("insert into messages (message, state, plate) values ('%s','%s','%s')" % (msg, state, plate))
    db.commit()
    return msg

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/_status/')
def status():
    return 'OK'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)

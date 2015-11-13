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

@app.route('/<state>/<plate>', methods=['POST'])
def post_message(state, plate):
    data = request.json
    msg = data['message']
    db = get_db()
    db.execute("insert into messages (message, state, plate) values ('%s','%s','%s')" % (msg, state, plate))
    db.commit()
    return msg

@app.route('/users/add', methods=['POST'])
def add_subscriber(state, plate):
    data = request.json
    db = get_db()
    db.execute("insert into subscribers (phone_number, state, plate) values ('%s','%s','%s')" % (data['phone_number'], data['state'], data['plate']))
    db.commit()
    return 'OK'

@app.route('/users/<state>', methods=['GET'])
def get_subscribers_by_state(state):
    data = request.json
    db = get_db()
    cur = db.execute("select * from subscribers where state='%s'" % state)
    entries = cur.fetchall()
    return str(entries)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/_status/')
def status():
    return 'OK'

@app.route('/twilio', methods=['POST'])
def twilio():
    body = request.form['Body']
    print "I got a body of: --->%s<---" % body
    print request.get_data()
    return 'OK'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)

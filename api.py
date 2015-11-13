import sqlite3
import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify, make_response, current_app
from datetime import timedelta
from functools import update_wrapper

# configuration
# path to fender db needs to be set in environmental variable
DATABASE = os.environ['FENDER_DB']
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'fender'
PASSWORD = 'fenderpw'

app = Flask(__name__)

# allow for crossdomain
def crossdomain(origin=None, methods=None, headers=None, max_age=21600, attach_to_all=True, automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

def connect_db():
    return sqlite3.connect(DATABASE)

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.route('/db')
@crossdomain(origin='*')
def db_get():
    db = get_db()
    cur = db.execute('select * from messages')
    entries = cur.fetchall()
    return str(entries)

@app.route('/<state>/<plate>', methods=['GET'])
@crossdomain(origin='*')
def get_all_messages(state, plate):
    db = get_db()
    cur = db.execute("select * from messages where state='%s' and plate='%s'" % (state, plate))
    entries = cur.fetchall()
    return str(entries)

@app.route('/<state>/<plate>', methods=['POST'])
@crossdomain(origin='*')
def post_message(state, plate):
    data = request.json
    msg = data['message']
    db = get_db()
    db.execute("insert into messages (message, state, plate) values ('%s','%s','%s')" % (msg, state, plate))
    db.commit()
    return msg

@app.route('/users/add', methods=['POST'])
@crossdomain(origin='*')
def add_subscriber(state, plate):
    data = request.json
    db = get_db()
    db.execute("insert into subscribers (phone_number, state, plate) values ('%s','%s','%s')" % (data['phone_number'], data['state'], data['plate']))
    db.commit()
    return 'OK'

@app.route('/users/<state>', methods=['GET'])
@crossdomain(origin='*')
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
@crossdomain(origin='*')
def twilio():
    body = request.form['Body']
    data = parse_twilio_data(body)
    db = get_db()
    db.execute("insert into messages (message, state, plate) values (?,?,?)", % (data['msg'], data['state'], data['plate']))
    db.commit()
    return 'OK'

def parse_twilio_data(body):
    parts = body.split('.')
    msg = parts[1]
    state_license = parts[0].split(' ')
    state = state_license[0]
    plate = ''.join(state_license[3:])
    return {'state': state, 'plate': plate, 'msg': msg}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)

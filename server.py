import os
import uuid
from flask import Flask, session, render_template, request, redirect, url_for, session
import psycopg2
import psycopg2.extras
from flask.ext.socketio import SocketIO, emit

app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app)

messages = [{'text':'test', 'name':'testName'}]
users = {}

currentuser = ''

def connectToDB():
    connectionString = 'dbname=chat user=postgres password=fuckoff host=localhost'
    print connectionString
    try:
        return psycopg2.connect(connectionString)
    except:
        print("Can't connect to database")

def updateRoster():
    names = []
    for user_id in  users:
        print users[user_id]['username']
        if len(users[user_id]['username'])==0:
            names.append('Anonymous')
        else:
            names.append(users[user_id]['username'])
    print 'broadcasting names'
    
    emit('roster', names, broadcast=True)
    

@socketio.on('connect', namespace='/chat')
def test_connect():
    db = connectToDB()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    session['uuid']=uuid.uuid1()
    session['username']='starter name'
    print 'connected'
    
    users[session['uuid']]={'username':'New User'}
    updateRoster()
    cur.execute("""SELECT * FROM messages LIMIT 20;""")
    chatmsg = cur.fetchall()
    for text in chatmsg:
        print text['text']
        thing = {'text':text['text'], 'name':text['userperson']}
        emit('message', thing, broadcast=True)

@socketio.on('message', namespace='/chat')
def new_message(text):
    db = connectToDB()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    uid = session['userid']
    try:
        cur.execute("""INSERT INTO messages VALUES (DEFAULT, %s, %s);""", (text, session['username']) )
    except:
        print("ERROR inserting into messages")
    db.commit()
    
    cur.execute("""SELECT * FROM messages;""")
    chatmsg = cur.fetchall()
    #tmp = {'text':message, 'name':'testName'}
    tmp = {'text':text, 'name':users[session['uuid']]['username']}
    messages.append(tmp)
    emit('message', tmp, broadcast=True)
    updateRoster()
    
@socketio.on('identify', namespace='/chat')
def on_identify(message):
    print 'identify' + message
    users[session['uuid']]={'username':message}
    updateRoster()

@socketio.on('search', namespace='/chat')
def on_search(term):
    db = connectToDB()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    print 'find '  + term
    thing = term
    query = "SELECT * FROM messages WHERE text LIKE %s OR userperson LIKE %s;"
    cur.execute(query, (term, thing))
    finds = cur.fetchall()
    if not finds:
        print "no finds"
    else:
        for find in finds:
            thing = {'text':find['text'], 'name':find['userperson']}
            emit('search', thing, broadcast=True)
    


@socketio.on('login', namespace='/chat')
def on_login(data):
    db = connectToDB()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    print 'login '  + data['username']
    uname = data['username']
    pw = data['password']
    currentuser = uname
    query = "SELECT * FROM users WHERE username = %s AND password = %s;"
    print query
    cur.execute(query, (uname, pw))
    fetchingthing = cur.fetchone()
    x = 3
    if not fetchingthing:
        print "No username found."
        x = 1
        emit('login', x, broadcast=True)
    else:
        print "it worked biatch"
        session['username'] = uname
        session['userid'] = fetchingthing['userid']
        
        emit('login', 0, broadcast=True)
    
    users[session['uuid']]={'username':uname}
    updateRoster()


    
@socketio.on('disconnect', namespace='/chat')
def on_disconnect():
    print 'disconnect'
    if session['uuid'] in users:
        del users[session['uuid']]
        updateRoster()

@app.route('/')
def hello_world():
    print 'in hello world'
    return app.send_static_file('index.html')
    return 'Hello World!'

@app.route('/js/<path:path>')
def static_proxy_js(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(os.path.join('js', path))
    
@app.route('/css/<path:path>')
def static_proxy_css(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(os.path.join('css', path))
    
@app.route('/img/<path:path>')
def static_proxy_img(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(os.path.join('img', path))
    
if __name__ == '__main__':
    print "A"

    socketio.run(app, host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)))
     

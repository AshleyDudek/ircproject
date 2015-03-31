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
    #cur.execute("""SELECT * FROM messages LIMIT 20;""")
    #chatmsg = cur.fetchall()
    #for text in chatmsg:
        #print text['text']
        #thing = {'text':text['text'], 'name':text['userperson']}
        #emit('message', thing, broadcast=True)

@socketio.on('register', namespace='/chat')
def on_register(user):
    db = connectToDB()
    cur1 = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query1 = "SELECT * FROM users WHERE username=%s AND username=%s;"
    cur1.execute(query1, (user['username'], user['username']))
    anyothers = cur1.fetchone()
    if not anyothers:
        cur2 = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query2 = "INSERT INTO users (username, password) VALUES (%s, %s);"
        try:
            cur2.execute(query2, (user['username'], user['password']))
        except:
            print("ERROR inserting into users")
        db.commit()
        emit('register', 'User registered', broadcast=True)
    else:
        emit('register', 'There is already a user with that username', broadcast=True)
    
@socketio.on('subto', namespace='/chat')
def on_subto(room):
    db = connectToDB()
    cur1 = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    uid = session['userid']
    dudename = users[session['uuid']]['username']
    query1 = "SELECT * FROM chatrooms WHERE name=%s AND chatpassword=%s;"
    cur1.execute(query1, (room['room'], room['password']))
    theroom = cur1.fetchone()
    if not theroom:
        print "no room"
    else:
        print "i see the room i want to subscribe to"
        #cur2 = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur3 = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        #query2 = "SELECT * FROM chatrooms WHERE name=%s AND name=%s;"
        #cur2.execute(query2, (room['room'], room['room']))
        #croom = cur2.fetchone()
        #query3 = "INSERT INTO sub VALUES (%s, %s);"
        print theroom['roomid']
        print uid
        try:
            cur3.execute("""INSERT INTO sub VALUES (%s, %s);""", (theroom['roomid'], uid))
        except:
            print("ERROR inserting into messages sub")
        db.commit()

@socketio.on('message1', namespace='/chat')
def new_message1(text):
    db = connectToDB()
    cur1 = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur2 = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur3 = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur4 = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    uid = session['userid']
    dudename = users[session['uuid']]['username']
    #words = text['text']
    #room=text['room']
    #cur1.execute("""SELECT userid FROM users WHERE username=%s AND username=%s;""", (dudename, dudename))
    #usid = cur1.fetchone()
    
    #cur2.execute("""SELECT roomid FROM chatrooms WHERE name=%s AND name=%s""", (roomname, roomname))
    #rid = cur2.fetchone()
    
    print session['userid']
    print session['room1id']
    print text
    try:
        cur3.execute("""INSERT INTO messages (text, userid, roomid) VALUES (%s, %s, %s);""", (text, session['userid'], session['room1id']) )
    except:
        print("ERROR inserting into messages 1")
    db.commit()
    
    cur4.execute("""SELECT * FROM messages;""")
    chatmsg = cur4.fetchall()
    #tmp = {'text':message, 'name':'testName'}
    tmp = {'text':text, 'name':users[session['uuid']]['username']}
    messages.append(tmp)
    emit('message1', tmp, broadcast=True)
    updateRoster()
    
@socketio.on('message2', namespace='/chat')
def new_message2(text):
    db = connectToDB()
    cur1 = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur2 = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur3 = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur4 = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    uid = session['userid']
    dudename = users[session['uuid']]['username']
    #words = text['text']
    #room=text['room']
    #cur1.execute("""SELECT userid FROM users WHERE username=%s AND username=%s;""", (dudename, dudename))
    #usid = cur1.fetchone()
    
    #cur2.execute("""SELECT roomid FROM chatrooms WHERE name=%s AND name=%s""", (roomname, roomname))
    #rid = cur2.fetchone()
    
    print session['userid']
    print session['room2id']
    print text
    try:
        cur3.execute("""INSERT INTO messages (text, userid, roomid) VALUES (%s, %s, %s);""", (text, session['userid'], session['room2id']) )
    except:
        print("ERROR inserting into messages 2")
    db.commit()
    
    cur4.execute("""SELECT * FROM messages;""")
    chatmsg = cur4.fetchall()
    #tmp = {'text':message, 'name':'testName'}
    tmp = {'text':text, 'name':users[session['uuid']]['username']}
    messages.append(tmp)
    emit('message2', tmp, broadcast=True)
    updateRoster()
    
@socketio.on('message3', namespace='/chat')
def new_message3(text):
    db = connectToDB()
    cur1 = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur2 = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur3 = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur4 = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    uid = session['userid']
    dudename = users[session['uuid']]['username']
    #words = text['text']
    #room=text['room']
    #cur1.execute("""SELECT userid FROM users WHERE username=%s AND username=%s;""", (dudename, dudename))
    #usid = cur1.fetchone()
    
    #cur2.execute("""SELECT roomid FROM chatrooms WHERE name=%s AND name=%s""", (roomname, roomname))
    #rid = cur2.fetchone()
    
    print session['userid']
    print session['room3id']
    print text
    try:
        cur3.execute("""INSERT INTO messages (text, userid, roomid) VALUES (%s, %s, %s);""", (text, session['userid'], session['room3id']) )
    except:
        print("ERROR inserting into messages 3")
    db.commit()
    
    cur4.execute("""SELECT * FROM messages;""")
    chatmsg = cur4.fetchall()
    #tmp = {'text':message, 'name':'testName'}
    tmp = {'text':text, 'name':users[session['uuid']]['username']}
    messages.append(tmp)
    emit('message3', tmp, broadcast=True)
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
    uid = session['userid']
    dudename = users[session['uuid']]['username']
    print 'find '  + term
    thing = '%' + term + '%'
    query = "SELECT messages.text AS text, users.username AS username, chatrooms.name AS roomname FROM messages INNER JOIN chatrooms ON messages.roomid=chatrooms.roomid INNER JOIN users ON messages.userid=users.userid WHERE messages.text LIKE %s OR users.username LIKE %s;"
    cur.execute(query, (thing, thing))
    finds = cur.fetchall()
    if not finds:
        print "no finds"
    else:
        for find in finds:
            #db2 = connectToDB()
            cur2 = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
            query2 = "SELECT * FROM chatrooms INNER JOIN sub ON chatrooms.roomid=sub.roomid INNER JOIN users ON sub.userid=users.userid WHERE users.username=%s AND chatrooms.name=%s;"
            place = find['roomname']
            print 'is ' + dudename + ' subbed to ' + place + '?'
            cur2.execute(query2, (dudename, place))
            subbed = cur2.fetchone()
            print subbed
            if not subbed:
                print 'message ' + find['text'] + ' not subbed'
            else:
                thing={'text':find['text'], 'name':find['username'], 'room':find['roomname']}
                emit('search', thing, broadcast=True)
            
            #thing = {'text':find['text'], 'name':find['userperson']}
            #emit('search', thing, broadcast=True)
    

@socketio.on('enterroom1', namespace='/chat')
def on_enter1(room):
    db = connectToDB()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    print 'enter '  + room
    uid = session['userid']
    dudename = users[session['uuid']]['username']
    query = "SELECT * FROM chatrooms INNER JOIN sub ON chatrooms.roomid=sub.roomid INNER JOIN users ON sub.userid=users.userid WHERE users.username=%s AND chatrooms.name=%s;"
    print query
    cur.execute(query, (dudename, room))
    rooms = cur.fetchone();
    if not rooms:
        print "no rooms for room 1"
    else:
        print "in room 1"
        thing = {'id':rooms['roomid'], 'name':rooms['name'], 'gotin':0}
        session['room1id'] = rooms['roomid']
        emit('enterroom1', room, broadcast=True)
    
@socketio.on('load1', namespace='/chat')
def on_load1(room):
    db = connectToDB()
    print room
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = "SELECT messages.text AS text, users.username AS dude FROM messages INNER JOIN chatrooms ON messages.roomid=chatrooms.roomid INNER JOIN users ON messages.userid=users.userid WHERE chatrooms.name=%s AND chatrooms.name=%s;"
    cur.execute(query, (room, room))
    chatmsg = cur.fetchall()
    for text in chatmsg:
        print text['text']
        thing = {'text':text['text'], 'name':text['dude']}
        emit('message1', thing, broadcast=True)
        
@socketio.on('enterroom2', namespace='/chat')
def on_enter2(room):
    db = connectToDB()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    print 'enter '  + room
    uid = session['userid']
    dudename = users[session['uuid']]['username']
    query = "SELECT * FROM chatrooms INNER JOIN sub ON chatrooms.roomid=sub.roomid INNER JOIN users ON sub.userid=users.userid WHERE users.username=%s AND chatrooms.name=%s;"
    print query
    cur.execute(query, (dudename, room))
    rooms = cur.fetchone();
    if not rooms:
        print "no rooms for room 2"
    else:
        print "in room 2"
        thing = {'id':rooms['roomid'], 'name':rooms['name'], 'gotin':0}
        session['room2id'] = rooms['roomid']
        emit('enterroom2', room, broadcast=True)
    
@socketio.on('load2', namespace='/chat')
def on_load2(room):
    db = connectToDB()
    print room
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = "SELECT messages.text AS text, users.username AS dude FROM messages INNER JOIN chatrooms ON messages.roomid=chatrooms.roomid INNER JOIN users ON messages.userid=users.userid WHERE chatrooms.name=%s AND chatrooms.name=%s;"
    cur.execute(query, (room, room))
    chatmsg = cur.fetchall()
    for text in chatmsg:
        print text['text']
        thing = {'text':text['text'], 'name':text['dude']}
        emit('message2', thing, broadcast=True)

@socketio.on('enterroom3', namespace='/chat')
def on_enter3(room):
    db = connectToDB()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    print 'enter '  + room
    uid = session['userid']
    dudename = users[session['uuid']]['username']
    query = "SELECT * FROM chatrooms INNER JOIN sub ON chatrooms.roomid=sub.roomid INNER JOIN users ON sub.userid=users.userid WHERE users.username=%s AND chatrooms.name=%s;"
    print query
    cur.execute(query, (dudename, room))
    rooms = cur.fetchone();
    if not rooms:
        print "no rooms for room 3"
    else:
        print "in room 3"
        thing = {'id':rooms['roomid'], 'name':rooms['name'], 'gotin':0}
        session['room3id'] = rooms['roomid']
        emit('enterroom3', room, broadcast=True)
    
@socketio.on('load3', namespace='/chat')
def on_load3(room):
    db = connectToDB()
    print room
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = "SELECT messages.text AS text, users.username AS dude FROM messages INNER JOIN chatrooms ON messages.roomid=chatrooms.roomid INNER JOIN users ON messages.userid=users.userid WHERE chatrooms.name=%s AND chatrooms.name=%s;"
    cur.execute(query, (room, room))
    chatmsg = cur.fetchall()
    for text in chatmsg:
        print text['text']
        thing = {'text':text['text'], 'name':text['dude']}
        emit('message3', thing, broadcast=True)


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
        print session['username']
        session['userid'] = fetchingthing['userid']
        print session['userid']
        
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
     

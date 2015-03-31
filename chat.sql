DROP DATABASE IF EXISTS chat;
CREATE DATABASE chat;

\c chat;

-- USERS

DROP TABLE IF EXISTS users;
CREATE TABLE IF NOT EXISTS users (
  userid serial,
  username varchar(12) NOT NULL,
  password varchar(126) NOT NULL,
  PRIMARY KEY (userid)
)  ;

INSERT INTO users (username, password) VALUES ('ashley', 'ugh');
INSERT INTO users (username, password) VALUES ('tyler', 'gross');
INSERT INTO users (username, password) VALUES ('savannah', 'yay');

-- CHATROOMS

DROP TABLE IF EXISTS chatrooms;
CREATE TABLE IF NOT EXISTS chatrooms (
  roomid serial,
  name varchar(12) NOT NULL,
  chatpassword varchar(126) NOT NULL,
  PRIMARY KEY (roomid)
)  ;

INSERT INTO chatrooms (name, chatpassword) VALUES ('Friendship', 'not tyler');
INSERT INTO chatrooms (name, chatpassword) VALUES ('Video Games', 'fpl');
INSERT INTO chatrooms (name, chatpassword) VALUES ('Class Stuff', 'too many cooks');
INSERT INTO chatrooms (name, chatpassword) VALUES ('Tyler Sucks', 'all day');

-- ROOM/USER SUBSCRIPTION JUNCTION

DROP TABLE IF EXISTS sub;
CREATE TABLE IF NOT EXISTS sub (
  roomid int,
  userid int
);

INSERT INTO sub VALUES (1, 1);
INSERT INTO sub VALUES (1, 2);
INSERT INTO sub VALUES (1, 3);
INSERT INTO sub VALUES (2, 1);
INSERT INTO sub VALUES (2, 2);
INSERT INTO sub VALUES (2, 3);
INSERT INTO sub VALUES (3, 1);
INSERT INTO sub VALUES (3, 2);
INSERT INTO sub VALUES (3, 3);
INSERT INTO sub VALUES (4, 1);
INSERT INTO sub VALUES (4, 3);
  

-- MESSAGES

DROP TABLE IF EXISTS messages;
CREATE TABLE IF NOT EXISTS messages (
  messageid serial,
  text varchar(140),
  userid int NOT NULL,
  roomid int NOT NULL,
  PRIMARY KEY (messageid)
)  ;

INSERT INTO messages (text, userid, roomid) VALUES ('hey friends', 1, 1);
INSERT INTO messages (text, userid, roomid) VALUES ('ugh you', 2, 1);
INSERT INTO messages (text, userid, roomid) VALUES ('i like metroid', 3, 1);
INSERT INTO messages (text, userid, roomid) VALUES ('yayyy', 1, 1);
INSERT INTO messages (text, userid, roomid) VALUES ('metroid???', 3, 2);
INSERT INTO messages (text, userid, roomid) VALUES ('yes', 1, 2);
INSERT INTO messages (text, userid, roomid) VALUES ('no', 2, 2);
INSERT INTO messages (text, userid, roomid) VALUES ('when is sprint 2 due?', 2, 3);
INSERT INTO messages (text, userid, roomid) VALUES ('now', 1, 3);
INSERT INTO messages (text, userid, roomid) VALUES ('never', 3, 3);
INSERT INTO messages (text, userid, roomid) VALUES ('tyler sucks', 1, 4);
INSERT INTO messages (text, userid, roomid) VALUES ('i know', 3, 4);

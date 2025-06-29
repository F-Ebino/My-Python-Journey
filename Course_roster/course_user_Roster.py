import json
import sqlite3

db_connect = sqlite3.connect('Roster.sqlite')
db_cursor = db_connect.cursor()

db_cursor.executescript('''
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Member;
DROP TABLE IF EXISTS Course;

CREATE TABLE User (
    id     INTEGER PRIMARY KEY,
    name   TEXT UNIQUE
);

CREATE TABLE Course (
    id     INTEGER PRIMARY KEY,
    title  TEXT UNIQUE
);

CREATE TABLE Member (
    user_id     INTEGER,
    course_id   INTEGER,
    role        INTEGER,
    PRIMARY KEY (user_id, course_id)
)
''')

file_name = input('Enter file name >>')
if len(file_name) < 1:
    file_name = 'roster_data.json'

raw_data = open(file_name).read()
json_data = json.loads(raw_data)

for sub_list in json_data:

    name = sub_list[0]
    title = sub_list[1]
    role = sub_list[2]
    #print((name, title, role))
    
    db_cursor.execute('''INSERT OR IGNORE INTO User (name)
        VALUES ( ? )''', ( name, ) )
    db_cursor.execute('SELECT id FROM User WHERE name = ? ', (name, ))
    user_id = db_cursor.fetchone()[0]

    db_cursor.execute('''INSERT OR IGNORE INTO Course (title)
        VALUES ( ? )''', ( title, ) )
    db_cursor.execute('SELECT id FROM Course WHERE title = ? ', (title, ))
    course_id = db_cursor.fetchone()[0]

    db_cursor.execute('''INSERT OR REPLACE INTO Member
        (user_id, course_id, role) VALUES ( ?, ?, ? )''',
        ( user_id, course_id, role) )

    db_connect.commit()
    print("committed")

db_cursor.close()
print("closed")
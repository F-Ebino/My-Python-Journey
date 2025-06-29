import re
import sqlite3

db_connect = sqlite3.connect('Tracks_table.sqlite')
db_cursor = db_connect.cursor()

db_cursor.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Genre;                 
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;
                  
CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Genre (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    title   TEXT UNIQUE
);

CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY 
        AUTOINCREMENT UNIQUE,
    title TEXT  UNIQUE,
    album_id  INTEGER,
    genre_id  INTEGER,
    runtime INTEGER, rating INTEGER, plays INTEGER
);
''')

file_handle = open('tracks.csv')
for line in file_handle:
    columns_list= re.findall(r"(.+),(.+),(.+),(.+),(.+),(.+),(.+)", line)
    [(name, artist, album, plays, rating, runtime, genre)] = columns_list
    #print(columns_list)

    db_cursor.execute('''INSERT OR IGNORE INTO Artist (name) 
        VALUES ( ? )''', ( artist, ) )
    db_cursor.execute('SELECT id FROM Artist WHERE name = ? ', (artist, ))
    artist_id = db_cursor.fetchone()[0]

    db_cursor.execute('''INSERT OR IGNORE INTO Genre (name) 
        VALUES ( ? )''', ( genre, ) )
    db_cursor.execute('SELECT id FROM Genre WHERE name = ? ', (genre, ))
    genre_id = db_cursor.fetchone()[0]

    db_cursor.execute('''INSERT OR IGNORE INTO Album (title, artist_id) 
        VALUES ( ?, ? )''', ( album, artist_id ) )
    db_cursor.execute('SELECT id FROM Album WHERE title = ? ', (album, ))
    album_id = db_cursor.fetchone()[0]

    db_cursor.execute('''INSERT OR REPLACE INTO Track
        (title, album_id, genre_id, runtime, rating, plays) 
        VALUES ( ?, ?, ?, ?, ?, ? )''', 
        ( name, album_id, genre_id, runtime, rating, plays ) )
    
    db_connect.commit()
    print("committed")

db_cursor.close()
print("closed")
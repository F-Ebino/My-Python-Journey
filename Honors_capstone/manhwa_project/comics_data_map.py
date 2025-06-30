import sqlite3
import pandas as pd

# Connect to the flat data DB and the new normalized DB
src_conn = sqlite3.connect('manhwa_manhua.sqlite')
dst_conn = sqlite3.connect('comics.sqlite')

dst_conn.execute("PRAGMA foreign_keys = ON;")

cursor = dst_conn.cursor()

# Drop all tables if exist (order matters due to FK constraints)
tables = ['comic_authors', 'comic_genres','comics','authors',
         'genres', 'comic_types', 'countries','pubdates'
         ]

for table in tables:
    cursor.execute(f"DROP TABLE IF EXISTS {table}")

# Create tables fresh

cursor.execute("""
CREATE TABLE comic_types (
    comic_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
    type_name TEXT NOT NULL UNIQUE
)
""")

cursor.execute("""
CREATE TABLE countries (
    country_id INTEGER PRIMARY KEY AUTOINCREMENT,
    country_name TEXT NOT NULL UNIQUE
)
""")

cursor.execute("""
CREATE TABLE authors (
    author_id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_name TEXT NOT NULL UNIQUE
)
""")

cursor.execute("""
CREATE TABLE genres (
    genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
    genre_name TEXT NOT NULL UNIQUE
)
""")

cursor.execute("""
CREATE TABLE pubdates (
    pubdate_id INTEGER PRIMARY KEY AUTOINCREMENT,
    publication_date TEXT NOT NULL UNIQUE
)
""")

cursor.execute("""
CREATE TABLE comics (
    comic_id INTEGER PRIMARY KEY AUTOINCREMENT,
    comic_uri TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    comic_type_id INTEGER NOT NULL,
    country_id INTEGER NOT NULL,
    pubdate_id INTEGER,
    FOREIGN KEY (comic_type_id) REFERENCES comic_types(comic_type_id),
    FOREIGN KEY (country_id) REFERENCES countries(country_id),
    FOREIGN KEY (pubdate_id) REFERENCES pubdates(pubdate_id)
)
""")

cursor.execute("""
CREATE TABLE comic_authors (
    comic_id INTEGER NOT NULL,
    author_id INTEGER NOT NULL,
    PRIMARY KEY (comic_id, author_id),
    FOREIGN KEY (comic_id) REFERENCES comics(comic_id),
    FOREIGN KEY (author_id) REFERENCES authors(author_id)
)
""")

cursor.execute("""
CREATE TABLE comic_genres (
    comic_id INTEGER NOT NULL,
    genre_id INTEGER NOT NULL,
    PRIMARY KEY (comic_id, genre_id),
    FOREIGN KEY (comic_id) REFERENCES comics(comic_id),
    FOREIGN KEY (genre_id) REFERENCES genres(genre_id)
)
""")

dst_conn.commit()

# Read all data from the flat 'webcomics' table
df = pd.read_sql_query("SELECT * FROM webcomics", src_conn)

# Convert publication_date to consistent string format
df['publication_date'] = pd.to_datetime(df['publication_date'], errors='coerce').dt.strftime('%Y-%m-%dT00:00:00Z')

# Helper function to insert unique values into lookup tables and return their IDs
def upsert_lookup_table(conn, table, column, values):
    """
    Insert unique values into lookup table if not exists, and return a dict mapping value -> id.
    """
    # Map table names to their ID column names
    id_column_map = {
        'countries': 'country_id',
        'authors': 'author_id',
        'genres': 'genre_id',
        'comic_types': 'comic_type_id',
        'pubdates': 'pubdate_id',  
    }
    
    id_col = id_column_map.get(table)
    if not id_col:
        raise ValueError(f"ID column mapping not found for table '{table}'")

    cursor = conn.cursor()
    unique_values = pd.Series(values).dropna().unique()

    # Insert values that do not already exist
    for val in unique_values:
        cursor.execute(f"INSERT OR IGNORE INTO {table} ({column}) VALUES (?)", (val,))
    conn.commit()

    # Query back all ids using the mapped id_col
    cursor.execute(f"SELECT {column}, {id_col} FROM {table}")
    rows = cursor.fetchall()

    # Return dictionary {value: id}
    return {row[0]: row[1] for row in rows}


# Insert into lookup tables and get mapping dicts
type_map = upsert_lookup_table(dst_conn, 'comic_types', 'type_name', df['type'])
country_map = upsert_lookup_table(dst_conn, 'countries', 'country_name', df['origin_country'])
author_map = upsert_lookup_table(dst_conn, 'authors', 'author_name', df['author'])
genre_map = upsert_lookup_table(dst_conn, 'genres', 'genre_name', df['genre'])
pubdate_map = upsert_lookup_table(dst_conn, 'pubdates', 'publication_date', df['publication_date'])


# Map publication_date to pubdate_id for the entire DataFrame first
df['pubdate_id'] = df['publication_date'].map(pubdate_map)

# Prepare cursor for inserting comics and relations
cursor = dst_conn.cursor()

# We will keep track of comics inserted to avoid duplicates
comic_uri_to_id = {}

for _, row in df.iterrows():
    comic_uri = row['comic_uri']
    if pd.isna(comic_uri):
        continue  # skip if no URI
    
    # Skip if already inserted
    if comic_uri in comic_uri_to_id:
        comic_id = comic_uri_to_id[comic_uri]
    else:
        # Insert comic
        comic_type_id = type_map.get(row['type'])
        country_id = country_map.get(row['origin_country'])
        title = row['title']
        pubdate_id = row['pubdate_id'] if pd.notna(row['pubdate_id']) else None

        cursor.execute("""
            INSERT OR IGNORE INTO comics (comic_uri, title, comic_type_id, country_id, pubdate_id)
            VALUES (?, ?, ?, ?, ?)
        """, (comic_uri, title, comic_type_id, country_id, pubdate_id))
        
        # Get comic_id (last inserted row or select by comic_uri)
        cursor.execute("SELECT comic_id FROM comics WHERE comic_uri = ?", (comic_uri,))
        comic_id = cursor.fetchone()[0]
        comic_uri_to_id[comic_uri] = comic_id

    # Insert comic-author relationship if author is present
    if pd.notna(row['author']):
        author_id = author_map.get(row['author'])
        if author_id:
            cursor.execute("""
                INSERT OR IGNORE INTO comic_authors (comic_id, author_id)
                VALUES (?, ?)
            """, (comic_id, author_id))

    # Insert comic-genre relationship if genre is present
    if pd.notna(row['genre']):
        genre_id = genre_map.get(row['genre'])
        if genre_id:
            cursor.execute("""
                INSERT OR IGNORE INTO comic_genres (comic_id, genre_id)
                VALUES (?, ?)
            """, (comic_id, genre_id))

# Commit and close connections
dst_conn.commit()
src_conn.close()
dst_conn.close()

print(" Data successfully normalized and inserted into comics.sqlite!")

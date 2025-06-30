import sqlite3

conn = sqlite3.connect('comics.sqlite')
cur = conn.cursor()

# Join comic_genres to genres and count comics per genre
cur.execute('''
    SELECT genres.genre_name, COUNT(DISTINCT comic_genres.comic_id) AS comic_count
    FROM comic_genres
    JOIN genres ON comic_genres.genre_id = genres.genre_id
    GROUP BY genres.genre_id
    ORDER BY comic_count DESC
    LIMIT 100
''')

rows = cur.fetchall()

# Extract counts to compute normalization for font sizes
counts = [row[1] for row in rows]
highest = max(counts) if counts else 0
lowest = min(counts) if counts else 0

bigsize = 80
smallsize = 20

with open('genre_cloud.js', 'w', encoding='utf-8') as fhand:
    fhand.write("genres = [\n")
    first = True
    for genre_name, count in rows:
        if not first:
            fhand.write(",\n")
        first = False
        # Normalize size to range [smallsize, bigsize]
        if highest == lowest:
            size = (bigsize + smallsize) // 2  # avoid division by zero
        else:
            size = int(((count - lowest) / (highest - lowest)) * bigsize + smallsize)
        fhand.write(f"{{text: '{genre_name}', size: {size}}}")
    fhand.write("\n];\n")
    fhand.close()

print("Output written to genre_cloud.js")
print("Open genre_cloud.html in a browser to see the visualization")

import sqlite3
import pandas as pd

# Connect to the normalized database
conn = sqlite3.connect('comics.sqlite')

# Query comics with publication dates
query = """
SELECT pd.publication_date
FROM comics c
JOIN pubdates pd ON c.pubdate_id = pd.pubdate_id
WHERE pd.publication_date IS NOT NULL
"""

df = pd.read_sql_query(query, conn)

# Convert to datetime and extract 'YYYY-MM'
df['month'] = pd.to_datetime(df['publication_date'], errors='coerce').dt.to_period('M').astype(str)

# Count comics per month
counts = df['month'].value_counts().sort_index()

# Write to comics_line.js
with open("comics_line.js", "w") as f:
    f.write("comics_line = [ ['Month', 'Comics']\n")
    for month, count in counts.items():
        f.write(f",['{month}', {count}]\n")
    f.write("];\n")

print(" comics_line.js written.")

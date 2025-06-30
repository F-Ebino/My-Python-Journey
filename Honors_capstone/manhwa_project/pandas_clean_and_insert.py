import pandas as pd
import sqlite3

# 1. Load the CSV into a pandas DataFrame
df = pd.read_csv("manhwa_manhua.csv")
print("Original columns:")
print(df.columns.tolist())  # Show original column names

# 2. Rename columns for clarity and SQLite compatibility
df = df.rename(columns={
    "comic": "comic_uri",                 # Internal Wikidata URI (optional to keep)
    "comicLabel": "title",                # Comic title
    "comicTypeLabel": "type",             # Either "manhwa" or "manhua"
    "authorLabel": "author",              # Author's name
    "countryLabel": "origin_country",     # Country of origin
    "genreLabel": "genre",                # Genre of the work
    "pubDate": "publication_date"         # Date published
})

print("Renamed columns:")
print(df.columns.tolist())

# 3. Drop exact duplicate rows
df = df.drop_duplicates()

# 4. Clean string data (strip whitespace)
df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)

# 5. Drop rows missing essential info (like title or country)
df = df.dropna(subset=["title", "origin_country"])

# 6. Connect to SQLite database (creates the file if it doesn't exist)
conn = sqlite3.connect("manhwa_manhua.sqlite")

# 7. Write the cleaned DataFrame to a new SQL table
df.to_sql("webcomics", conn, if_exists="replace", index=False)

# 8. Close the database connection
conn.close()

print(" Data cleaned and saved to manhwa_manhua.sqlite successfully.")

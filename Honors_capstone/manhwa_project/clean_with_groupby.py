import pandas as pd

# Load CSV exported from your SPARQL query
df = pd.read_csv('manhwa_manhua.csv')

# Optional: inspect columns to decide if renaming needed
print("Original columns:", df.columns.tolist())

# Rename columns for sqlite-friendly format (lowercase, no spaces)
df = df.rename(columns={
    "comic": "comic_uri",                 # Internal Wikidata URI (optional to keep)
    "comicLabel": "title",                # Comic title
    "comicTypeLabel": "type",             # Either "manhwa" or "manhua"
    "authorLabel": "author",              # Author's name
    "countryLabel": "origin_country",     # Country of origin
    "genreLabel": "genre",                # Genre of the work
    "pubDate": "publication_date"         # Date published
})
print(df.columns.tolist())
#quit()
# Drop duplicate rows if any
df = df.drop_duplicates()

# Combine multiple genres per comic into one comma-separated string
df_cleaned = df.groupby(
    ['comic_uri', 'type', 'title', 'author', 'origin_country', 'publication_date'],
    dropna=False  # keep rows even if some columns are NaN
)['genre'].apply(lambda x: ', '.join(sorted(set(x.dropna())))).reset_index()

#df_cleaned = df.groupby(
#    ['comic_uri', 'type', 'title', 'author', 'origin_country'],
#    dropna=False
#).agg({
#    'genre': lambda x: ', '.join(sorted(set(x.dropna()))),
#    'publication_date': lambda x: ', '.join(sorted(set(x.dropna().astype(str))))
#}).reset_index()



# Show the cleaned DataFrame structure
print(df_cleaned.head())

# Save cleaned data to a new CSV (optional)
df_cleaned.to_csv('cleaned_comics.csv', index=False)

# Insert into SQLite database example:
import sqlite3

#conn = sqlite3.connect('')
#df_cleaned.to_sql('comics', conn, if_exists='replace', index=False)
#conn.close()

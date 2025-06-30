import requests
from bs4 import BeautifulSoup

# Target URL
url = "https://asuracomic.net"

# Make the request
headers = {
    "User-Agent": "Mozilla/5.0"
}
response = requests.get(url, headers=headers)

# Check if successful
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find all comic cards
    comic_blocks = soup.select("div[class*='hover:cursor-pointer']")

    for comic in comic_blocks:
        title_tag = comic.select_one("span.block")
        genre_tag = comic.select_one("div.absolute span")

        title = title_tag.text.strip() if title_tag else "No Title"
        genre = genre_tag.text.strip() if genre_tag else "No Genre"

        print(f"Title: {title}")
        print(f"Genre: {genre}")
        print("-" * 40)
else:
    print("Failed to fetch the page. Status code:", response.status_code)

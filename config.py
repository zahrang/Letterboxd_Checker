USERNAME = #Use custom username

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://letterboxd.com/",
}

# SerpApi for Google "Available On" results
SERPAPI_KEY = #Use custom key

# ALL the streaming services to check against
MY_SERVICES = [
    "Netflix",
    "Amazon Prime Video", 
    "Disney Plus",
    "HBO Max",
    "Apple TV Plus",
    "BBC iPlayer",      # Free with TV Licence
    "ITVX",             # Free with ads
    "Channel 4",        # Free with ads
    "Channel 5",        # Free with ads
]

REGION = "GB"

DATA_FILE = "data/watchlist.json"
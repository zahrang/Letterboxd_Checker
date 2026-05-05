USERNAME = "occhiolizm"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://letterboxd.com/",
}

# TMDb API (keep as fallback, not currently used)
TMDB_API_KEY = "4b926dadd0ddd32ec3fedb8491dcd4b6"

# SerpApi for Google "Available On" results
SERPAPI_KEY = "2628f532c568be658f64e686c2e800cc9b54ac037933202d4c43f6c806506088"  # Get from https://serpapi.com/

# ALL the streaming services you subscribe to or have access to
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

REGION = "GB"  # UK region for Google searches

DATA_FILE = "data/watchlist.json"
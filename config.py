"""User settings. Command-line flags (see `python main.py --help`) override these."""

import os

# Your Letterboxd username (watchlist must be public). Override with --username.
USERNAME = "your_letterboxd_username"

# Two-letter country code used for streaming availability. Override with --region.
REGION = "GB"

# Where availability data comes from: "serpapi" (Google "Available on" panel,
# 100 free searches/month) or "tmdb" (TMDB / JustWatch data, free, no monthly cap).
BACKEND = "serpapi"

# API keys are read from environment variables so they never end up in git.
SERPAPI_KEY = os.environ.get("SERPAPI_KEY")
TMDB_API_KEY = os.environ.get("TMDB_API_KEY")

# The streaming services you subscribe to. Names must match the right-hand
# side of SERVICE_ALIASES in services.py.
MY_SERVICES = [
    "Netflix",
    "Amazon Prime Video",
    "Disney Plus",
    "HBO Max",
    "Apple TV Plus",
    "BBC iPlayer",
]

# A cached result is trusted for this many days before the film is looked up
# again. Higher = fewer API calls; lower = fresher results.
CACHE_DAYS = 14

DATA_DIR = "data"
WATCHLIST_FILE = os.path.join(DATA_DIR, "watchlist.json")  # last run's watchlist
CACHE_FILE = os.path.join(DATA_DIR, "cache.json")          # per-film results

REQUEST_TIMEOUT = 10  # seconds, for every HTTP request

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://letterboxd.com/",
}

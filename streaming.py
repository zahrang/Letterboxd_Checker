import requests
import time
from config import TMDB_API_KEY, REGION, MY_SERVICES

SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
PROVIDERS_URL = "https://api.themoviedb.org/3/movie/{movie_id}/watch/providers"

cache = {}
request_count = 0
last_request_time = 0

# Service name mapping
SERVICE_MAPPING = {
    "Netflix": "Netflix",
    "Netflix basic with ads": "Netflix",
    "Amazon Prime Video": "Amazon Prime Video",
    "Amazon Video": "Amazon Prime Video",
    "Prime Video": "Amazon Prime Video",
    "Disney+": "Disney Plus",
    "Disney Plus": "Disney Plus",
    "HBO Max": "HBO Max",
    "Max": "HBO Max",
    "Apple TV Plus": "Apple TV Plus",
    "Apple TV+": "Apple TV Plus",
    "BBC iPlayer": "BBC iPlayer",
    "ITVX": "ITVX",
    "Channel 4": "Channel 4",
    "Now TV": "Now TV",
    "Sky Go": "Sky Go",
}

def rate_limit():
    """Ensure we don't exceed TMDB rate limits (50 requests per second max)"""
    global last_request_time
    current_time = time.time()
    time_since_last = current_time - last_request_time
    if time_since_last < 0.1:  # Max 10 requests per second to be safe
        time.sleep(0.1 - time_since_last)
    last_request_time = time.time()

def search_movie(title):
    """Search for a movie by title and return its TMDB ID"""
    clean_title = title.split(' (')[0] if ' (' in title else title
    
    params = {
        "api_key": TMDB_API_KEY,
        "query": clean_title
    }

    try:
        rate_limit()
        response = requests.get(SEARCH_URL, params=params, timeout=10)
        
        if response.status_code == 429:  # Rate limited
            print("  Rate limited, waiting 1 second...")
            time.sleep(1)
            return search_movie(title)  # Retry
            
        if response.status_code != 200:
            return None

        results = response.json().get("results", [])
        if not results:
            return None

        return results[0]["id"]
    except Exception as e:
        return None


def get_providers(movie_id):
    """Get streaming providers for a movie in the specified region"""
    url = PROVIDERS_URL.format(movie_id=movie_id)
    params = {"api_key": TMDB_API_KEY}

    try:
        rate_limit()
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code != 200:
            return []

        results = response.json().get("results", {})
        region_data = results.get(REGION)

        if not region_data:
            return []

        # Only get flatrate (subscription) providers
        providers = region_data.get("flatrate", [])
        
        return [p["provider_name"] for p in providers]
    except Exception as e:
        return []


def get_streaming_services(title):
    """Get matching streaming services for a film title"""
    if title in cache:
        return cache[title]

    movie_id = search_movie(title)
    if not movie_id:
        cache[title] = []
        return []

    providers = get_providers(movie_id)
    
    # Map TMDB provider names to your services
    matched_services = []
    for provider in providers:
        if provider in SERVICE_MAPPING:
            service = SERVICE_MAPPING[provider]
            if service not in matched_services and service in MY_SERVICES:
                matched_services.append(service)
    
    cache[title] = matched_services
    return matched_services


def test_api():
    """Test if the TMDB API is working correctly"""
    print(f"\nTesting TMDB API (Region: {REGION})")
    print("=" * 50)
    
    test_films = [
        "The Silence of the Lambs",
        "Arrival", 
        "Inception"
    ]
    
    for film in test_films:
        print(f"\nChecking: {film}")
        movie_id = search_movie(film)
        if movie_id:
            print(f"Found movie ID: {movie_id}")
            providers = get_providers(movie_id)
            if providers:
                print(f"Subscription providers: {providers}")
                matched = get_streaming_services(film)
                if matched:
                    print(f"Matched your services: {matched}")
                else:
                    print(f"No match with your services: {MY_SERVICES}")
            else:
                print(f"No subscription providers in {REGION}")
        else:
            print(f"Movie not found")
        time.sleep(0.2)  # Small delay between tests


if __name__ == "__main__":
    test_api()
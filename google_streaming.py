from serpapi import GoogleSearch
import time
from config import SERPAPI_KEY, REGION, MY_SERVICES

# Cache to avoid repeated API calls
cache = {}

# Complete service mapping for ALL services you want to track
SERVICE_MAPPING = {
    # Netflix
    "Netflix": "Netflix",
    
    # Amazon Prime
    "Amazon Prime Video": "Amazon Prime Video",
    "Prime Video": "Amazon Prime Video",
    
    # Disney Plus
    "Disney+": "Disney Plus",
    "Disney Plus": "Disney Plus",
    
    # HBO Max
    "HBO Max": "HBO Max",
    "Max": "HBO Max",
    
    # Apple TV Plus
    "Apple TV+": "Apple TV Plus",
    "Apple TV Plus": "Apple TV Plus",
    
    # BBC iPlayer
    "BBC iPlayer": "BBC iPlayer",
    "BBC": "BBC iPlayer",
    
    # Additional services (UK free with ads)
    "ITVX": "ITVX",
    "ITV Hub": "ITVX",
    "Channel 4": "Channel 4",
    "All 4": "Channel 4",
    "My5": "Channel 5",
    "Channel 5": "Channel 5",
}


def search_google_available_on(title):
    """Search Google for a film and return where it's available to stream"""
    if title in cache:
        return cache[title]
    
    search_query = f"{title} watch online"
    
    params = {
        "api_key": SERPAPI_KEY,
        "engine": "google",
        "q": search_query,
        "gl": REGION.lower(),
        "hl": "en",
    }
    
    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        
        available_on = results.get("available_on", [])
        
        matched_services = []
        for service in available_on:
            service_name = service.get("name", "")
            price = service.get("price", "").lower()
            
            # Special handling for Amazon Prime - skip add-ons
            if "prime" in service_name.lower() or "amazon" in service_name.lower():
                # Skip if this requires an add-on subscription
                if "add-on" in price:
                    continue
                # Only include if it's truly included with Prime
                elif "subscription" in price or "premium" in price:
                    if "Amazon Prime Video" in MY_SERVICES and "Amazon Prime Video" not in matched_services:
                        matched_services.append("Amazon Prime Video")
            
            # For all other services
            elif ("subscription" in price or "premium" in price) and service_name in SERVICE_MAPPING:
                matched_service = SERVICE_MAPPING[service_name]
                if matched_service in MY_SERVICES and matched_service not in matched_services:
                    matched_services.append(matched_service)
            
            # Special handling for free UK services (BBC iPlayer, ITVX, Channel 4)
            elif "free" in price and service_name in SERVICE_MAPPING:
                matched_service = SERVICE_MAPPING[service_name]
                if matched_service in MY_SERVICES and matched_service not in matched_services:
                    matched_services.append(matched_service)
        
        cache[title] = matched_services
        return matched_services
        
    except Exception as e:
        print(f"  Google search failed for {title}: {e}")
        return []


def get_streaming_services(title):
    """Get streaming services for a film (excluding add-on subscriptions)"""
    return search_google_available_on(title)


def test_google_api():
    """Test the Google API with some films"""
    test_films = [
        "The Prestige",
        "Blue Planet II",  # Should be on BBC iPlayer
        "Fleabag",  # Should be on BBC iPlayer/Amazon
    ]
    
    print(f"\n🔍 Testing Google Available On API (Region: {REGION.upper()})")
    print(f"Tracking services: {MY_SERVICES}")
    print("=" * 70)
    
    for film in test_films:
        print(f"\nChecking: {film}")
        services = get_streaming_services(film)
        if services:
            print(f"  ✓ Available on: {', '.join(services)}")
        else:
            print(f"  ✗ Not available on your services")
        time.sleep(1)


if __name__ == "__main__":
    test_google_api()
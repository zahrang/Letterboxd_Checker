"""SerpApi backend: reads the "Available on" panel from a Google search."""

import requests

from config import REQUEST_TIMEOUT
from services import BackendUnavailable, LookupFailed, canonical_service, split_title

SERPAPI_URL = "https://serpapi.com/search.json"
NO_RESULTS = "Google hasn't returned any results for this query."


def build_query(title):
    """'Rope (1948)' -> 'Rope 1948 film' (brackets dropped, year kept)."""
    name, year = split_title(title)
    return f"{name} {year} film" if year else f"{name} film"


def is_included(price):
    """True if a listing is part of a subscription or free, not a rental,
    purchase or paid add-on channel."""
    price = (price or "").lower()
    if "add-on" in price or "add on" in price:
        return False
    return "subscription" in price or "free" in price


def parse_available_on(available_on):
    """Turn SerpApi `available_on` entries into canonical service names,
    dropping add-ons, rentals and services we don't recognise."""
    services = []
    for entry in available_on or []:
        if not is_included(entry.get("price")):
            continue
        service = canonical_service(entry.get("name"))
        if service and service not in services:
            services.append(service)
    return services


def lookup(title, region, api_key):
    """Return every known service `title` is included on in `region`."""
    if not api_key:
        raise BackendUnavailable("SERPAPI_KEY environment variable is not set")

    params = {
        "api_key": api_key,
        "engine": "google",
        "q": build_query(title),
        "gl": region.lower(),
        "hl": "en",
    }
    try:
        response = requests.get(SERPAPI_URL, params=params, timeout=REQUEST_TIMEOUT)
    except requests.RequestException as e:
        raise LookupFailed(f"network error: {e}") from e

    try:
        data = response.json()
    except ValueError as e:
        raise LookupFailed(f"non-JSON response (HTTP {response.status_code})") from e

    error = data.get("error")
    if response.status_code in (401, 403):
        raise BackendUnavailable(f"SerpApi rejected the key: {error}")
    if response.status_code == 429:
        raise BackendUnavailable(f"SerpApi quota or rate limit hit: {error}")
    if error == NO_RESULTS:
        return []
    if error or response.status_code != 200:
        raise LookupFailed(f"SerpApi error (HTTP {response.status_code}): {error}")

    return parse_available_on(data.get("available_on"))

"""TMDB backend: watch-provider data (sourced from JustWatch). Free, no monthly cap."""

import requests

from config import REQUEST_TIMEOUT
from services import BackendUnavailable, LookupFailed, canonical_service, split_title

SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
PROVIDERS_URL = "https://api.themoviedb.org/3/movie/{movie_id}/watch/providers"

# Subscription, free and free-with-ads. Rent/buy are deliberately excluded.
INCLUDED_TYPES = ("flatrate", "free", "ads")


def _get(url, params):
    try:
        response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
    except requests.RequestException as e:
        raise LookupFailed(f"network error: {e}") from e
    if response.status_code == 401:
        raise BackendUnavailable("TMDB rejected the API key")
    if response.status_code != 200:
        raise LookupFailed(f"TMDB HTTP {response.status_code}")
    try:
        return response.json()
    except ValueError as e:
        raise LookupFailed("TMDB returned non-JSON") from e


def parse_providers(region_data):
    """Turn one region's TMDB provider block into canonical service names."""
    services = []
    for kind in INCLUDED_TYPES:
        for provider in (region_data or {}).get(kind, []):
            service = canonical_service(provider.get("provider_name"))
            if service and service not in services:
                services.append(service)
    return services


def lookup(title, region, api_key):
    """Return every known service `title` is included on in `region`."""
    if not api_key:
        raise BackendUnavailable("TMDB_API_KEY environment variable is not set")

    name, year = split_title(title)
    params = {"api_key": api_key, "query": name}
    if year:
        params["primary_release_year"] = year

    results = _get(SEARCH_URL, params).get("results", [])
    if not results:
        return []

    movie_id = results[0]["id"]
    providers = _get(PROVIDERS_URL.format(movie_id=movie_id), {"api_key": api_key})
    return parse_providers(providers.get("results", {}).get(region.upper()))

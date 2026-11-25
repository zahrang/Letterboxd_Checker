"""Scrapes a public Letterboxd watchlist (HTML pages, not RSS)."""

import html

import requests
from bs4 import BeautifulSoup

from config import HEADERS, REQUEST_TIMEOUT


class WatchlistError(Exception):
    """The watchlist couldn't be fetched."""


def parse_page(page_html):
    """Return the film titles on one watchlist page, e.g. 'Rope (1948)'."""
    soup = BeautifulSoup(page_html, "html.parser")
    films = []
    for component in soup.find_all("div", class_="react-component"):
        name = component.get("data-item-name")
        if name and component.get("data-component-class") in ("LazyPoster", None):
            films.append(html.unescape(name))
    has_next = bool(soup.select_one("div.pagination a.next"))
    return list(dict.fromkeys(films)), has_next


def fetch_watchlist(username, verbose=False):
    """Fetch every page of `username`'s watchlist. Raises WatchlistError."""
    films = []
    page = 1
    while True:
        url = f"https://letterboxd.com/{username}/watchlist/page/{page}/"
        if verbose:
            print(f"Fetching: {url}")
        try:
            response = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        except requests.RequestException as e:
            raise WatchlistError(f"network error fetching {url}: {e}") from e

        if response.status_code == 404 and page == 1:
            raise WatchlistError(f"Letterboxd user '{username}' not found")
        if response.status_code != 200:
            raise WatchlistError(f"Letterboxd returned HTTP {response.status_code} for {url}")

        page_films, has_next = parse_page(response.text)
        if verbose:
            print(f"Found {len(page_films)} films on page {page}")
        films.extend(page_films)

        if not page_films or not has_next:
            break
        page += 1

    if verbose:
        print(f"Total films found: {len(films)}")
    return list(dict.fromkeys(films))


if __name__ == "__main__":
    import sys
    from config import USERNAME
    fetch_watchlist(sys.argv[1] if len(sys.argv) > 1 else USERNAME, verbose=True)

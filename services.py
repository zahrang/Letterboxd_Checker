"""Shared helpers for turning provider names and film titles into a common form."""

import re

# Provider names as they appear in SerpApi / TMDB -> one canonical name.
# Add-on channels (e.g. "MUBI Amazon Channel") are deliberately absent, so
# they never match.
SERVICE_ALIASES = {
    "Netflix": "Netflix",
    "Netflix basic with Ads": "Netflix",
    "Netflix Standard with Ads": "Netflix",
    "Amazon Prime Video": "Amazon Prime Video",
    "Amazon Prime Video with Ads": "Amazon Prime Video",
    "Prime Video": "Amazon Prime Video",
    "Disney+": "Disney Plus",
    "Disney Plus": "Disney Plus",
    "HBO Max": "HBO Max",
    "Max": "HBO Max",
    "Apple TV+": "Apple TV Plus",
    "Apple TV Plus": "Apple TV Plus",
    "Apple TV": "Apple TV Plus",  # Apple renamed Apple TV+ to "Apple TV" in 2025
    "BBC iPlayer": "BBC iPlayer",
    "BBC": "BBC iPlayer",
    "ITVX": "ITVX",
    "ITV Hub": "ITVX",
    "Channel 4": "Channel 4",
    "All 4": "Channel 4",
    "My5": "Channel 5",
    "Channel 5": "Channel 5",
}

_LOWER_ALIASES = {k.lower(): v for k, v in SERVICE_ALIASES.items()}


def canonical_service(name):
    """Return the canonical service name, or None if it's not one we know."""
    return _LOWER_ALIASES.get((name or "").strip().lower())


def split_title(title):
    """'Rope (1948)' -> ('Rope', '1948'); 'Rope' -> ('Rope', None)."""
    match = re.match(r"^(.*?)\s*\((\d{4})\)\s*$", title)
    if match:
        return match.group(1), match.group(2)
    return title.strip(), None


class LookupFailed(Exception):
    """A single film couldn't be checked (network error, bad response...)."""


class BackendUnavailable(Exception):
    """The backend can't be used at all (bad key, quota used up). Stop the run."""

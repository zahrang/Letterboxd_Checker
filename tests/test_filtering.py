import json
from pathlib import Path

from serpapi_backend import build_query, is_included, parse_available_on
from services import canonical_service, split_title
from tmdb_backend import parse_providers

FIXTURES = Path(__file__).parent / "fixtures"


SAMPLES = json.loads((FIXTURES / "serpapi_samples.json").read_text(encoding="utf-8"))


def test_real_sample_keeps_subscription_drops_addon_and_rentals():
    # Netflix "Subscription" kept; NOW "Subscription (Requires add-on)" and rentals dropped.
    assert parse_available_on(SAMPLES["Arrival (2016)"]) == ["Netflix"]


def test_real_sample_prime_addon_is_not_counted_as_prime():
    # Prime Video lists it as "Subscription (Requires add-on)", i.e. a paid channel.
    assert parse_available_on(SAMPLES["The Silence of the Lambs (1991)"]) == []


def test_real_sample_rentals_only():
    assert parse_available_on(SAMPLES["Rope (1948)"]) == []


def test_price_rules():
    assert not is_included("Subscription (Requires add-on)")
    assert not is_included("From £3.99")
    assert not is_included("£3.49")
    assert is_included("Subscription")
    assert is_included("Premium subscription")
    assert is_included("Free")


def test_parse_handles_missing_panel():
    assert parse_available_on(None) == []


def test_tmdb_ignores_rent_and_buy():
    region = {
        "flatrate": [{"provider_name": "Netflix"}, {"provider_name": "MUBI Amazon Channel"}],
        "free": [{"provider_name": "BBC iPlayer"}],
        "rent": [{"provider_name": "Apple TV"}],
        "buy": [{"provider_name": "Amazon Video"}],
    }
    assert parse_providers(region) == ["Netflix", "BBC iPlayer"]


def test_split_title_and_query():
    assert split_title("Rope (1948)") == ("Rope", "1948")
    assert split_title("Avatar Aang: The Last Airbender (2026)") == ("Avatar Aang: The Last Airbender", "2026")
    assert split_title("Untitled") == ("Untitled", None)
    assert build_query("Rope (1948)") == "Rope 1948 film"


def test_canonical_service_is_case_insensitive():
    assert canonical_service("disney+") == "Disney Plus"
    assert canonical_service("Max") == "HBO Max"
    assert canonical_service("Nope") is None

from datetime import datetime, timedelta, timezone

from storage import Cache
from update import compare_watchlists


def test_compare_watchlists_preserves_order():
    old = ["A (2000)", "B (2001)", "C (2002)"]
    new = ["D (2003)", "A (2000)", "C (2002)", "E (2004)"]
    assert compare_watchlists(old, new) == (["D (2003)", "E (2004)"], ["B (2001)"])


def test_cache_expires_and_persists(tmp_path):
    path = str(tmp_path / "cache.json")
    t0 = datetime(2026, 1, 1, tzinfo=timezone.utc)

    cache = Cache(path, max_age_days=14)
    cache.put("serpapi", "gb", "Rope (1948)", ["Netflix"], now=t0)
    cache.save()

    reloaded = Cache(path, max_age_days=14)
    assert reloaded.get("serpapi", "GB", "Rope (1948)", now=t0 + timedelta(days=13)) == ["Netflix"]
    assert reloaded.get("serpapi", "GB", "Rope (1948)", now=t0 + timedelta(days=15)) is None
    # Different backend or region is a different entry.
    assert reloaded.get("tmdb", "GB", "Rope (1948)", now=t0) is None
    assert reloaded.get("serpapi", "US", "Rope (1948)", now=t0) is None


def test_cache_remembers_empty_results(tmp_path):
    cache = Cache(str(tmp_path / "c.json"), max_age_days=14)
    cache.put("serpapi", "GB", "Obscure (1999)", [])
    assert cache.get("serpapi", "GB", "Obscure (1999)") == []

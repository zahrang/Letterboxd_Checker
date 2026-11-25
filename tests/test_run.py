import main
from services import BackendUnavailable, LookupFailed
from storage import Cache


def test_check_films_uses_cache_and_stops_on_quota(tmp_path, monkeypatch):
    calls = []

    def fake_lookup(title, region, api_key):
        calls.append(title)
        if title == "Flaky (2001)":
            raise LookupFailed("timeout")
        if title == "Quota (2002)":
            raise BackendUnavailable("out of searches")
        return ["Netflix"]

    monkeypatch.setitem(main.BACKENDS, "fake", (fake_lookup, lambda: "key", "Fake", 0))
    cache = Cache(str(tmp_path / "cache.json"), max_age_days=14)
    cache.put("fake", "GB", "Cached (2000)", ["BBC iPlayer"])

    args = main.parse_args(["--backend", "serpapi", "--region", "GB"])
    args.backend = "fake"
    films = ["Cached (2000)", "New (2003)", "Flaky (2001)", "Quota (2002)", "After (2004)"]
    results, failed, api_calls, stop_reason = main.check_films(films, args, cache)

    assert calls == ["New (2003)", "Flaky (2001)", "Quota (2002)"]  # no call for cached or after the stop
    assert results == {"Cached (2000)": ["BBC iPlayer"], "New (2003)": ["Netflix"]}
    assert failed == ["Flaky (2001)", "Quota (2002)", "After (2004)"]
    assert stop_reason == "out of searches"
    assert cache.get("fake", "GB", "New (2003)") == ["Netflix"]
    assert cache.get("fake", "GB", "Flaky (2001)") is None  # failures aren't cached

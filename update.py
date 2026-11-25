def compare_watchlists(old, new):
    """Return (added, removed) between two watchlists, in watchlist order."""
    old_set, new_set = set(old), set(new)
    added = [film for film in new if film not in old_set]
    removed = [film for film in old if film not in new_set]
    return added, removed

def compare_watchlists(old, new):
    old_set = set(old)
    new_set = set(new)

    added = list(new_set - old_set)
    removed = list(old_set - new_set)

    return added, removed
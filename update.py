def compare_watchlists(old, new):
    """
    Compare old and new watchlists to find added and removed films.
    
    Args:
        old (list): Previous watchlist
        new (list): Current watchlist
    
    Returns:
        tuple: (added_films, removed_films)
    """
    old_set = set(old)
    new_set = set(new)
    
    added = list(new_set - old_set)
    removed = list(old_set - new_set)
    
    return added, removed
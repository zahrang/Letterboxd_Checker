"""Letterboxd Watchlist Checker: which watchlist films are on my streaming services?"""

import argparse
import time

from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.table import Table

import config
import serpapi_backend
import tmdb_backend
from scraper import WatchlistError, fetch_watchlist
from services import BackendUnavailable, LookupFailed
from storage import Cache, load_watchlist, save_watchlist
from update import compare_watchlists

BACKENDS = {
    "serpapi": (serpapi_backend.lookup, lambda: config.SERPAPI_KEY, "SerpApi (Google 'Available on')", 0.5),
    "tmdb": (tmdb_backend.lookup, lambda: config.TMDB_API_KEY, "TMDB watch providers", 0.1),
}

console = Console()


def parse_args(argv=None):
    p = argparse.ArgumentParser(description="Check which films on a Letterboxd watchlist are on your streaming services.")
    p.add_argument("--username", default=config.USERNAME, help="Letterboxd username (default: config.USERNAME)")
    p.add_argument("--region", default=config.REGION, help="two-letter country code, e.g. GB or US")
    p.add_argument("--backend", choices=BACKENDS, default=config.BACKEND, help="availability data source")
    p.add_argument("--refresh", action="store_true", help="ignore the cache and re-check every film")
    p.add_argument("--cache-days", type=int, default=config.CACHE_DAYS, help="how long a cached result stays valid")
    return p.parse_args(argv)


def _capped(films, colour, sign, limit=15):
    lines = [f"[{colour}]{sign} {film}[/{colour}]" for film in films[:limit]]
    if len(films) > limit:
        lines.append(f"[dim]  ...and {len(films) - limit} more[/dim]")
    return lines


def show_changes(previous, current):
    if previous is None:
        console.print("[dim]First run: saved your watchlist so future runs can show what changed.[/dim]\n")
        return
    added, removed = compare_watchlists(previous, current)
    if not added and not removed:
        console.print("[dim]No watchlist changes since last run.[/dim]\n")
        return
    lines = _capped(added, "green", "+") + _capped(removed, "red", "-")
    console.print(Panel(
        "\n".join(lines),
        title=f"Since last run: {len(added)} added, {len(removed)} removed",
        border_style="magenta",
    ))
    console.print()


def check_films(films, args, cache):
    """Look up each film, using the cache where fresh. Returns
    (results {title: services}, failed [titles], api_calls, stop_reason)."""
    lookup, get_key, _, delay = BACKENDS[args.backend]
    api_key = get_key()
    results, failed, api_calls, stop_reason = {}, [], 0, None

    with Progress(SpinnerColumn(), TextColumn("{task.description}"), BarColumn(),
                  TextColumn("{task.completed}/{task.total}"), console=console) as progress:
        task = progress.add_task("[green]Checking availability...", total=len(films))
        for title in films:
            cached = None if args.refresh else cache.get(args.backend, args.region, title)
            if cached is not None:
                results[title] = cached
            elif stop_reason:
                failed.append(title)
            else:
                try:
                    services = lookup(title, args.region, api_key)
                    api_calls += 1
                    cache.put(args.backend, args.region, title, services)
                    results[title] = services
                    time.sleep(delay)
                except LookupFailed as e:
                    api_calls += 1
                    failed.append(title)
                    progress.console.print(f"[yellow]  Couldn't check {title}: {e}[/yellow]")
                except BackendUnavailable as e:
                    stop_reason = str(e)
                    failed.append(title)
            progress.advance(task)

    return results, failed, api_calls, stop_reason


def show_results(results, args):
    mine = set(config.MY_SERVICES)
    available = [(t, [s for s in svcs if s in mine]) for t, svcs in results.items()]
    available = [(t, svcs) for t, svcs in available if svcs]

    if not available:
        if results:
            console.print("\n[yellow]None of the checked films are currently on your services.[/yellow]")
        return 0

    table = Table(title=f"Available in {args.region.upper()} on your streaming services", border_style="green")
    table.add_column("#", style="dim", width=4)
    table.add_column("Film", style="bold white")
    table.add_column("Services", style="cyan")
    for i, (title, services) in enumerate(available, 1):
        table.add_row(str(i), title, ", ".join(services))
    console.print()
    console.print(table)
    return len(available)


def main(argv=None):
    args = parse_args(argv)
    _, get_key, backend_label, _ = BACKENDS[args.backend]

    console.print(Panel.fit(
        f"[bold cyan]Letterboxd Watchlist Checker[/bold cyan]\n"
        f"[dim]{args.username} | {backend_label} | Region: {args.region.upper()}[/dim]",
        border_style="cyan",
    ))
    console.print()

    if not get_key():  # still worth running: cached results can be shown
        env = "SERPAPI_KEY" if args.backend == "serpapi" else "TMDB_API_KEY"
        console.print(f"[yellow]{env} isn't set, so only cached results can be shown. "
                      f"Set it first, e.g. PowerShell: $env:{env}=\"...\"  bash: export {env}=...[/yellow]\n")

    try:
        with console.status("[cyan]Fetching watchlist..."):
            watchlist = fetch_watchlist(args.username)
    except WatchlistError as e:
        console.print(f"[red]Couldn't fetch the watchlist: {e}[/red]")
        return 1
    if not watchlist:
        console.print("[yellow]That watchlist is empty (or private).[/yellow]")
        return 0

    watchlist_file = config.WATCHLIST_FILE
    previous = load_watchlist(watchlist_file)
    show_changes(previous, watchlist)
    save_watchlist(watchlist_file, watchlist)

    cache = Cache(config.CACHE_FILE, args.cache_days)
    try:
        results, failed, api_calls, stop_reason = check_films(watchlist, args, cache)
    finally:
        cache.save()  # keep whatever we paid for, even on Ctrl+C

    found = show_results(results, args)

    console.print()
    if stop_reason:
        console.print(f"[red]Stopped making lookups: {stop_reason}[/red]")
    if failed:
        console.print(f"[yellow]{len(failed)} film(s) couldn't be checked and will be retried next run.[/yellow]")
    console.print(Panel(
        f"[dim]Total: {len(watchlist)} films | Available: {found} | "
        f"API calls this run: {api_calls} | Region: {args.region.upper()}[/dim]",
        border_style="dim",
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

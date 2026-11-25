# Letterboxd Watchlist Checker

A command-line tool that reads your public Letterboxd watchlist and shows which films are included on the streaming services you actually subscribe to, ignoring rentals, purchases and paid add-on channels.

<!-- TODO: add a screenshot or GIF of a run here, e.g. ![demo](docs/demo.gif) -->

## Features

- **Change detection**: every run shows which films were added to or removed from your watchlist since the last run
- **Two availability backends**:
  - [SerpApi](https://serpapi.com/), which reads Google's "Available on" panel
  - [TMDB](https://www.themoviedb.org/), which uses JustWatch provider data, is free and has no monthly cap
- **Add-on filtering**: only counts films that come with the subscription itself (for example, Prime Video but not a "MUBI add-on")
- **Persistent cache**: results are saved to disk with a timestamp and reused for `CACHE_DAYS` (14 by default), so a normal run only looks up new films and stale entries
- **Fails gracefully**: network errors are counted and retried on the next run, and the run stops cleanly if the API quota runs out or the key is rejected

## Prerequisites

- Python 3.9+
- A [SerpApi](https://serpapi.com/) API key (free tier: 100 searches/month) **or** a [TMDB](https://www.themoviedb.org/settings/api) API key (free)

## Installation

```bash
git clone https://github.com/zahrang/Letterboxd_Checker.git
cd Letterboxd_Checker
pip install -r requirements.txt
```

## Configuration

API keys are read from environment variables, so they never end up in your code or in git:

```powershell
# PowerShell
$env:SERPAPI_KEY = "your_serpapi_key"
$env:TMDB_API_KEY = "your_tmdb_key"      # only needed for --backend tmdb
```

```bash
# bash / zsh
export SERPAPI_KEY="your_serpapi_key"
export TMDB_API_KEY="your_tmdb_key"
```

Then edit `config.py`:

```python
USERNAME = "your_letterboxd_username"
REGION = "GB"
BACKEND = "serpapi"        # or "tmdb"
MY_SERVICES = ["Netflix", "Amazon Prime Video", "BBC iPlayer", ...]
CACHE_DAYS = 14
```

## Usage

```bash
python main.py                                  # uses config.py
python main.py --username someone --region US   # override settings
python main.py --backend tmdb                   # use TMDB instead of SerpApi
python main.py --refresh                        # ignore the cache, re-check everything
python main.py --help
```

## How it works

1. Scrapes the HTML pages of your public Letterboxd watchlist (`letterboxd.com/<user>/watchlist/page/N/`).
2. Compares the result with the watchlist saved by the last run (`data/watchlist.json`) and prints what was added or removed.
3. For each film, uses the cached result (`data/cache.json`) if it's newer than `CACHE_DAYS`. Otherwise it asks the chosen backend.
4. Keeps only listings that are included with a subscription or free, maps provider names to a common form (`Disney+` → `Disney Plus`), and filters them to `MY_SERVICES`.
5. Prints a table of matches and a summary line showing how many API calls the run used.

## Example output

```
╭────────────────────────────────────────────────────╮
│ Letterboxd Watchlist Checker                       │
│ you | SerpApi (Google 'Available on') | Region: GB │
╰────────────────────────────────────────────────────╯

╭── Since last run: 2 added, 1 removed ──╮
│ + Maharaja (2024)                      │
│ + Billy Elliot (2000)                  │
│ - Novocaine (2025)                     │
╰────────────────────────────────────────╯

          Available in GB on your streaming services
┏━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┓
┃ #    ┃ Film                               ┃ Services     ┃
┡━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━┩
│ 1    │ Drive Me Crazy (1999)              │ Disney Plus  │
│ 2    │ Maharaja (2024)                    │ Netflix      │
│ ...  │ ...                                │ ...          │
└──────┴────────────────────────────────────┴──────────────┘

Total: 194 films | Available: 50 | API calls this run: 2 | Region: GB
```

## Design decisions

**Why SerpApi?** Google's "Available on" panel reflects what's actually included in each region, including UK free services such as BBC iPlayer and ITVX, and labels each listing with its price type. Google has no public API for it, so SerpApi provides it as structured JSON.

**Why also TMDB?** SerpApi's free tier allows 100 searches a month, while a typical watchlist has 150–200 films. TMDB's watch-provider data is free with no monthly cap, so it's a fallback you can switch to with `--backend tmdb`. Both backends return the same canonical service names, so the rest of the program doesn't depend on which one is used.

**Add-on filtering.** Prime Video lists channels like "MUBI add-on subscription" alongside included titles. A listing only counts if its price says it's included with a subscription or free, and anything mentioning an add-on is rejected. TMDB lists add-ons as separate "… Amazon Channel" providers, which aren't in the alias map, so they're dropped automatically.

**Caching strategy.** Looking up every film on every run would use up a month's SerpApi quota in one go. Instead:
- each result is stored on disk with a `checked_at` timestamp and treated as fresh for `CACHE_DAYS`;
- the cache stores *every* recognised service rather than only yours, so editing `MY_SERVICES` never forces a re-check;
- "not available anywhere" is cached too (it's a real answer), while failed lookups aren't, so they're retried next run;
- cache keys include the backend and region, so switching either doesn't mix up results;
- the cache is saved even if you press Ctrl+C mid-run, so lookups you've already paid for aren't lost.

Together with change detection, a typical run only looks up newly added films plus whatever has expired.

## Tests

```bash
pip install -r requirements-dev.txt
python -m pytest
```

The tests cover add-on and rental filtering (using real SerpApi responses saved in `tests/fixtures/`), title parsing, watchlist comparison and cache expiry. They don't make any network calls.

## Troubleshooting

**"SERPAPI_KEY isn't set"**: set the environment variable in the same terminal you run the script from (see Configuration).

**Quota used up**: the run stops making lookups, keeps everything already cached, and checks the remaining films next time. You can see your usage at [serpapi.com/dashboard](https://serpapi.com/dashboard), or switch with `--backend tmdb`.

**Letterboxd user not found**: check the username and make sure your watchlist is public.

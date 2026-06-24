# Letterboxd Watchlist Checker

A personalised command-line tool that searches through your Letterboxd watchlist and shows which films are available on your specific streaming services.

## Personalisation

Edit `config.py` with your custom API key and Letterboxd username in order to use.

## Features

- Reviews your Letterboxd watchlist for new additions and removals
- Checks streaming availability using Google's "Available On" API
- Filters out add-on subscriptions
- Shows exactly which of your subscribed services have each film
- Caches results to avoid repeated API calls

## Prerequisites

- Python 3.8+
- A [SerpApi](https://serpapi.com/) API key (free tier: 100 searches/month)

## Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/Letterboxd_Checker.git
cd Letterboxd_Checker

# Install dependencies
pip install -r requirements.txt
```

## Configuration

1. Get your SerpApi key from [serpapi.com](https://serpapi.com/)
2. Open `config.py` and add your credentials:

```python
SERPAPI_KEY = "your_serpapi_key_here"
LETTERBOXD_USERNAME = "your_username"
```

3. Customise your streaming services in `config.py`

## How It Works

1. Fetches your Letterboxd watchlist via RSS feed
2. Queries SerpApi for streaming availability of each film
3. Filters results to only show your subscribed services
4. Caches results for 24 hours to minimise API usage
5. Displays results in a clean, formatted table

## Example Output

```bash
╭───────────────────────────────────────────────────────────────────────────────────────────────────╮
│ Letterboxd Watchlist Checker                                                                     │
│ Google Available On API | Region: GB                                                             │
╰───────────────────────────────────────────────────────────────────────────────────────────────────╯

Found 50 films available on your subscription services!

                          Available in GB on Your Streaming Services                          
┏━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ #    ┃ Film                                               ┃ Services                       ┃
┡━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 1    │ Drive Me Crazy (1999)                              │ Disney Plus                    │
│ 2    │ Maharaja (2024)                                    │ Netflix                        │
│ 3    │ He's Just Not That Into You (2009)                 │ Netflix                        │
│ ...  │ ...                                                │ ...                            │
│ 50   │ Labyrinth (1986)                                   │ ITVX                           │
└──────┴────────────────────────────────────────────────────┴────────────────────────────────┘

Total: 172 films | Available: 50 | Region: GB
```

## Troubleshooting

### Common Issues

**API Key Errors**
- Ensure your SerpApi key is correctly set in `config.py`
- Check your API usage at [serpapi.com/dashboard](https://serpapi.com/dashboard)

**Rate Limiting**
- The free tier allows 100 searches/month
- The cache system reduces duplicate searches
- Increase cache duration in `config.py` if needed

**Letterboxd Username Not Found**
- Verify your Letterboxd username (case-sensitive)
- Ensure your watchlist is public

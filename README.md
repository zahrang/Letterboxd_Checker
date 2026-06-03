# 🎬 Letterboxd Watchlist Checker

A personalised command-line tool that monitors your Letterboxd watchlist and shows which films are available on your specific streaming services.

## Personalisation:
- Edit config.py with your custom API key and Letterboxd username in order to use.

## ✨ Features

- Monitors your Letterboxd watchlist for new additions and removals
- Checks streaming availability using Google's "Available On" API
- Filters out add-on subscriptions (e.g., Eros Now on Amazon Prime)
- Shows exactly which of your subscribed services have each film
- Beautiful terminal interface with tables, colours, and progress bars
- Caches results to avoid repeated API calls

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- A [SerpApi](https://serpapi.com/) API key (free tier: 100 searches/month)

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/Letterboxd_Checker.git
cd Letterboard_Checker

# Install dependencies
pip install -r requirements.txt
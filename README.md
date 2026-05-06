# 🎬 Letterboxd Watchlist Checker

A personalised command-line tool that monitors your Letterboxd watchlist and shows which films are available on your specific streaming services.

## ⚠️ Important Personalisation Note

**This code is specifically tailored to my personal needs and configuration. It is not designed as a generic tool for public use.**

The following are **hardcoded** to my personal setup:
- My Letterboxd username
- My streaming service subscriptions (Netflix, Disney+, Amazon Prime Video, etc.)
- My region: United Kingdom (GB)

If you wish to use this code, you will need to **modify multiple files** to replace my personal configurations with your own.

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
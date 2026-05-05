import requests
from bs4 import BeautifulSoup
from config import USERNAME, HEADERS


def fetch_watchlist_silent():
    """Fetch watchlist without printing any output"""
    films = []
    page = 1
    
    while True:
        url = f"https://letterboxd.com/{USERNAME}/watchlist/page/{page}/"
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code != 200:
            break
        
        soup = BeautifulSoup(response.text, "html.parser")
        page_films = []
        
        # Extract from React component data attributes
        react_components = soup.find_all('div', class_='react-component')
        
        for component in react_components:
            if component.get('data-component-class') == 'LazyPoster':
                film_name = component.get('data-item-name')
                if film_name:
                    film_name = film_name.replace('&#039;', "'")
                    page_films.append(film_name)
        
        # Backup method for any missed films
        if not page_films:
            grid_items = soup.find_all('li', class_='griditem')
            for item in grid_items:
                react_comp = item.find('div', class_='react-component')
                if react_comp and react_comp.get('data-item-name'):
                    film_name = react_comp.get('data-item-name')
                    film_name = film_name.replace('&#039;', "'")
                    page_films.append(film_name)
        
        # Remove duplicates
        page_films = list(dict.fromkeys(page_films))
        
        if not page_films:
            break
        
        films.extend(page_films)
        
        # Check if there's a next page
        pagination = soup.find('div', class_='pagination')
        if pagination:
            next_link = pagination.find('a', class_='next')
            if not next_link:
                break
        else:
            break
        
        page += 1
    
    return films


def fetch_watchlist():
    """Original function with print statements (kept for compatibility)"""
    films = []
    page = 1
    
    while True:
        url = f"https://letterboxd.com/{USERNAME}/watchlist/page/{page}/"
        print(f"Fetching: {url}")
        
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code != 200:
            print(f"Failed: Status {response.status_code}")
            break
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        page_films = []
        
        react_components = soup.find_all('div', class_='react-component')
        
        for component in react_components:
            if component.get('data-component-class') == 'LazyPoster':
                film_name = component.get('data-item-name')
                if film_name:
                    film_name = film_name.replace('&#039;', "'")
                    page_films.append(film_name)
        
        if not page_films:
            grid_items = soup.find_all('li', class_='griditem')
            for item in grid_items:
                react_comp = item.find('div', class_='react-component')
                if react_comp and react_comp.get('data-item-name'):
                    film_name = react_comp.get('data-item-name')
                    film_name = film_name.replace('&#039;', "'")
                    page_films.append(film_name)
        
        page_films = list(dict.fromkeys(page_films))
        
        print(f"Found {len(page_films)} films on page {page}")
        
        if not page_films:
            break
        
        if page == 1 and page_films:
            print(f"Sample films: {page_films[:3]}")
        
        films.extend(page_films)
        
        pagination = soup.find('div', class_='pagination')
        if pagination:
            next_link = pagination.find('a', class_='next')
            if not next_link:
                print(f"No more pages. Reached page {page}")
                break
        else:
            break
        
        page += 1
    
    print(f"\n✅ Total films found: {len(films)}")
    
    if films:
        print("\nFirst 20 films in your watchlist:")
        for i, film in enumerate(films[:20], 1):
            print(f"  {i}. {film}")
    
    return films
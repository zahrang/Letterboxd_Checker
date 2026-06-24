from streaming import get_streaming_services, test_api
from config import REGION

print(f"Testing with region: {REGION}")
print("=" * 50)

# Test a few specific films
test_films = [
    "The Silence of the Lambs (1991)",
    "Arrival (2016)",
    "Her (2013)",
    "The Prestige (2006)"
]

for film in test_films:
    print(f"\nChecking: {film}")
    services = get_streaming_services(film)
    if services:
        print(f"Available on: {', '.join(services)}")
    else:
        print(f"Not available")
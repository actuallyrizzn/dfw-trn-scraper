#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

url = 'http://localhost:5000'
print(f"Fetching {url} ...")
try:
    r = requests.get(url)
    r.raise_for_status()
    soup = BeautifulSoup(r.content, 'html.parser')
    print("\nLinks found on the index page:")
    for a in soup.find_all('a', href=True):
        print(f"  {a.get('href')} - {a.get_text(strip=True)[:60]}")
except Exception as e:
    print(f"Error: {e}") 
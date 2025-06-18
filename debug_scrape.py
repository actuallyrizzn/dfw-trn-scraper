import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)

def debug_attendee_page(url):
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    
    print(f"Fetching: {url}")
    response = session.get(url)
    print(f"Status: {response.status_code}")
    
    if response.status_code != 200:
        print(f"Error: {response.text[:500]}")
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Save the HTML for inspection
    with open('debug_page.html', 'w', encoding='utf-8') as f:
        f.write(response.text)
    print("Saved HTML to debug_page.html")
    
    # Look for attendee-related elements
    print("\n=== Looking for attendee elements ===")
    
    # Check for common attendee selectors
    selectors_to_try = [
        '.attendee',
        '.member',
        '.user',
        '.person',
        '.profile',
        '[class*="attendee"]',
        '[class*="member"]',
        '[class*="user"]',
        '[class*="person"]',
        'tr',  # Table rows
        'li',  # List items
        '.list-item',
        '.item'
    ]
    
    for selector in selectors_to_try:
        elements = soup.select(selector)
        if elements:
            print(f"Found {len(elements)} elements with selector '{selector}'")
            if len(elements) <= 5:  # Show first few
                for i, elem in enumerate(elements[:3]):
                    print(f"  {i+1}: {elem.get_text()[:100].strip()}")
    
    # Look for any text that might contain names
    print("\n=== Looking for potential names ===")
    text_content = soup.get_text()
    lines = [line.strip() for line in text_content.split('\n') if line.strip()]
    
    # Look for lines that might be names (2-3 words, no special chars)
    potential_names = []
    for line in lines:
        if len(line.split()) in [2, 3] and line.isalpha() and len(line) > 5:
            potential_names.append(line)
    
    print(f"Found {len(potential_names)} potential name lines:")
    for name in potential_names[:10]:
        print(f"  {name}")
    
    # Check for pagination
    print("\n=== Looking for pagination ===")
    pagination_selectors = [
        '.pagination',
        '.pager',
        '[class*="page"]',
        'a[href*="page"]'
    ]
    
    for selector in pagination_selectors:
        elements = soup.select(selector)
        if elements:
            print(f"Found pagination with selector '{selector}': {len(elements)} elements")
            for elem in elements[:3]:
                print(f"  {elem}")

if __name__ == "__main__":
    debug_attendee_page("https://www.dfwtrn.org/event-6176250/Attendees?elp=1") 
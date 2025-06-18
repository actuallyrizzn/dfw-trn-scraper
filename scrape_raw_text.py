#!/usr/bin/env python3
"""
DFWTRN Event Attendee Scraper - Module 1
Scrapes attendee lists from DFWTRN events and saves to raw text files.
"""

import requests
from bs4 import BeautifulSoup
import time
import argparse
import sys
from datetime import datetime
from urllib.parse import urljoin, urlparse, parse_qs
import csv
import os

class DFWTRNScraper:
    def __init__(self, delay=1):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.delay = delay
        
    def get_page(self, url):
        """Fetch a page and return BeautifulSoup object"""
        try:
            print(f"Fetching: {url}")
            response = self.session.get(url)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def analyze_page_structure(self, url):
        """Analyze the page structure to understand the layout"""
        soup = self.get_page(url)
        if not soup:
            return None
            
        print("\n=== PAGE STRUCTURE ANALYSIS ===")
        
        # Look for attendee table
        tables = soup.find_all('table')
        print(f"Found {len(tables)} tables on page")
        
        for i, table in enumerate(tables):
            print(f"\nTable {i+1}:")
            rows = table.find_all('tr')
            print(f"  Rows: {len(rows)}")
            
            if rows:
                # Show first few rows
                for j, row in enumerate(rows[:3]):
                    cells = row.find_all(['td', 'th'])
                    cell_text = [cell.get_text(strip=True) for cell in cells]
                    print(f"    Row {j+1}: {cell_text}")
        
        # Look for pagination
        pagination = soup.find_all('a', href=True)
        pagination_links = [a for a in pagination if 'elp=' in a.get('href', '')]
        print(f"\nPagination links found: {len(pagination_links)}")
        for link in pagination_links[:5]:  # Show first 5
            print(f"  {link.get('href')} - {link.get_text(strip=True)}")
        
        # Look for attendee-specific content
        attendee_content = soup.find_all(text=lambda text: text and ('Anonymous user' in text or any(name in text for name in ['Dowswell', 'Vachon', 'Trevizo'])))
        print(f"\nAttendee content found: {len(attendee_content)} instances")
        
        return soup
    
    def extract_attendees_from_page(self, soup):
        """Extract attendee data from a single page"""
        attendees = []
        
        # Look for the main content area
        tables = soup.find_all('table')
        
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 2:  # Expecting date and name columns
                    date_cell = cells[0].get_text(strip=True)
                    name_cell = cells[1].get_text(strip=True)
                    
                    # Skip header rows
                    if date_cell.lower() in ['date', 'registered'] or name_cell.lower() in ['name', 'attendee']:
                        continue
                    
                    # Skip empty rows
                    if not date_cell or not name_cell:
                        continue
                    
                    attendees.append({
                        'date': date_cell,
                        'name': name_cell
                    })
        
        return attendees
    
    def get_pagination_links(self, soup, base_url):
        """Extract all pagination links"""
        pagination_links = []
        
        # Look for pagination links
        links = soup.find_all('a', href=True)
        for link in links:
            href = link.get('href', '')
            if 'elp=' in href:
                full_url = urljoin(base_url, href)
                pagination_links.append(full_url)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_links = []
        for link in pagination_links:
            if link not in seen:
                seen.add(link)
                unique_links.append(link)
        
        return unique_links
    
    def scrape_event(self, event_url, output_format='txt'):
        """Main scraping function for an event"""
        print(f"Starting scrape of: {event_url}")
        
        # First, analyze the page structure
        soup = self.analyze_page_structure(event_url)
        if not soup:
            print("Failed to fetch initial page")
            return False
        
        # Extract event ID from URL
        parsed_url = urlparse(event_url)
        query_params = parse_qs(parsed_url.query)
        event_id = event_url.split('/')[-2] if '/' in event_url else 'unknown'
        
        # Generate timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Get all pagination links
        pagination_links = self.get_pagination_links(soup, event_url)
        if not pagination_links:
            pagination_links = [event_url]  # Single page
        
        print(f"Found {len(pagination_links)} pages to scrape")
        
        all_attendees = []
        
        # Scrape each page
        for i, page_url in enumerate(pagination_links):
            print(f"\nScraping page {i+1}/{len(pagination_links)}: {page_url}")
            
            page_soup = self.get_page(page_url)
            if page_soup:
                page_attendees = self.extract_attendees_from_page(page_soup)
                all_attendees.extend(page_attendees)
                print(f"  Found {len(page_attendees)} attendees on this page")
            
            # Respect delay between requests
            if i < len(pagination_links) - 1:  # Don't delay after last page
                time.sleep(self.delay)
        
        print(f"\nTotal attendees found: {len(all_attendees)}")
        
        # Save to file
        if output_format == 'txt':
            filename = f"raw_attendees_{event_id}_{timestamp}.txt"
            self.save_as_txt(all_attendees, filename)
        elif output_format == 'csv':
            filename = f"raw_attendees_{event_id}_{timestamp}.csv"
            self.save_as_csv(all_attendees, filename)
        
        return True
    
    def save_as_txt(self, attendees, filename):
        """Save attendees to text file"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"DFWTRN Event Attendees - Scraped on {datetime.now().isoformat()}\n")
            f.write("=" * 50 + "\n\n")
            
            for attendee in attendees:
                f.write(f"{attendee['date']}\t{attendee['name']}\n")
        
        print(f"Saved {len(attendees)} attendees to {filename}")
    
    def save_as_csv(self, attendees, filename):
        """Save attendees to CSV file"""
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Date', 'Name'])
            
            for attendee in attendees:
                writer.writerow([attendee['date'], attendee['name']])
        
        print(f"Saved {len(attendees)} attendees to {filename}")

def main():
    parser = argparse.ArgumentParser(description='Scrape DFWTRN event attendees')
    parser.add_argument('url', help='Event attendee URL to scrape')
    parser.add_argument('--delay', type=float, default=1.0, help='Delay between requests (seconds)')
    parser.add_argument('--format', choices=['txt', 'csv'], default='txt', help='Output format')
    parser.add_argument('--analyze-only', action='store_true', help='Only analyze page structure, don\'t scrape')
    
    args = parser.parse_args()
    
    scraper = DFWTRNScraper(delay=args.delay)
    
    if args.analyze_only:
        scraper.analyze_page_structure(args.url)
    else:
        success = scraper.scrape_event(args.url, args.format)
        if not success:
            sys.exit(1)

if __name__ == '__main__':
    main() 
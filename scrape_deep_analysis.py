#!/usr/bin/env python3
"""
DFWTRN Deep Analysis - Phase 1.5
Analyzes deeper attendee pages to understand full data structure for database design.
"""

import requests
from bs4 import BeautifulSoup
import time
import argparse
import sys
from datetime import datetime
from urllib.parse import urljoin, urlparse, parse_qs
import json
import os

class DFWTRNDeepAnalyzer:
    def __init__(self, delay=1):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.delay = delay
        self.attendee_details = []
        
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
    
    def extract_attendee_links(self, soup, base_url):
        """Extract all attendee profile links from the main attendee list"""
        attendee_links = []
        
        # Look for the main attendee table
        tables = soup.find_all('table')
        
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 2:
                    name_cell = cells[1]
                    
                    # Look for links in the name cell
                    links = name_cell.find_all('a', href=True)
                    for link in links:
                        href = link.get('href', '')
                        name_text = link.get_text(strip=True)
                        
                        # Skip if it's not an attendee link (avoid pagination links)
                        if href and 'elp=' not in href and name_text and name_text != 'Anonymous user':
                            full_url = urljoin(base_url, href)
                            attendee_links.append({
                                'name': name_text,
                                'url': full_url
                            })
        
        return attendee_links
    
    def analyze_attendee_profile(self, url, attendee_name):
        """Analyze a single attendee profile page"""
        soup = self.get_page(url)
        if not soup:
            return None
            
        print(f"\n=== ANALYZING PROFILE: {attendee_name} ===")
        
        profile_data = {
            'name': attendee_name,
            'profile_url': url,
            'tables': [],
            'forms': [],
            'links': [],
            'text_blocks': []
        }
        
        # Analyze all tables on the page
        tables = soup.find_all('table')
        print(f"Found {len(tables)} tables")
        
        for i, table in enumerate(tables):
            table_data = {
                'table_index': i,
                'rows': [],
                'headers': []
            }
            
            rows = table.find_all('tr')
            for j, row in enumerate(rows):
                cells = row.find_all(['td', 'th'])
                cell_data = []
                
                for cell in cells:
                    cell_text = cell.get_text(strip=True)
                    cell_links = [a.get('href') for a in cell.find_all('a', href=True)]
                    cell_data.append({
                        'text': cell_text,
                        'links': cell_links
                    })
                
                if j == 0:  # Assume first row is headers
                    table_data['headers'] = cell_data
                else:
                    table_data['rows'].append(cell_data)
            
            profile_data['tables'].append(table_data)
            
            # Show first few rows for analysis
            print(f"\nTable {i+1} - Headers: {[cell['text'] for cell in table_data['headers']]}")
            for k, row in enumerate(table_data['rows'][:3]):
                print(f"  Row {k+1}: {[cell['text'] for cell in row]}")
        
        # Look for forms (might contain editable data)
        forms = soup.find_all('form')
        print(f"\nFound {len(forms)} forms")
        for form in forms:
            form_data = {
                'action': form.get('action', ''),
                'method': form.get('method', ''),
                'inputs': []
            }
            
            inputs = form.find_all('input')
            for inp in inputs:
                form_data['inputs'].append({
                    'name': inp.get('name', ''),
                    'type': inp.get('type', ''),
                    'value': inp.get('value', '')
                })
            
            profile_data['forms'].append(form_data)
        
        # Look for specific data patterns
        text_content = soup.get_text()
        
        # Common profile fields to look for
        profile_fields = [
            'email', 'phone', 'company', 'title', 'position', 'address',
            'city', 'state', 'zip', 'member', 'since', 'joined', 'bio',
            'skills', 'experience', 'education', 'certifications'
        ]
        
        for field in profile_fields:
            if field.lower() in text_content.lower():
                print(f"  Found potential {field} data")
        
        return profile_data
    
    def get_pagination_links(self, soup, base_url):
        """Extract all pagination links from the attendee list page"""
        pagination_links = []
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

    def extract_all_attendee_links_across_pages(self, event_url):
        """Iterate through all pagination pages and collect attendee profile links from each. Print name cell HTML for last page."""
        all_links = []
        visited = set()
        # Fetch the first page
        soup = self.get_page(event_url)
        if not soup:
            return []
        # Get all pagination links (including the first page)
        pagination_links = self.get_pagination_links(soup, event_url)
        if event_url not in pagination_links:
            pagination_links.insert(0, event_url)
        print(f"\nFound {len(pagination_links)} pagination pages to scan for profile links.")
        for i, page_url in enumerate(pagination_links):
            if page_url in visited:
                continue
            visited.add(page_url)
            print(f"  Scanning page {i+1}/{len(pagination_links)}: {page_url}")
            page_soup = self.get_page(page_url)
            if not page_soup:
                continue
            # DEBUG: Print name cell HTML for the last page
            if i == len(pagination_links) - 1:
                print("\n--- DEBUG: Raw HTML of name cells on last page ---")
                tables = page_soup.find_all('table')
                for table in tables:
                    rows = table.find_all('tr')
                    for row in rows:
                        cells = row.find_all(['td', 'th'])
                        if len(cells) >= 2:
                            print(cells[1])
            page_links = self.extract_attendee_links(page_soup, page_url)
            print(f"    Found {len(page_links)} profile links on this page.")
            all_links.extend(page_links)
            time.sleep(self.delay)
        # Remove duplicates by profile URL
        seen_urls = set()
        unique_links = []
        for link in all_links:
            if link['url'] not in seen_urls:
                seen_urls.add(link['url'])
                unique_links.append(link)
        return unique_links

    def analyze_sample_profiles(self, event_url, max_profiles=5):
        """Analyze a sample of attendee profiles to understand data structure"""
        print(f"Starting deep analysis of: {event_url}")
        # Get all attendee profile links across all pages
        attendee_links = self.extract_all_attendee_links_across_pages(event_url)
        print(f"\nFound {len(attendee_links)} attendee profile links across all pages")
        # Show first few links
        for i, link_data in enumerate(attendee_links[:5]):
            print(f"  {i+1}. {link_data['name']} -> {link_data['url']}")
        # Analyze sample profiles
        sample_size = min(max_profiles, len(attendee_links))
        print(f"\nAnalyzing {sample_size} sample profiles...")
        for i, link_data in enumerate(attendee_links[:sample_size]):
            profile_data = self.analyze_attendee_profile(link_data['url'], link_data['name'])
            if profile_data:
                self.attendee_details.append(profile_data)
            if i < sample_size - 1:
                time.sleep(self.delay)
        # Save analysis results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"deep_analysis_{timestamp}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.attendee_details, f, indent=2, default=str)
        print(f"\nDeep analysis saved to {filename}")
        # Generate schema suggestions
        self.generate_schema_suggestions()
        return True
    
    def generate_schema_suggestions(self):
        """Generate database schema suggestions based on analyzed data"""
        print("\n=== DATABASE SCHEMA SUGGESTIONS ===")
        
        if not self.attendee_details:
            print("No profile data analyzed yet")
            return
        
        # Analyze common patterns across profiles
        all_fields = set()
        table_patterns = {}
        
        for profile in self.attendee_details:
            for table in profile['tables']:
                headers = [cell['text'] for cell in table['headers']]
                table_key = '|'.join(sorted(headers))
                
                if table_key not in table_patterns:
                    table_patterns[table_key] = {
                        'headers': headers,
                        'count': 0,
                        'sample_rows': []
                    }
                
                table_patterns[table_key]['count'] += 1
                
                # Store sample rows
                for row in table['rows'][:2]:  # First 2 rows as samples
                    table_patterns[table_key]['sample_rows'].append([cell['text'] for cell in row])
        
        print(f"\nFound {len(table_patterns)} distinct table patterns:")
        
        for pattern_key, pattern_data in table_patterns.items():
            print(f"\nPattern {pattern_data['count']} occurrences:")
            print(f"  Headers: {pattern_data['headers']}")
            print(f"  Sample rows:")
            for row in pattern_data['sample_rows'][:2]:
                print(f"    {row}")
        
        # Suggest schema
        print("\n=== SUGGESTED DATABASE SCHEMA ===")
        print("""
-- Main attendees table
CREATE TABLE attendees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER,
    event_date TEXT,
    full_name TEXT,
    first_name TEXT,
    last_name TEXT,
    profile_url TEXT,
    is_anonymous BOOLEAN DEFAULT FALSE,
    guest_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(event_id, full_name, event_date)
);

-- Profile details table (for linked profiles)
CREATE TABLE attendee_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    attendee_id INTEGER,
    profile_url TEXT UNIQUE,
    email TEXT,
    phone TEXT,
    company TEXT,
    job_title TEXT,
    bio TEXT,
    member_since TEXT,
    location TEXT,
    skills TEXT,
    certifications TEXT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (attendee_id) REFERENCES attendees(id)
);

-- Dynamic profile fields (for flexible data)
CREATE TABLE profile_fields (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id INTEGER,
    field_name TEXT,
    field_value TEXT,
    field_type TEXT,
    FOREIGN KEY (profile_id) REFERENCES attendee_profiles(id)
);

-- Events table
CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    event_name TEXT,
    event_date TEXT,
    event_url TEXT,
    total_attendees INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
        """)

def main():
    parser = argparse.ArgumentParser(description='Deep analysis of DFWTRN attendee profiles')
    parser.add_argument('url', help='Event attendee URL to analyze')
    parser.add_argument('--delay', type=float, default=1.0, help='Delay between requests (seconds)')
    parser.add_argument('--max-profiles', type=int, default=5, help='Maximum profiles to analyze')
    
    args = parser.parse_args()
    
    analyzer = DFWTRNDeepAnalyzer(delay=args.delay)
    success = analyzer.analyze_sample_profiles(args.url, args.max_profiles)
    
    if not success:
        sys.exit(1)

if __name__ == '__main__':
    main() 
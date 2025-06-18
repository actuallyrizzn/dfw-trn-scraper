#!/usr/bin/env python3
"""
DFWTRN Direct-to-DB Scraper
Scrapes attendee lists and deep profile data, inserting all discovered data directly into the SQLite database as it is scraped.
"""

import requests
from bs4 import BeautifulSoup
import time
import argparse
import sys
from datetime import datetime
from urllib.parse import urljoin, urlparse, parse_qs
import sqlite3
import re
import logging
import json
import concurrent.futures
import signal
import threading

DB_FILE = 'attendees.db'

# Global flag for graceful shutdown
shutdown_requested = False

def signal_handler(signum, frame):
    """Handle Ctrl+C gracefully"""
    global shutdown_requested
    logging.info("Shutdown requested. Finishing current tasks...")
    shutdown_requested = True

# --- DB SCHEMA ---
SCHEMA = '''
CREATE TABLE IF NOT EXISTS attendees (
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

CREATE TABLE IF NOT EXISTS attendee_profiles (
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

CREATE TABLE IF NOT EXISTS profile_fields (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id INTEGER,
    field_name TEXT,
    field_value TEXT,
    field_type TEXT,
    FOREIGN KEY (profile_id) REFERENCES attendee_profiles(id)
);

CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY,
    event_name TEXT,
    event_date TEXT,
    event_url TEXT,
    total_attendees INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
'''

# --- LOGGING ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

def extract_profile_data_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    profile_data = {}
    form_repeater = soup.find('div', id=lambda x: x and 'memberProfile_MemberForm' in x)
    if form_repeater:
        field_containers = form_repeater.find_all('div', class_='fieldContainer')
        for container in field_containers:
            label_span = container.find('span', id=lambda x: x and 'titleLabel' in x)
            if not label_span:
                continue
            label = label_span.get_text(strip=True)
            value_span = container.find('span', id=lambda x: x and ('TextBoxLabel' in x or 'DropDownLabel' in x))
            if not value_span:
                continue
            email_link = value_span.find('a', href=lambda x: x and x.startswith('mailto:'))
            if email_link:
                value = email_link.get('href').replace('mailto:', '')
            else:
                value = value_span.get_text(strip=True)
            if label and value:
                if 'first name' in label.lower():
                    profile_data['first_name'] = value
                elif 'last name' in label.lower():
                    profile_data['last_name'] = value
                elif 'company' in label.lower():
                    profile_data['company'] = value
                elif 'job function' in label.lower() or 'title' in label.lower():
                    profile_data['job_title'] = value
                elif 'work e-mail' in label.lower() or 'home e-mail' in label.lower():
                    if 'email' not in profile_data:
                        profile_data['email'] = value
                elif 'mobile phone' in label.lower() or 'phone' in label.lower():
                    profile_data['phone'] = value
                elif 'business type' in label.lower():
                    profile_data['business_type'] = value
                elif 'city' in label.lower():
                    profile_data['city'] = value
                else:
                    field_key = label.lower().replace(' ', '_').replace('*', '')
                    profile_data[field_key] = value
    membership_span = soup.find('span', id=lambda x: x and 'membershipDetails' in x)
    if membership_span:
        profile_data['membership_level'] = membership_span.get_text(strip=True)
    return profile_data

class DFWTRNDBScraper:
    def __init__(self, db_file=DB_FILE, delay=1.0):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.delay = delay
        # Set a longer timeout for SQLite to reduce 'database is locked' errors
        self.conn = sqlite3.connect(db_file, timeout=30.0, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.ensure_schema()

    def ensure_schema(self):
        with self.conn:
            self.conn.executescript(SCHEMA)

    def get_page(self, url):
        try:
            logging.info(f"Fetching: {url}")
            response = self.session.get(url)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            logging.error(f"Error fetching {url}: {e}")
            return None

    def get_pagination_links(self, soup, base_url):
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

    def extract_attendees_from_page(self, soup, base_url):
        attendees = []
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 2:
                    date_cell = cells[0].get_text(strip=True)
                    name_cell = cells[1].get_text(strip=True)
                    # Skip header rows
                    if date_cell.lower() in ['date', 'registered'] or name_cell.lower() in ['name', 'attendee']:
                        continue
                    if not date_cell or not name_cell:
                        continue
                    # Check for profile link
                    link_tag = cells[1].find('a', href=True)
                    profile_url = urljoin(base_url, link_tag['href']) if link_tag else None
                    is_anonymous = 'anonymous user' in name_cell.lower()
                    guest_count = 0
                    m = re.search(r'plus (\d+) guest', name_cell.lower())
                    if m:
                        guest_count = int(m.group(1))
                    # Parse name
                    full_name = name_cell.split('-')[0].strip()
                    if ',' in full_name:
                        last_name, first_name = [x.strip() for x in full_name.split(',', 1)]
                    elif ' ' in full_name:
                        first_name, last_name = full_name.split(' ', 1)
                    else:
                        first_name = full_name
                        last_name = ''
                    attendees.append({
                        'date': date_cell,
                        'name': full_name,
                        'first_name': first_name,
                        'last_name': last_name,
                        'profile_url': profile_url,
                        'is_anonymous': is_anonymous,
                        'guest_count': guest_count,
                        'raw_name': name_cell
                    })
        return attendees

    def extract_all_attendees(self, event_url):
        soup = self.get_page(event_url)
        if not soup:
            return []
        pagination_links = self.get_pagination_links(soup, event_url)
        if event_url not in pagination_links:
            pagination_links.insert(0, event_url)
        all_attendees = []
        for i, page_url in enumerate(pagination_links):
            logging.info(f"Scraping attendee page {i+1}/{len(pagination_links)}: {page_url}")
            page_soup = self.get_page(page_url)
            if not page_soup:
                continue
            attendees = self.extract_attendees_from_page(page_soup, page_url)
            logging.info(f"  Found {len(attendees)} attendees on this page.")
            all_attendees.extend(attendees)
            if i < len(pagination_links) - 1:
                time.sleep(self.delay)
        return all_attendees

    def extract_profile_data(self, profile_url):
        soup = self.get_page(profile_url)
        if not soup:
            return {}
        return extract_profile_data_from_html(str(soup))

    def _retry_db_write(self, func, *args, **kwargs):
        max_retries = 5
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except sqlite3.OperationalError as e:
                if 'database is locked' in str(e):
                    wait = 2 ** attempt
                    logging.warning(f"DB is locked, retrying in {wait}s (attempt {attempt+1}/{max_retries})...")
                    time.sleep(wait)
                else:
                    raise
        raise sqlite3.OperationalError("Max retries exceeded due to database lock.")

    def upsert_attendee(self, attendee, event_id):
        def do_write():
            # Ensure event_id is always available for error logging
            original_event_id = event_id
            try:
                # Check required fields
                if not attendee['date'] or not attendee['name']:
                    logging.error(f"Skipping attendee with missing required fields: {attendee}")
                    return None
                
                # Ensure all values are the correct type
                event_id = int(event_id)
                event_date = str(attendee['date']).strip()
                full_name = str(attendee['name']).strip()
                first_name = str(attendee['first_name']).strip() if attendee['first_name'] else ''
                last_name = str(attendee['last_name']).strip() if attendee['last_name'] else ''
                profile_url = str(attendee['profile_url']).strip() if attendee['profile_url'] else None
                is_anonymous = bool(attendee['is_anonymous'])
                guest_count = int(attendee['guest_count']) if attendee['guest_count'] else 0
                
                with self.conn:
                    cur = self.conn.execute('''
                        INSERT OR IGNORE INTO attendees (event_id, event_date, full_name, first_name, last_name, profile_url, is_anonymous, guest_count)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        event_id,
                        event_date,
                        full_name,
                        first_name,
                        last_name,
                        profile_url,
                        is_anonymous,
                        guest_count
                    ))
                    if cur.lastrowid:
                        attendee_id = cur.lastrowid
                    else:
                        # Try to find existing record
                        row = self.conn.execute('''
                            SELECT id FROM attendees WHERE event_id=? AND full_name=? AND event_date=?
                        ''', (event_id, full_name, event_date)).fetchone()
                        attendee_id = row['id'] if row else None
                    return attendee_id
            except sqlite3.IntegrityError as e:
                if 'UNIQUE constraint failed' in str(e):
                    logging.warning(f"Duplicate attendee skipped: {attendee['name']} for event {original_event_id}")
                    # Try to get existing attendee_id
                    try:
                        row = self.conn.execute('''
                            SELECT id FROM attendees WHERE event_id=? AND full_name=? AND event_date=?
                        ''', (original_event_id, str(attendee['name']).strip(), str(attendee['date']).strip())).fetchone()
                        return row['id'] if row else None
                    except:
                        return None
                else:
                    logging.error(f"Integrity error for attendee: {attendee} (event_id={original_event_id}): {e}")
                    return None
            except Exception as e:
                logging.error(f"DB insert error for attendee: {attendee} (event_id={original_event_id}): {e}")
                return None
        return self._retry_db_write(do_write)

    def upsert_profile(self, attendee_id, profile_url, profile_data):
        def do_write():
            try:
                if attendee_id is None:
                    logging.error(f"Skipping profile insert because attendee_id is None: profile_url={profile_url}")
                    return None
                
                # Ensure all values are the correct type
                attendee_id = int(attendee_id)
                profile_url = str(profile_url).strip()
                
                # Convert profile data values to strings
                email = str(profile_data.get('email', '')).strip() if profile_data.get('email') else None
                phone = str(profile_data.get('phone', '')).strip() if profile_data.get('phone') else None
                company = str(profile_data.get('company', '')).strip() if profile_data.get('company') else None
                job_title = str(profile_data.get('title') or profile_data.get('job_title', '')).strip() if (profile_data.get('title') or profile_data.get('job_title')) else None
                bio = str(profile_data.get('bio', '')).strip() if profile_data.get('bio') else None
                member_since = str(profile_data.get('member since') or profile_data.get('member_since', '')).strip() if (profile_data.get('member since') or profile_data.get('member_since')) else None
                location = str(profile_data.get('city') or profile_data.get('location', '')).strip() if (profile_data.get('city') or profile_data.get('location')) else None
                skills = str(profile_data.get('skills', '')).strip() if profile_data.get('skills') else None
                certifications = str(profile_data.get('certifications', '')).strip() if profile_data.get('certifications') else None
                
                with self.conn:
                    cur = self.conn.execute('''
                        INSERT OR IGNORE INTO attendee_profiles (attendee_id, profile_url, email, phone, company, job_title, bio, member_since, location, skills, certifications)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        attendee_id,
                        profile_url,
                        email,
                        phone,
                        company,
                        job_title,
                        bio,
                        member_since,
                        location,
                        skills,
                        certifications
                    ))
                    if cur.lastrowid:
                        profile_id = cur.lastrowid
                    else:
                        # Try to find existing record
                        row = self.conn.execute('''
                            SELECT id FROM attendee_profiles WHERE profile_url=?
                        ''', (profile_url,)).fetchone()
                        profile_id = row['id'] if row else None
                    
                    # Insert dynamic fields only if we have a valid profile_id
                    if profile_id:
                        for k, v in profile_data.items():
                            if k in ['email', 'phone', 'company', 'title', 'job_title', 'bio', 'member since', 'member_since', 'city', 'location', 'skills', 'certifications']:
                                continue
                            try:
                                field_name = str(k).strip()
                                field_value = str(v).strip() if v else ''
                                self.conn.execute('''
                                    INSERT OR IGNORE INTO profile_fields (profile_id, field_name, field_value, field_type)
                                    VALUES (?, ?, ?, ?)
                                ''', (profile_id, field_name, field_value, 'text'))
                            except Exception as field_error:
                                logging.warning(f"Failed to insert profile field {k}: {field_error}")
                    
                    return profile_id
            except sqlite3.IntegrityError as e:
                if 'UNIQUE constraint failed' in str(e):
                    logging.warning(f"Duplicate profile skipped: {profile_url}")
                    # Try to get existing profile_id
                    try:
                        row = self.conn.execute('''
                            SELECT id FROM attendee_profiles WHERE profile_url=?
                        ''', (profile_url,)).fetchone()
                        return row['id'] if row else None
                    except:
                        return None
                else:
                    logging.error(f"Integrity error for profile: attendee_id={attendee_id}, profile_url={profile_url}: {e}")
                    return None
            except Exception as e:
                logging.error(f"DB insert error for profile: attendee_id={attendee_id}, profile_url={profile_url}: {e}")
                return None
        return self._retry_db_write(do_write)

    def upsert_event(self, event_id, event_name, event_date, event_url, total_attendees):
        def do_write():
            with self.conn:
                self.conn.execute('''
                    INSERT OR IGNORE INTO events (id, event_name, event_date, event_url, total_attendees)
                    VALUES (?, ?, ?, ?, ?)
                ''', (event_id, event_name, event_date, event_url, total_attendees))
        return self._retry_db_write(do_write)

    def scrape_and_load(self, event_url):
        # Extract event_id from URL and ensure it's an integer
        parsed_url = urlparse(event_url)
        event_id_match = re.search(r'event-(\d+)', parsed_url.path)
        if not event_id_match:
            logging.error(f"Could not extract event ID from URL: {event_url}")
            return
        
        event_id = int(event_id_match.group(1))
        logging.info(f"Processing event {event_id}")
        
        # Get or create event record
        db = self.conn
        event = db.execute('SELECT * FROM events WHERE id = ?', (event_id,)).fetchone()
        if not event:
            # Try to get event name from the page
            event_name = f"Event {event_id}"
            db.execute('INSERT INTO events (id, event_name, event_url) VALUES (?, ?, ?)', 
                      (event_id, event_name, event_url))
            db.commit()
            logging.info(f"Created new event record: {event_name}")
        
        # Scrape attendees using the proper method
        attendees = self.extract_all_attendees(event_url)
        attendees_scraped = 0
        profiles_scraped = 0
        
        for attendee in attendees:
            try:
                # Insert attendee
                attendee_id = self.upsert_attendee(attendee, event_id)
                if attendee_id is not None:
                    attendees_scraped += 1
                    
                    # Extract profile data if profile link exists
                    if attendee.get('profile_url'):
                        profile_data = self.extract_profile_data(attendee['profile_url'])
                        if profile_data:
                            profile_id = self.upsert_profile(attendee_id, attendee['profile_url'], profile_data)
                            if profile_id is not None:
                                profiles_scraped += 1
                
            except Exception as e:
                logging.error(f"Error processing attendee {attendee.get('name', 'unknown')}: {e}")
                continue
        
        logging.info(f"Event {event_id} complete: {attendees_scraped} attendees, {profiles_scraped} profiles")
        return attendees_scraped, profiles_scraped

    def extract_all_event_links(self, events_url="https://www.dfwtrn.org/Events"):
        """Scrape the DFWTRN Events page and return a list of event URLs (attendee list pages)"""
        soup = self.get_page(events_url)
        if not soup:
            return []
        
        event_links = []
        event_ids = set()  # Use set to avoid duplicates
        
        # Find all event links (both absolute and relative)
        for a in soup.find_all('a', href=True):
            href = a.get('href', '')
            
            # Match event detail pages (both absolute and relative URLs)
            # Pattern: event-<digits> (with or without trailing slash)
            if re.match(r'.*event-\d+/?$', href):
                event_id_match = re.search(r'event-(\d+)', href)
                if event_id_match:
                    event_id = event_id_match.group(1)
                    if event_id not in event_ids:  # Avoid duplicates
                        event_ids.add(event_id)
                        attendee_url = f"https://www.dfwtrn.org/event-{event_id}/Attendees?elp=1"
                        event_links.append(attendee_url)
        
        logging.info(f"Found {len(event_links)} unique event attendee list URLs.")
        return event_links

    def scrape_all_events(self, events_url="https://www.dfwtrn.org/Events"):
        """Scrape all events listed on the DFWTRN Events page"""
        event_links = self.extract_all_event_links(events_url)
        for i, event_url in enumerate(event_links):
            logging.info(f"\n[{i+1}/{len(event_links)}] Scraping event: {event_url}")
            try:
                self.scrape_and_load(event_url)
            except Exception as e:
                logging.error(f"Error scraping {event_url}: {e}")
            time.sleep(self.delay * 2)

# --- CLI ---
def main():
    global shutdown_requested
    
    # Set up signal handling for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    parser = argparse.ArgumentParser(description="Scrape DFWTRN event attendees and load directly into SQLite DB")
    parser.add_argument('url', nargs='?', help='Event attendee URL to scrape, or "ALL" to scrape all events')
    parser.add_argument('--delay', type=float, default=1.0, help='Delay between requests (seconds)')
    parser.add_argument('--all', action='store_true', help='Scrape all events listed on the DFWTRN Events page')
    parser.add_argument('--workers', type=int, default=1, help='Number of parallel event workers (default: 1)')
    parser.add_argument('--limit', type=int, default=None, help='Limit the number of events to scrape (only with --all)')
    args = parser.parse_args()
    
    scraper = DFWTRNDBScraper(delay=args.delay)
    
    if args.all or (args.url and args.url.upper() == 'ALL'):
        event_links = scraper.extract_all_event_links()
        if args.limit is not None:
            event_links = event_links[:args.limit]
        logging.info(f"Scraping {len(event_links)} events...")
        
        if args.workers > 1:
            from concurrent.futures import ThreadPoolExecutor, as_completed
            with ThreadPoolExecutor(max_workers=args.workers) as executor:
                futures = {executor.submit(scraper.scrape_and_load, url): url for url in event_links}
                
                try:
                    for future in as_completed(futures):
                        if shutdown_requested:
                            logging.info("Shutdown requested. Cancelling remaining tasks...")
                            # Cancel all pending futures
                            for f in futures:
                                f.cancel()
                            break
                            
                        url = futures[future]
                        try:
                            attendees, profiles = future.result()
                            logging.info(f"{url}: {attendees} attendees, {profiles} profiles")
                        except Exception as e:
                            logging.error(f"Error scraping {url}: {e}")
                            
                except KeyboardInterrupt:
                    logging.info("Interrupted by user. Shutting down gracefully...")
                    # Cancel all pending futures
                    for f in futures:
                        f.cancel()
                    # Wait for running tasks to complete
                    executor.shutdown(wait=True)
                    logging.info("Shutdown complete.")
        else:
            for url in event_links:
                if shutdown_requested:
                    logging.info("Shutdown requested. Stopping...")
                    break
                try:
                    scraper.scrape_and_load(url)
                except KeyboardInterrupt:
                    logging.info("Interrupted by user. Stopping...")
                    break
    elif args.url:
        try:
            scraper.scrape_and_load(args.url)
        except KeyboardInterrupt:
            logging.info("Interrupted by user. Stopping...")
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 
# Debug Directory

This directory contains debug and development files for the DFWTRN scraper project.

## Files

- `debug_page.html` - Debug interface for testing HTML parsing and data extraction
- `debug_scrape.py` - Debug script for testing individual scraping functions
- `events_page.html` - Sample events page for debugging (currently empty)

## Purpose

These files are used for:
- **Development debugging** - Test individual components in isolation
- **HTML parsing** - Debug BeautifulSoup parsing logic
- **Data extraction** - Test extraction functions with sample data
- **Development workflow** - Quick testing without running full scraper

## Usage

```bash
# Run debug scraper
python debug/debug_scrape.py

# Open debug page in browser
# Open debug/debug_page.html in your web browser
```

## Note

These files are primarily for development and debugging purposes. They may not be needed for production use of the scraper. 
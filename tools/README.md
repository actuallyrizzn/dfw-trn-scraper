# Tools Directory

This directory contains utility scripts for database inspection, data validation, and debugging the DFWTRN scraper.

## Files

- `check_db.py` - Database inspection tool to view schema, record counts, and sample data
- `check_events.py` - Utility to check event data in the database
- `check_profile_data.py` - Tool to inspect attendee profile data
- `inspect_dashboard.py` - Utility for testing the Flask dashboard functionality

## Usage

```bash
# Check database structure and data
python tools/check_db.py

# Check events data
python tools/check_events.py

# Check profile data
python tools/check_profile_data.py

# Test dashboard
python tools/inspect_dashboard.py
```

## Purpose

These tools help with:
- **Database debugging** - Inspect data structure and content
- **Data validation** - Verify scraped data quality
- **Development** - Test individual components
- **Monitoring** - Check scraping progress and results 
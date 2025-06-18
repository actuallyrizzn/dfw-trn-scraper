# Tests Directory

This directory contains test files and test data for the DFWTRN scraper project.

## Files

- `test_profile_extraction.py` - Unit tests for profile data extraction functionality
- `test_event_detail_full.txt` - Sample event detail data for testing
- `test_events_full.txt` - Sample events list data for testing  
- `test_events.html` - Sample HTML page for testing event parsing

## Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_profile_extraction.py

# Run with verbose output
python -m pytest tests/ -v
```

## Test Data

The `.txt` and `.html` files contain sample data from the DFWTRN website that can be used for testing the scraper functionality without making actual HTTP requests. 
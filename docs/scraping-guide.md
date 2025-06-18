# Scraping Guide

This guide covers how to use the DFWTRN scraper to collect attendee data from events. The scraper is designed to be respectful, efficient, and reliable.

## 🎯 Overview

The scraper has three main components:
1. **`scrape_to_sql.py`** - Main scraper with database integration
2. **`scrape_raw_text.py`** - Raw text extraction (legacy)
3. **`scrape_deep_analysis.py`** - Deep profile analysis

## 🚀 Getting Started

### Basic Scraping

**Scrape a single event:**
```bash
python scrape_to_sql.py "https://www.dfwtrn.org/event-6176250/Attendees?elp=1"
```

**Scrape all events:**
```bash
python scrape_to_sql.py --all
```

**Scrape with limit (for testing):**
```bash
python scrape_to_sql.py --all --limit 5
```

## 📋 Command Line Options

### Main Options

| Option | Description | Default | Example |
|--------|-------------|---------|---------|
| `url` | Specific event URL to scrape | None | `"https://www.dfwtrn.org/event-6176250/Attendees?elp=1"` |
| `--all` | Scrape all events from the main events page | False | `--all` |
| `--limit` | Maximum number of events to scrape | No limit | `--limit 10` |
| `--delay` | Delay between requests (seconds) | 1.0 | `--delay 2.0` |
| `--workers` | Number of parallel workers | 1 | `--workers 3` |

### Advanced Options

| Option | Description | Default | Example |
|--------|-------------|---------|---------|
| `--max-profiles` | Maximum profiles to analyze per event | No limit | `--max-profiles 50` |
| `--verbose` | Enable verbose logging | False | `--verbose` |
| `--dry-run` | Test without saving to database | False | `--dry-run` |

## 🔧 Usage Examples

### Single Event Scraping

**Basic single event:**
```bash
python scrape_to_sql.py "https://www.dfwtrn.org/event-6176250/Attendees?elp=1"
```

**Single event with custom delay:**
```bash
python scrape_to_sql.py "https://www.dfwtrn.org/event-6176250/Attendees?elp=1" --delay 2.0
```

**Single event with profile limit:**
```bash
python scrape_to_sql.py "https://www.dfwtrn.org/event-6176250/Attendees?elp=1" --max-profiles 25
```

### Batch Scraping

**Scrape all events:**
```bash
python scrape_to_sql.py --all
```

**Scrape first 10 events:**
```bash
python scrape_to_sql.py --all --limit 10
```

**Scrape with multiple workers:**
```bash
python scrape_to_sql.py --all --workers 3 --limit 20
```

**Scrape with custom settings:**
```bash
python scrape_to_sql.py --all --delay 1.5 --workers 2 --limit 15 --max-profiles 30
```

### Testing and Development

**Dry run (no database writes):**
```bash
python scrape_to_sql.py --all --limit 2 --dry-run
```

**Verbose logging:**
```bash
python scrape_to_sql.py --all --limit 3 --verbose
```

**Test with single event:**
```bash
python scrape_to_sql.py "https://www.dfwtrn.org/event-6176250/Attendees?elp=1" --verbose
```

## 📊 Scraping Process

### 1. Event Discovery
When using `--all`, the scraper:
1. Fetches the main events page
2. Extracts all event URLs
3. Filters for attendee list pages
4. Processes events in order (newest first)

### 2. Attendee Extraction
For each event:
1. Fetches the attendee list page
2. Parses HTML tables for attendee data
3. Extracts names, dates, and profile links
4. Handles pagination automatically

### 3. Profile Analysis
For attendees with profile links:
1. Follows profile URLs
2. Extracts detailed information
3. Stores company, job title, contact info
4. Captures additional profile fields

### 4. Database Storage
All data is stored in SQLite:
- Events table for event metadata
- Attendees table for basic info
- Profiles table for detailed data
- Profile fields for dynamic data

## ⚡ Performance Optimization

### Multi-Worker Scraping
```bash
# Use 3 workers for faster scraping
python scrape_to_sql.py --all --workers 3 --limit 20
```

**Benefits:**
- Faster processing of multiple events
- Better resource utilization
- Reduced total scraping time

**Considerations:**
- Higher memory usage
- More concurrent requests
- May trigger rate limiting

### Optimal Settings by Use Case

**Quick Testing:**
```bash
python scrape_to_sql.py --all --limit 3 --workers 1 --delay 1.0
```

**Production Scraping:**
```bash
python scrape_to_sql.py --all --workers 3 --delay 1.5 --max-profiles 50
```

**Respectful Scraping:**
```bash
python scrape_to_sql.py --all --workers 1 --delay 2.0
```

**Fast Scraping:**
```bash
python scrape_to_sql.py --all --workers 4 --delay 0.5 --limit 50
```

## 🔍 Monitoring Progress

### Log Output
The scraper provides detailed logging:

```
2025-06-18 17:30:00 INFO: Starting DFWTRN scraper
2025-06-18 17:30:01 INFO: Found 127 events to process
2025-06-18 17:30:02 INFO: Processing event 6176250
2025-06-18 17:30:03 INFO: Found 45 attendees for event 6176250
2025-06-18 17:30:04 INFO: Processing profile: https://www.dfwtrn.org/Sys/PublicProfile/12345
2025-06-18 17:30:05 INFO: Completed event 6176250 (45 attendees, 12 profiles)
```

### Progress Indicators
- Event count and current event
- Attendee count per event
- Profile processing status
- Completion statistics

### Error Handling
- Network errors are retried automatically
- Invalid data is logged and skipped
- Database errors are handled gracefully
- Graceful shutdown on Ctrl+C

## 🛡️ Rate Limiting and Ethics

### Built-in Protections
- **Request Delays**: Configurable delay between requests
- **Exponential Backoff**: Automatic retry with increasing delays
- **Respectful Headers**: Proper User-Agent and headers
- **Error Handling**: Graceful handling of server responses

### Recommended Settings
```bash
# Conservative (most respectful)
python scrape_to_sql.py --all --delay 2.0 --workers 1

# Balanced (default)
python scrape_to_sql.py --all --delay 1.5 --workers 2

# Aggressive (use with caution)
python scrape_to_sql.py --all --delay 0.5 --workers 4
```

### Best Practices
1. **Start Small**: Test with `--limit 5` first
2. **Monitor Logs**: Watch for error messages
3. **Respect Delays**: Don't set delays below 0.5 seconds
4. **Use Workers Wisely**: More workers = more load
5. **Check Terms of Service**: Ensure scraping is allowed

## 🔧 Advanced Configuration

### Environment Variables
Create a `.env` file for persistent settings:

```bash
# Scraping configuration
SCRAPE_DELAY=1.5
MAX_WORKERS=3
MAX_PROFILES=50
LOG_LEVEL=INFO

# Database configuration
DB_FILE=attendees.db
DB_TIMEOUT=30

# Network configuration
REQUEST_TIMEOUT=30
MAX_RETRIES=3
```

### Custom Headers
The scraper uses respectful headers:
```
User-Agent: DFWTRN-Scraper/1.0 (+https://github.com/actuallyrizzn/dfw-trn-scraper)
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: keep-alive
```

## 📈 Data Quality

### What Gets Scraped
- **Basic Info**: Name, registration date, event
- **Profile Links**: URLs to detailed profiles
- **Deep Data**: Company, job title, contact info
- **Additional Fields**: Skills, certifications, bio

### Data Validation
- Names are parsed and normalized
- Dates are standardized
- URLs are validated
- Duplicate detection prevents re-insertion

### Quality Metrics
```bash
# Check data quality
python tools/check_db.py

# View profile completion rates
python tools/check_profile_data.py
```

## 🚨 Troubleshooting

### Common Issues

**1. "Connection timeout"**
```bash
# Increase timeout and retry
python scrape_to_sql.py --all --delay 2.0 --workers 1
```

**2. "Database is locked"**
```bash
# Wait for other processes to finish
# Or restart with single worker
python scrape_to_sql.py --all --workers 1
```

**3. "Rate limited"**
```bash
# Increase delay significantly
python scrape_to_sql.py --all --delay 5.0 --workers 1
```

**4. "Memory error"**
```bash
# Reduce workers and limit
python scrape_to_sql.py --all --workers 1 --limit 10
```

### Debug Mode
```bash
# Enable verbose logging
python scrape_to_sql.py --all --limit 2 --verbose

# Check specific event
python scrape_to_sql.py "URL" --verbose
```

## 📊 Output and Results

### Database Creation
- Database file: `attendees.db`
- Tables created automatically
- Data persists between runs
- Safe to re-run (no duplicates)

### Sample Output
```
2025-06-18 17:30:00 INFO: Starting DFWTRN scraper
2025-06-18 17:30:01 INFO: Found 127 events to process
2025-06-18 17:30:02 INFO: Processing event 6176250 (1/127)
2025-06-18 17:30:03 INFO: Found 45 attendees for event 6176250
2025-06-18 17:30:04 INFO: Processing 12 profiles for event 6176250
2025-06-18 17:30:05 INFO: Completed event 6176250 (45 attendees, 12 profiles)
2025-06-18 17:30:06 INFO: Processing event 6176249 (2/127)
...
2025-06-18 17:45:00 INFO: Scraping completed!
2025-06-18 17:45:01 INFO: Total: 127 events, 5,847 attendees, 892 profiles
```

### Verification
```bash
# Check results
python tools/check_db.py

# View recent events
python tools/check_events.py

# Check profile data
python tools/check_profile_data.py
```

## 🔄 Resuming Scraping

The scraper is **idempotent** - safe to re-run:

```bash
# Resume from where you left off
python scrape_to_sql.py --all

# Only new events will be processed
# Existing data is preserved
```

### Resume Scenarios
1. **Interrupted scraping**: Just re-run the command
2. **New events added**: Scraper will find and process them
3. **Partial data**: Missing data will be filled in
4. **Database corruption**: Delete `attendees.db` and start fresh

## 📞 Getting Help

### Debug Information
```bash
# Check scraper version and settings
python scrape_to_sql.py --help

# Test with single event
python scrape_to_sql.py "URL" --verbose

# Check database status
python tools/check_db.py
```

### Common Solutions
1. **Network issues**: Check internet connection
2. **Permission errors**: Ensure write access to directory
3. **Memory issues**: Reduce workers and limits
4. **Rate limiting**: Increase delays

---

*Next: [Dashboard Guide](dashboard-guide.md) or [CLI Reference](cli-reference.md)* 
# Quick Start Guide

Get the DFWTRN Scraper up and running in 5 minutes! This guide assumes you have Python 3.7+ installed.

## ⚡ 5-Minute Setup

### 1. Clone and Setup (1 minute)
```bash
# Clone the repository
git clone https://github.com/actuallyrizzn/dfw-trn-scraper.git
cd dfw-trn-scraper

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### 2. Test Scraping (2 minutes)
```bash
# Scrape a single event to test
python scrape_to_sql.py --all --limit 1

# Check the results
python tools/check_db.py
```

### 3. Launch Dashboard (1 minute)
```bash
# Start the web dashboard
python attendee_dashboard.py
```

### 4. View Results (1 minute)
- Open your browser to: `http://localhost:5000`
- You should see the dashboard with scraped data!

## 🎯 What You'll See

### Dashboard Overview
- **Statistics Cards**: Total attendees, events, profiles
- **Recent Events**: Latest scraped events
- **Quick Actions**: Search, export, navigation

### Sample Data
After scraping, you'll have:
- **Attendee Information**: Names, registration dates
- **Profile Data**: Company, job titles, contact info
- **Event Details**: Event metadata and statistics

## 🚀 Next Steps

### Scrape More Data
```bash
# Scrape all events (takes longer)
python scrape_to_sql.py --all

# Scrape with multiple workers (faster)
python scrape_to_sql.py --all --workers 3

# Scrape specific event
python scrape_to_sql.py "https://www.dfwtrn.org/event-6176250/Attendees?elp=1"
```

### Explore the Dashboard
- **Search Attendees**: Use the search bar to find specific people
- **View Events**: Click on event cards to see attendee lists
- **Export Data**: Download JSON files for analysis

### Check Data Quality
```bash
# View database statistics
python tools/check_db.py

# Check profile data
python tools/check_profile_data.py

# Inspect events
python tools/check_events.py
```

## 🔧 Common Commands

### Scraping Commands
```bash
# Basic scraping
python scrape_to_sql.py --all --limit 5

# Scraping with custom delay
python scrape_to_sql.py --all --delay 2.0

# Multi-worker scraping
python scrape_to_sql.py --all --workers 4 --limit 10
```

### Dashboard Commands
```bash
# Start dashboard
python attendee_dashboard.py

# Start with custom port
python attendee_dashboard.py --port 8080

# Start in debug mode
python attendee_dashboard.py --debug
```

### Utility Commands
```bash
# Check database
python tools/check_db.py

# Test dashboard
python tools/inspect_dashboard.py

# Run tests
python -m pytest tests/
```

## 📊 Understanding the Data

### What Gets Scraped
- **Basic Info**: Name, registration date, event
- **Profile Links**: URLs to detailed profiles
- **Deep Data**: Company, job title, contact info (when available)

### Data Structure
```
Events → Attendees → Profiles → Profile Fields
   ↓         ↓         ↓           ↓
Event ID  Name/Date  Company    Skills/Certs
```

### Sample Records
```json
{
  "event": {
    "id": 6176250,
    "name": "DFWTRN Monthly Meetup",
    "attendees": 45
  },
  "attendee": {
    "name": "John Smith",
    "date": "15 Jun 2025",
    "company": "Tech Corp",
    "job_title": "Software Engineer"
  }
}
```

## 🎨 Dashboard Features

### Overview Page (`/`)
- **Statistics**: Total counts and percentages
- **Recent Activity**: Latest scraped events
- **Quick Search**: Find attendees instantly

### Event Details (`/event/<id>`)
- **Attendee List**: Paginated table with profile links
- **Event Info**: Date, location, attendee count
- **Export Options**: Download event data

### Search Results (`/search?q=<query>`)
- **Fuzzy Matching**: Partial name searches
- **Cross-Event**: Find attendees across events
- **Profile Integration**: Show available profile data

## 🔍 Quick Tips

### Efficient Scraping
- Start with `--limit 5` to test
- Use `--workers 3` for faster scraping
- Set `--delay 1.5` to be respectful to servers

### Dashboard Usage
- Use the search bar for quick lookups
- Click profile links to see detailed info
- Export data for external analysis

### Data Management
- Database is automatically created
- Data is persistent between runs
- Safe to re-run scrapers (no duplicates)

## 🚨 Troubleshooting

### Common Issues
1. **"Module not found"**: Run `pip install -r requirements.txt`
2. **"Database locked"**: Wait for other processes to finish
3. **"Connection error"**: Check internet connection
4. **"Port already in use"**: Use different port with `--port 8080`

### Quick Fixes
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Clear database (start fresh)
rm attendees.db

# Check Python version
python --version
```

## 📈 Success Metrics

You'll know it's working when:
- ✅ Database file `attendees.db` is created
- ✅ Dashboard loads at `http://localhost:5000`
- ✅ You can see scraped attendee data
- ✅ Search functionality works
- ✅ Export options are available

## 🎉 Congratulations!

You've successfully set up the DFWTRN Scraper! 

**Next Steps:**
1. Read the [Scraping Guide](scraping-guide.md) for advanced usage
2. Explore the [Dashboard Guide](dashboard-guide.md) for UI features
3. Check the [API Reference](api-reference.md) for programmatic access
4. Review [Troubleshooting](troubleshooting.md) if you encounter issues

---

*Need help? Check the [Troubleshooting Guide](troubleshooting.md) or [Error Reference](error-reference.md)* 
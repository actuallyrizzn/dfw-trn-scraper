# DFWTRN Attendee Dashboard

A comprehensive web application for scraping, storing, and exploring DFWTRN event attendee data with rich profile information.

## 📚 Documentation

**📖 [Complete Documentation](docs/README.md)** - Full documentation index with all guides and references

### 🚀 Getting Started
- **[Installation Guide](docs/installation.md)** - Complete setup instructions for all platforms
- **[Quick Start Guide](docs/quick-start.md)** - Get up and running in 5 minutes
- **[Configuration Guide](docs/configuration.md)** - System configuration options

### 🛠 Usage Guides
- **[Scraping Guide](docs/scraping-guide.md)** - How to scrape attendee data with all options
- **[Dashboard Guide](docs/dashboard-guide.md)** - Using the web interface and features
- **[CLI Reference](docs/cli-reference.md)** - Command-line interface documentation

### 🧩 Technical Documentation
- **[Database Schema](docs/database-schema.md)** - Complete database structure and relationships
- **[API Reference](docs/api-reference.md)** - REST API documentation with examples
- **[Data Model](docs/data-model.md)** - Understanding the data structure

### 🔧 Development & Troubleshooting
- **[Development Setup](docs/development.md)** - Setting up for development
- **[Testing Guide](docs/testing.md)** - Running tests and test data
- **[Troubleshooting Guide](docs/troubleshooting.md)** - Common issues and solutions
- **[Error Reference](docs/error-reference.md)** - Error codes and meanings

## 🚀 Features

- **Live Data Scraping**: Direct-to-database scraping of attendee lists and profile data
- **Rich Profile Data**: Extracts company, job title, contact info, and more from attendee profiles
- **Web Dashboard**: Beautiful Bootstrap-based interface for exploring data
- **Search & Filter**: Find attendees by name, company, or event
- **API Endpoints**: JSON API for programmatic access
- **Pagination**: Handle large datasets efficiently
- **Export Options**: Download data in JSON format
- **Multi-Worker Support**: Parallel processing for faster scraping
- **Resumable Scraping**: Safe to re-run without duplicates

## 📋 Requirements

- Python 3.7+
- SQLite3
- Internet connection for scraping

## 🛠 Installation

1. Clone or download the project files
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

**📖 For detailed installation instructions, see the [Installation Guide](docs/installation.md)**

## 🎯 Quick Start

### Phase 1: Scrape Data
```bash
# Scrape attendee data directly to database
python scrape_to_sql.py "https://www.dfwtrn.org/event-6176250/Attendees?elp=1" --delay 1.5
```

### Phase 2: Launch Dashboard
```bash
# Start the web dashboard
python attendee_dashboard.py
```

Then open your browser to: `http://localhost:5000`

**📖 For detailed usage instructions, see the [Quick Start Guide](docs/quick-start.md)**

## 📊 Dashboard Features

### Overview Page (`/`)
- **Statistics Cards**: Total attendees, events, profiles, coverage percentage
- **Recent Event**: Quick access to latest event details
- **Attendee Breakdown**: Named vs anonymous attendees
- **Top Attendees**: Most frequent attendees across events
- **Quick Actions**: Export, search, and navigation shortcuts

### Event Details (`/event/<id>`)
- **Event Information**: Date, attendee count, event metadata
- **Attendee Table**: Paginated list with profile links
- **Profile Data**: Company, job title, contact information
- **Export Options**: JSON export for specific events

### Search (`/search?q=<query>`)
- **Name Search**: Find attendees by first, last, or full name
- **Cross-Event Results**: Search across all events
- **Profile Integration**: Shows available profile data
- **Pagination**: Handle large result sets

### API Endpoints
- **`/api/attendees`**: Get all attendees (with optional event filtering)
- **`/api/events`**: Get all events
- **Query Parameters**: `event_id`, `limit` for filtering

**📖 For complete API documentation, see the [API Reference](docs/api-reference.md)**

## 🗄 Database Schema

The application uses SQLite with the following tables:

### `attendees`
- Basic attendee information (name, event, registration date)
- Profile URL links
- Anonymous user handling
- Guest count tracking

### `attendee_profiles`
- Rich profile data (email, phone, company, job title)
- Member information (since date, location)
- Skills and certifications

### `profile_fields`
- Dynamic field storage for flexible data
- Key-value pairs for additional profile information

### `events`
- Event metadata and statistics
- Total attendee counts

**📖 For complete database documentation, see the [Database Schema](docs/database-schema.md)**

## 🔧 Configuration

### Scraping Options
- `--delay`: Request delay between pages (default: 1.0s)
- `--max-profiles`: Limit profile analysis (deep analysis only)
- `--workers`: Number of parallel workers (default: 1)
- `--limit`: Maximum events to scrape

### Database
- Database file: `attendees.db` (auto-created)
- Schema: Auto-initialized on first run

**📖 For detailed configuration options, see the [Configuration Guide](docs/configuration.md)**

## 🎨 UI Features

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Bootstrap 5**: Modern, clean interface
- **Bootstrap Icons**: Consistent iconography
- **Dark/Light Mode**: Automatic system preference detection
- **Accessibility**: ARIA labels, keyboard navigation

## 📈 Data Insights

The dashboard provides several analytics:

- **Profile Coverage**: Percentage of attendees with available profiles
- **Anonymous vs Named**: Breakdown of privacy preferences
- **Top Attendees**: Most active community members
- **Event Statistics**: Attendance trends and patterns

## 🔍 Search Capabilities

- **Fuzzy Matching**: Partial name searches
- **Cross-Event**: Find attendees across multiple events
- **Profile Integration**: Show available profile data in results
- **Pagination**: Handle large result sets efficiently

## 📤 Export Options

- **JSON API**: Programmatic access to all data
- **Event-Specific**: Export attendees for specific events
- **Search Results**: Export filtered search results
- **Profile Data**: Include rich profile information

## 🚨 Important Notes

- **Rate Limiting**: Built-in delays to respect server resources
- **Idempotent**: Safe to re-run scrapers (no duplicate data)
- **Error Handling**: Robust error recovery and logging
- **Data Privacy**: Handles anonymous users appropriately

## 🛡 Best Practices

1. **Respectful Scraping**: Use appropriate delays between requests
2. **Data Backup**: Regular database backups recommended
3. **Monitoring**: Check logs for scraping issues
4. **Updates**: Keep dependencies updated for security

## 🔮 Future Enhancements

- **Advanced Search**: Company, date range, location filtering
- **Data Visualization**: Charts and graphs for insights
- **Email Integration**: Contact attendees directly
- **Analytics Dashboard**: Advanced reporting features
- **Multi-Event Support**: Compare events side-by-side

## 🚨 Troubleshooting

**Common Issues:**
- **Module not found**: Run `pip install -r requirements.txt`
- **Database locked**: Use `--workers 1` or restart
- **Connection timeout**: Increase `--delay` to 2.0+ seconds
- **Dashboard won't start**: Use `--port 8080` for different port

**📖 For comprehensive troubleshooting, see the [Troubleshooting Guide](docs/troubleshooting.md)**

## 📞 Support

For issues or questions:

1. **Check the [Troubleshooting Guide](docs/troubleshooting.md)** for common solutions
2. **Review the [Error Reference](docs/error-reference.md)** for specific error codes
3. **Verify database file permissions** and ensure all dependencies are installed
4. **Check network connectivity** for scraping issues

## 📄 License

This project is for educational and research purposes. Please respect the terms of service of the source websites.

---

**📚 [View Complete Documentation](docs/README.md) | [Quick Start](docs/quick-start.md) | [Troubleshooting](docs/troubleshooting.md)** 
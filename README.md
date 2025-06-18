# DFWTRN Attendee Dashboard

A comprehensive web application for scraping, storing, and exploring DFWTRN event attendee data with rich profile information.

## 🚀 Features

- **Live Data Scraping**: Direct-to-database scraping of attendee lists and profile data
- **Rich Profile Data**: Extracts company, job title, contact info, and more from attendee profiles
- **Web Dashboard**: Beautiful Bootstrap-based interface for exploring data
- **Search & Filter**: Find attendees by name, company, or event
- **API Endpoints**: JSON API for programmatic access
- **Pagination**: Handle large datasets efficiently
- **Export Options**: Download data in JSON format

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

## 🎯 Usage

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

## 🔧 Configuration

### Scraping Options
- `--delay`: Request delay between pages (default: 1.0s)
- `--max-profiles`: Limit profile analysis (deep analysis only)

### Database
- Database file: `attendees.db` (auto-created)
- Schema: Auto-initialized on first run

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

## 📞 Support

For issues or questions:
1. Check the logs for error messages
2. Verify database file permissions
3. Ensure all dependencies are installed
4. Check network connectivity for scraping

## 📄 License

This project is for educational and research purposes. Please respect the terms of service of the source websites. 
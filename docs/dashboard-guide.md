# Dashboard Guide

The DFWTRN Dashboard is a web-based interface for exploring and analyzing scraped attendee data. It provides an intuitive way to browse events, search attendees, and export data.

## 🚀 Getting Started

### Launch the Dashboard
```bash
# Start the dashboard
python attendee_dashboard.py

# Access in your browser
# http://localhost:5000
```

### Dashboard Options
```bash
# Custom port
python attendee_dashboard.py --port 8080

# Debug mode
python attendee_dashboard.py --debug

# Custom host
python attendee_dashboard.py --host 0.0.0.0
```

## 🎨 Dashboard Overview

### Main Dashboard (`/`)
The main page provides an overview of all scraped data:

**Statistics Cards:**
- **Total Attendees**: Count of all attendees across events
- **Total Events**: Number of events processed
- **Profiles Available**: Attendees with detailed profile data
- **Coverage Percentage**: Percentage of attendees with profiles

**Recent Events:**
- Latest scraped events with attendee counts
- Quick access to event details
- Event dates and basic information

**Quick Actions:**
- Search bar for finding attendees
- Export options for data download
- Navigation to different sections

### Sample Dashboard Layout
```
┌─────────────────────────────────────────────────────────────┐
│                    DFWTRN Attendee Dashboard                │
├─────────────────────────────────────────────────────────────┤
│ 📊 Statistics                                               │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────┐ │
│ │ 5,847       │ │ 127         │ │ 892         │ │ 15.2%   │ │
│ │ Attendees   │ │ Events      │ │ Profiles    │ │ Coverage│ │
│ └─────────────┘ └─────────────┘ └─────────────┘ └─────────┘ │
├─────────────────────────────────────────────────────────────┤
│ 🔍 Quick Search: [________________] [Search]                │
├─────────────────────────────────────────────────────────────┤
│ 📅 Recent Events                                            │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Event 6176250 - DFWTRN Monthly Meetup (45 attendees)   │ │
│ │ Event 6176249 - Tech Talk Series (32 attendees)        │ │
│ │ Event 6176248 - Networking Night (28 attendees)        │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## 📋 Navigation and Features

### Top Navigation
- **Home** (`/`): Main dashboard overview
- **Events** (`/events`): List of all events
- **Search** (`/search`): Advanced search interface
- **API** (`/api`): API documentation

### Search Functionality
The dashboard provides multiple search options:

**Quick Search (Homepage):**
- Search by name (first, last, or full name)
- Real-time results as you type
- Shows basic attendee information

**Advanced Search (`/search`):**
- More detailed search options
- Filter by event, date range, company
- Export search results

### Search Examples
```
# Find attendees by name
"John Smith" → Shows all attendees with "John" or "Smith"

# Find by company
"Tech Corp" → Shows all attendees from Tech Corp

# Find by event
"Event 6176250" → Shows all attendees from that event
```

## 📊 Event Details Page

### Accessing Event Details
Click on any event card from the main dashboard or navigate to `/event/<event_id>`.

### Event Information Display
```
┌─────────────────────────────────────────────────────────────┐
│ Event Details: DFWTRN Monthly Meetup                       │
├─────────────────────────────────────────────────────────────┤
│ 📅 Date: 15 Jun 2025                                       │
│ 👥 Attendees: 45                                           │
│ 🔗 URL: https://www.dfwtrn.org/event-6176250/             │
├─────────────────────────────────────────────────────────────┤
│ 📋 Attendee List                                           │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Name          │ Date      │ Company    │ Profile       │ │
│ ├─────────────────────────────────────────────────────────┤ │
│ │ John Smith    │ 15 Jun    │ Tech Corp  │ [View]        │ │
│ │ Jane Doe      │ 15 Jun    │ Startup Inc│ [View]        │ │
│ │ Bob Wilson    │ 15 Jun    │ -          │ -             │ │
│ └─────────────────────────────────────────────────────────┘ │
│ [Previous] 1-20 of 45 [Next]                               │
│ [Export JSON] [Export CSV]                                 │
└─────────────────────────────────────────────────────────────┘
```

### Attendee Table Features
- **Sortable Columns**: Click headers to sort
- **Pagination**: Navigate through large attendee lists
- **Profile Links**: Direct links to attendee profiles
- **Export Options**: Download event data

### Profile Information
When available, attendee profiles show:
- **Company**: Employer or organization
- **Job Title**: Professional position
- **Contact Info**: Email and phone (if public)
- **Location**: Geographic location
- **Skills**: Professional skills and expertise
- **Bio**: Personal description

## 🔍 Search Results Page

### Search Interface (`/search`)
```
┌─────────────────────────────────────────────────────────────┐
│ Search Attendees                                            │
├─────────────────────────────────────────────────────────────┤
│ Query: [________________] [Search]                          │
├─────────────────────────────────────────────────────────────┤
│ Filters:                                                    │
│ [ ] Events: [All Events ▼]                                 │
│ [ ] Date Range: [Start] [End]                              │
│ [ ] Company: [All Companies ▼]                             │
├─────────────────────────────────────────────────────────────┤
│ Results: 15 attendees found                                │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Name          │ Event      │ Company    │ Profile       │ │
│ ├─────────────────────────────────────────────────────────┤ │
│ │ John Smith    │ Event 6176 │ Tech Corp  │ [View]        │ │
│ │ John Wilson   │ Event 6175 │ Startup Inc│ [View]        │ │
│ └─────────────────────────────────────────────────────────┘ │
│ [Export Results]                                            │
└─────────────────────────────────────────────────────────────┘
```

### Search Features
- **Fuzzy Matching**: Partial name searches work
- **Cross-Event**: Find attendees across multiple events
- **Filtering**: Narrow results by event, date, company
- **Export**: Download search results

## 📤 Export Options

### Available Export Formats

**JSON Export:**
```json
{
  "event": {
    "id": 6176250,
    "name": "DFWTRN Monthly Meetup",
    "date": "15 Jun 2025",
    "attendees": 45
  },
  "attendees": [
    {
      "name": "John Smith",
      "date": "15 Jun 2025",
      "company": "Tech Corp",
      "job_title": "Software Engineer",
      "profile_url": "https://www.dfwtrn.org/Sys/PublicProfile/12345"
    }
  ]
}
```

**CSV Export:**
```csv
Name,Date,Company,Job Title,Profile URL
John Smith,15 Jun 2025,Tech Corp,Software Engineer,https://www.dfwtrn.org/Sys/PublicProfile/12345
Jane Doe,15 Jun 2025,Startup Inc,Product Manager,https://www.dfwtrn.org/Sys/PublicProfile/67890
```

### Export Locations
- **Event Export**: From event details page
- **Search Export**: From search results page
- **API Export**: Programmatic access via `/api/attendees`

## 🎨 User Interface Features

### Responsive Design
- **Desktop**: Full-featured interface with all options
- **Tablet**: Optimized layout for medium screens
- **Mobile**: Touch-friendly interface for small screens

### Visual Elements
- **Bootstrap 5**: Modern, clean design
- **Bootstrap Icons**: Consistent iconography
- **Color Coding**: Visual indicators for different data types
- **Loading States**: Progress indicators for long operations

### Accessibility
- **Keyboard Navigation**: Full keyboard support
- **Screen Reader**: ARIA labels and semantic HTML
- **High Contrast**: Readable text and backgrounds
- **Focus Indicators**: Clear focus states

## 🔧 Configuration Options

### Dashboard Settings
```bash
# Environment variables for configuration
FLASK_HOST=localhost
FLASK_PORT=5000
FLASK_DEBUG=False
DB_FILE=attendees.db
ITEMS_PER_PAGE=20
```

### Customization
- **Items per page**: Adjust pagination size
- **Search timeout**: Configure search performance
- **Export limits**: Set maximum export size
- **Cache settings**: Configure data caching

## 📊 Data Visualization

### Statistics Display
- **Real-time counts**: Live statistics from database
- **Percentage calculations**: Automatic coverage calculations
- **Trend indicators**: Visual indicators for data trends

### Data Quality Indicators
- **Profile completion**: Shows percentage of attendees with profiles
- **Data freshness**: Indicates when data was last updated
- **Coverage metrics**: Visual representation of data completeness

## 🔍 Advanced Features

### API Integration
The dashboard includes a built-in API for programmatic access:

**Get all attendees:**
```bash
curl http://localhost:5000/api/attendees
```

**Get attendees for specific event:**
```bash
curl http://localhost:5000/api/attendees?event_id=6176250
```

**Search attendees:**
```bash
curl "http://localhost:5000/api/attendees?name=John"
```

### Performance Features
- **Pagination**: Efficient handling of large datasets
- **Caching**: Database query optimization
- **Lazy Loading**: Load data as needed
- **Search Indexing**: Fast search capabilities

## 🚨 Troubleshooting

### Common Issues

**1. "Dashboard won't start"**
```bash
# Check if port is in use
python attendee_dashboard.py --port 8080

# Check database exists
python tools/check_db.py
```

**2. "No data displayed"**
```bash
# Verify database has data
python tools/check_db.py

# Check database file permissions
ls -la attendees.db
```

**3. "Search not working"**
```bash
# Check database indexes
python tools/check_db.py

# Restart dashboard
python attendee_dashboard.py
```

**4. "Export fails"**
```bash
# Check disk space
df -h

# Check file permissions
ls -la
```

### Debug Mode
```bash
# Enable debug mode for detailed error messages
python attendee_dashboard.py --debug
```

## 📈 Performance Tips

### Optimization Strategies
1. **Use pagination**: Don't load all data at once
2. **Enable caching**: Cache frequently accessed data
3. **Optimize queries**: Use database indexes
4. **Limit exports**: Set reasonable export limits

### Monitoring Performance
- **Response times**: Monitor page load times
- **Memory usage**: Watch for memory leaks
- **Database queries**: Optimize slow queries
- **User experience**: Test on different devices

## 🔒 Security Considerations

### Data Protection
- **Local access only**: Dashboard runs locally
- **No authentication**: Designed for local use
- **Data privacy**: Respects attendee privacy settings
- **Export limits**: Prevents data abuse

### Best Practices
1. **Keep local**: Don't expose dashboard publicly
2. **Regular updates**: Keep dependencies updated
3. **Data backup**: Regular database backups
4. **Access control**: Restrict file permissions

## 📞 Getting Help

### Dashboard Status
```bash
# Check dashboard health
python tools/inspect_dashboard.py

# Test API endpoints
curl http://localhost:5000/api/attendees
```

### Common Solutions
1. **Restart dashboard**: `python attendee_dashboard.py`
2. **Check database**: `python tools/check_db.py`
3. **Clear cache**: Restart the application
4. **Check logs**: Look for error messages

### Support Resources
- **Documentation**: Check this guide for specific features
- **API Reference**: See API documentation for programmatic access
- **Troubleshooting**: Review common issues and solutions
- **Database Guide**: Understand the underlying data structure

---

*Next: [API Reference](api-reference.md) or [Data Model](data-model.md)* 
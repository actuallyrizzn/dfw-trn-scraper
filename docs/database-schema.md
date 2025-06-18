# Database Schema

The DFWTRN Scraper uses SQLite as its database engine with a normalized schema designed for efficient querying and data integrity.

## 🗄️ Database Overview

- **Engine**: SQLite 3
- **File**: `attendees.db` (auto-created)
- **Encoding**: UTF-8
- **Concurrency**: WAL mode enabled for multi-worker support

## 📊 Schema Diagram

```
┌─────────────┐    ┌──────────────┐    ┌─────────────────┐    ┌────────────────┐
│   events    │    │  attendees   │    │ attendee_profiles│    │ profile_fields │
├─────────────┤    ├──────────────┤    ├─────────────────┤    ├────────────────┤
│ id (PK)     │◄───│ event_id (FK)│    │ id (PK)         │    │ id (PK)        │
│ event_name  │    │ id (PK)      │◄───│ attendee_id (FK)│◄───│ profile_id (FK)│
│ event_date  │    │ event_date   │    │ profile_url     │    │ field_name     │
│ event_url   │    │ full_name    │    │ email           │    │ field_value    │
│ total_attend│    │ first_name   │    │ phone           │    │ field_type     │
│ created_at  │    │ last_name    │    │ company         │    └────────────────┘
│             │    │ profile_url  │    │ job_title       │
│             │    │ is_anonymous │    │ bio             │
│             │    │ guest_count  │    │ member_since    │
│             │    │ created_at   │    │ location        │
│             │    │              │    │ skills          │
│             │    │              │    │ certifications  │
│             │    │              │    │ last_updated    │
└─────────────┘    └──────────────┘    └─────────────────┘
```

## 📋 Table Definitions

### 1. `events` Table

Stores event metadata and statistics.

```sql
CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    event_name TEXT,
    event_date TEXT,
    event_url TEXT,
    total_attendees INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Columns:**
- `id` (INTEGER, PRIMARY KEY): Unique event identifier from DFWTRN
- `event_name` (TEXT): Human-readable event name
- `event_date` (TEXT): Event date in format "DD MMM YYYY"
- `event_url` (TEXT): Full URL to the event page
- `total_attendees` (INTEGER): Total number of attendees for the event
- `created_at` (TIMESTAMP): When the event record was created

**Indexes:**
- Primary key on `id`
- Index on `event_date` for date-based queries

**Sample Data:**
```sql
INSERT INTO events VALUES (
    6176250,
    'DFWTRN Monthly Meetup',
    '15 Jun 2025',
    'https://www.dfwtrn.org/event-6176250/',
    45,
    '2025-06-18 17:30:00'
);
```

### 2. `attendees` Table

Stores basic attendee information for each event.

```sql
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
    FOREIGN KEY (event_id) REFERENCES events(id),
    UNIQUE(event_id, full_name, event_date)
);
```

**Columns:**
- `id` (INTEGER, PRIMARY KEY): Auto-incrementing unique identifier
- `event_id` (INTEGER, FOREIGN KEY): Reference to events table
- `event_date` (TEXT): Registration date in format "DD MMM YYYY"
- `full_name` (TEXT): Complete attendee name
- `first_name` (TEXT): Extracted first name
- `last_name` (TEXT): Extracted last name
- `profile_url` (TEXT): URL to attendee's profile page (if available)
- `is_anonymous` (BOOLEAN): Whether attendee is anonymous
- `guest_count` (INTEGER): Number of guests registered
- `created_at` (TIMESTAMP): When the record was created

**Constraints:**
- Foreign key constraint on `event_id`
- Unique constraint on `(event_id, full_name, event_date)` to prevent duplicates

**Indexes:**
- Primary key on `id`
- Index on `event_id` for event-based queries
- Index on `full_name` for name searches
- Index on `profile_url` for profile lookups

**Sample Data:**
```sql
INSERT INTO attendees VALUES (
    1,
    6176250,
    '15 Jun 2025',
    'John Smith',
    'John',
    'Smith',
    'https://www.dfwtrn.org/Sys/PublicProfile/12345',
    FALSE,
    0,
    '2025-06-18 17:30:00'
);
```

### 3. `attendee_profiles` Table

Stores detailed profile information for attendees with public profiles.

```sql
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
```

**Columns:**
- `id` (INTEGER, PRIMARY KEY): Auto-incrementing unique identifier
- `attendee_id` (INTEGER, FOREIGN KEY): Reference to attendees table
- `profile_url` (TEXT, UNIQUE): Unique profile URL
- `email` (TEXT): Contact email address
- `phone` (TEXT): Phone number
- `company` (TEXT): Employer or company name
- `job_title` (TEXT): Professional title
- `bio` (TEXT): Biography or description
- `member_since` (TEXT): Membership start date
- `location` (TEXT): Geographic location
- `skills` (TEXT): Skills and expertise
- `certifications` (TEXT): Professional certifications
- `last_updated` (TIMESTAMP): When profile was last updated

**Constraints:**
- Foreign key constraint on `attendee_id`
- Unique constraint on `profile_url`

**Indexes:**
- Primary key on `id`
- Index on `attendee_id` for attendee lookups
- Index on `profile_url` for profile searches
- Index on `company` for company-based queries

**Sample Data:**
```sql
INSERT INTO attendee_profiles VALUES (
    1,
    1,
    'https://www.dfwtrn.org/Sys/PublicProfile/12345',
    'john.smith@techcorp.com',
    '+1-555-0123',
    'Tech Corp',
    'Senior Software Engineer',
    'Experienced developer with 10+ years in web technologies.',
    'Jan 2020',
    'Dallas, TX',
    'Python, JavaScript, React, SQL',
    'AWS Certified Developer, PMP',
    '2025-06-18 17:30:00'
);
```

### 4. `profile_fields` Table

Stores dynamic profile fields for flexible data storage.

```sql
CREATE TABLE profile_fields (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id INTEGER,
    field_name TEXT,
    field_value TEXT,
    field_type TEXT,
    FOREIGN KEY (profile_id) REFERENCES attendee_profiles(id)
);
```

**Columns:**
- `id` (INTEGER, PRIMARY KEY): Auto-incrementing unique identifier
- `profile_id` (INTEGER, FOREIGN KEY): Reference to attendee_profiles table
- `field_name` (TEXT): Name of the dynamic field
- `field_value` (TEXT): Value of the field
- `field_type` (TEXT): Data type or category of the field

**Constraints:**
- Foreign key constraint on `profile_id`

**Indexes:**
- Primary key on `id`
- Index on `profile_id` for profile lookups
- Index on `field_name` for field-based queries

**Sample Data:**
```sql
INSERT INTO profile_fields VALUES 
(1, 1, 'LinkedIn', 'https://linkedin.com/in/johnsmith', 'social'),
(2, 1, 'GitHub', 'https://github.com/johnsmith', 'social'),
(3, 1, 'Years Experience', '10', 'numeric'),
(4, 1, 'Industry', 'Technology', 'category');
```

## 🔗 Relationships

### One-to-Many Relationships
1. **Event → Attendees**: One event can have many attendees
2. **Attendee → Profile**: One attendee can have one profile
3. **Profile → Profile Fields**: One profile can have many dynamic fields

### Foreign Key Constraints
- `attendees.event_id` → `events.id`
- `attendee_profiles.attendee_id` → `attendees.id`
- `profile_fields.profile_id` → `attendee_profiles.id`

## 📊 Data Integrity

### Unique Constraints
- `events.id`: Event IDs are unique
- `attendees(event_id, full_name, event_date)`: No duplicate attendees per event
- `attendee_profiles.profile_url`: Profile URLs are unique

### Data Validation
- All text fields are trimmed and validated
- Boolean fields use SQLite's INTEGER (0/1) representation
- Timestamps use ISO format
- URLs are validated before storage

## 🔍 Common Queries

### Basic Queries

**Get all events with attendee counts:**
```sql
SELECT e.*, COUNT(a.id) as actual_attendees
FROM events e
LEFT JOIN attendees a ON e.id = a.event_id
GROUP BY e.id
ORDER BY e.event_date DESC;
```

**Find attendees with profiles:**
```sql
SELECT a.full_name, a.event_date, p.company, p.job_title
FROM attendees a
JOIN attendee_profiles p ON a.id = p.attendee_id
WHERE a.event_id = 6176250;
```

**Search attendees by name:**
```sql
SELECT a.*, e.event_name
FROM attendees a
JOIN events e ON a.event_id = e.id
WHERE a.full_name LIKE '%John%'
   OR a.first_name LIKE '%John%'
   OR a.last_name LIKE '%John%';
```

### Advanced Queries

**Get company statistics:**
```sql
SELECT p.company, COUNT(*) as employee_count
FROM attendee_profiles p
WHERE p.company IS NOT NULL AND p.company != ''
GROUP BY p.company
ORDER BY employee_count DESC;
```

**Find most active attendees:**
```sql
SELECT a.full_name, COUNT(*) as event_count
FROM attendees a
GROUP BY a.full_name
ORDER BY event_count DESC
LIMIT 10;
```

**Get profile completion rates:**
```sql
SELECT 
    COUNT(*) as total_attendees,
    COUNT(p.id) as profiles_available,
    ROUND(COUNT(p.id) * 100.0 / COUNT(*), 2) as profile_percentage
FROM attendees a
LEFT JOIN attendee_profiles p ON a.id = p.attendee_id;
```

## 🛠️ Database Management

### Backup and Restore
```bash
# Create backup
sqlite3 attendees.db ".backup backup_$(date +%Y%m%d).db"

# Restore from backup
sqlite3 attendees.db ".restore backup_20250618.db"
```

### Database Optimization
```sql
-- Analyze table statistics
ANALYZE;

-- Rebuild indexes
REINDEX;

-- Vacuum database (remove unused space)
VACUUM;
```

### Schema Migration
The database automatically creates tables on first run. For schema changes:

```sql
-- Add new column (example)
ALTER TABLE attendee_profiles ADD COLUMN website TEXT;

-- Create new index
CREATE INDEX idx_attendee_profiles_website ON attendee_profiles(website);
```

## 📈 Performance Considerations

### Indexing Strategy
- Primary keys are automatically indexed
- Foreign keys are indexed for join performance
- Text search fields are indexed for LIKE queries
- Unique constraints create indexes

### Query Optimization
- Use LIMIT for large result sets
- Use WHERE clauses before JOINs
- Use EXPLAIN QUERY PLAN for query analysis
- Consider covering indexes for frequent queries

### Storage Optimization
- TEXT fields use appropriate lengths
- BOOLEAN fields use INTEGER (0/1)
- Timestamps use consistent format
- Regular VACUUM to reclaim space

## 🔒 Security Considerations

### Data Protection
- Database file should have restricted permissions
- No sensitive data is stored in plain text
- Profile URLs are validated before storage
- SQL injection is prevented through parameterized queries

### Access Control
- Database file is local only
- No network access to database
- Application-level access control
- Regular backups recommended

---

*Next: [API Reference](api-reference.md) or [Data Model](data-model.md)* 
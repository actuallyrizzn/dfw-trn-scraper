## 🧩 PROJECT: DFWTRN Scraper + Structured Loader

**Goal:** Scrape DFWTRN public event attendee list, persist raw data, and structure it into a queryable SQLite DB, including deep attendee profile data where available.

---

### 🧱 MODULE 1: `scrape_raw_text.py`

**Role:** (Optional/legacy) Grab all attendee pages and dump unstructured attendee blocks to raw `.txt` or `.csv`.

**Inputs:** `event_id`, optional delay
**Outputs:**

* `raw_attendees_<eventid>_<timestamp>.txt`
* (optional) debug `.html` or `.json` dump per page

**Success Criteria:**

* Accurately captures full attendee list with dates and names
* Handles pagination without missing/duplicating data
* 100% offline-readable (no JS dependency)
* Easy for Jim to run via CLI

https://www.dfwtrn.org/event-6176250/Attendees?elp=1 <=== this is the starter URL

---

### 🧱 MODULE 1.5: `scrape_deep_analysis.py`

**Role:** Scan all attendee list pages for profile links, follow those links, and analyze the richer data structure available on attendee profile pages. Output a JSON file with the discovered profile data and schema suggestions.

**Inputs:** Event attendee URL, optional delay, max profiles to analyze
**Outputs:**

* `deep_analysis_<timestamp>.json` (sampled profile data)
* Schema suggestions for relational DB

**Success Criteria:**

* Finds and follows all attendee profile links across all pagination pages
* Extracts and analyzes richer attendee data (e.g., phone, company, city, member status, bio, etc.)
* Outputs a sample of the data and schema recommendations for the next phase

---

### 🧱 MODULE 2: `scrape_to_sql.py`

**Role:** Scrape attendee lists and deep profile data live from the site and insert all discovered data directly into the SQLite database (no intermediate files required).

**Inputs:** Event attendee URL, optional delay
**Logic:**

* Scrape each attendee list page, extracting `event_date`, `first_name`, `last_name`, `full_name`, etc.
* For each attendee with a profile link, follow and extract all available profile fields
* Insert or update records in the SQLite DB as data is discovered (handle deduplication and normalization)
* Maintain robust, normalized schema for both basic and deep profile data

**Schema:**

```sql
-- Main attendees table
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
    UNIQUE(event_id, full_name, event_date)
);

-- Profile details table (for linked profiles)
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

-- Dynamic profile fields (for flexible data)
CREATE TABLE profile_fields (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id INTEGER,
    field_name TEXT,
    field_value TEXT,
    field_type TEXT,
    FOREIGN KEY (profile_id) REFERENCES attendee_profiles(id)
);

-- Events table
CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    event_name TEXT,
    event_date TEXT,
    event_url TEXT,
    total_attendees INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Success Criteria:**

* Robust, idempotent scraping and direct DB loading
* No duplicate records if rerun
* SQLite file written: `attendees.db`
* Deep profile data is normalized and queryable

---

### 🧱 MODULE 3: Flask Dashboard App

**File:** `attendee_dashboard.py`
**Stack:** Flask + SQLite + Jinja2 templates

**Routes:**

* `/` → Dashboard overview (total attendees, events, most common names)
* `/event/<event_id>` → Table of attendees for one event
* `/search?name=foo` → Search attendees by name substring
* `/api/attendees` → JSON API (optional)

**Frontend Features:**

* Bootstrap for layout
* Table view with pagination
* Optional CSV export button
* Light/dark mode toggle (optional)

**Success Criteria:**

* Localhost deploy with `flask run`
* Reads from same SQLite DB as Module 2
* Returns full page within 100ms for 1k+ records
* Clean UX for Jim's show-and-tell

---

### 🗂 DEPLOYMENT STRUCTURE:

```
/dfwtrn_project/
├── scrape_raw_text.py
├── scrape_deep_analysis.py
├── scrape_to_sql.py
├── attendee_dashboard.py
├── templates/
│   └── index.html
│   └── event.html
├── static/
│   └── styles.css
├── attendees.db
└── README.md
```

---

### 🧩 Optional Add-ons (for Jim to brag)

* 🧠 **Enrichment Hook:** Use PeopleDataLabs or SerpAPI in background to enrich names.
* 🛰 **Public Deploy:** Drop into Fly.io, Replit, or Glitch for quick live demo.
* 🔐 **Basic Auth:** Add login if hosted externally.

---

If you're ready, I'll:

1. Spin up `attendee_dashboard.py` with index + event routes and templating.
2. Drop in minimal HTML with a Bootstrap grid for table display.
3. Stub the data loader if the DB doesn't exist yet.

Want me to move forward with that code now?

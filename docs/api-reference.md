# API Reference

The DFWTRN Dashboard provides a REST API for programmatic access to attendee data. All endpoints return JSON responses and support various query parameters for filtering and pagination.

## 🚀 Base URL

```
http://localhost:5000/api
```

## 📋 Authentication

Currently, the API does not require authentication as it's designed for local use only.

## 📊 Response Format

All API responses follow this standard format:

```json
{
  "success": true,
  "data": [...],
  "meta": {
    "total": 5847,
    "page": 1,
    "per_page": 20,
    "pages": 293
  }
}
```

### Response Fields
- `success` (boolean): Whether the request was successful
- `data` (array/object): The actual data payload
- `meta` (object): Metadata about the response (pagination, counts, etc.)

### Error Responses
```json
{
  "success": false,
  "error": "Error message",
  "code": 400
}
```

## 🔗 Endpoints

### 1. Get All Attendees

**Endpoint:** `GET /api/attendees`

**Description:** Retrieve all attendees with optional filtering and pagination.

**Query Parameters:**
| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `event_id` | integer | Filter by specific event | `?event_id=6176250` |
| `name` | string | Search by name (fuzzy match) | `?name=John` |
| `company` | string | Filter by company | `?company=Tech Corp` |
| `page` | integer | Page number for pagination | `?page=2` |
| `per_page` | integer | Items per page (max 100) | `?per_page=50` |
| `limit` | integer | Limit total results | `?limit=100` |

**Example Request:**
```bash
curl "http://localhost:5000/api/attendees?event_id=6176250&per_page=10"
```

**Example Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "event_id": 6176250,
      "event_date": "15 Jun 2025",
      "full_name": "John Smith",
      "first_name": "John",
      "last_name": "Smith",
      "profile_url": "https://www.dfwtrn.org/Sys/PublicProfile/12345",
      "is_anonymous": false,
      "guest_count": 0,
      "created_at": "2025-06-18T17:30:00",
      "profile": {
        "company": "Tech Corp",
        "job_title": "Software Engineer",
        "email": "john.smith@techcorp.com",
        "phone": "+1-555-0123",
        "location": "Dallas, TX",
        "skills": "Python, JavaScript, React",
        "certifications": "AWS Certified Developer"
      }
    }
  ],
  "meta": {
    "total": 45,
    "page": 1,
    "per_page": 10,
    "pages": 5
  }
}
```

### 2. Get Specific Attendee

**Endpoint:** `GET /api/attendees/{id}`

**Description:** Retrieve a specific attendee by ID.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | integer | Attendee ID |

**Example Request:**
```bash
curl "http://localhost:5000/api/attendees/1"
```

**Example Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "event_id": 6176250,
    "event_date": "15 Jun 2025",
    "full_name": "John Smith",
    "first_name": "John",
    "last_name": "Smith",
    "profile_url": "https://www.dfwtrn.org/Sys/PublicProfile/12345",
    "is_anonymous": false,
    "guest_count": 0,
    "created_at": "2025-06-18T17:30:00",
    "event": {
      "id": 6176250,
      "name": "DFWTRN Monthly Meetup",
      "date": "15 Jun 2025",
      "url": "https://www.dfwtrn.org/event-6176250/"
    },
    "profile": {
      "id": 1,
      "company": "Tech Corp",
      "job_title": "Software Engineer",
      "email": "john.smith@techcorp.com",
      "phone": "+1-555-0123",
      "bio": "Experienced developer with 10+ years in web technologies.",
      "member_since": "Jan 2020",
      "location": "Dallas, TX",
      "skills": "Python, JavaScript, React, SQL",
      "certifications": "AWS Certified Developer, PMP",
      "last_updated": "2025-06-18T17:30:00"
    }
  }
}
```

### 3. Get All Events

**Endpoint:** `GET /api/events`

**Description:** Retrieve all events with attendee counts.

**Query Parameters:**
| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `page` | integer | Page number for pagination | `?page=2` |
| `per_page` | integer | Items per page (max 100) | `?per_page=50` |
| `limit` | integer | Limit total results | `?limit=20` |

**Example Request:**
```bash
curl "http://localhost:5000/api/events?per_page=5"
```

**Example Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 6176250,
      "name": "DFWTRN Monthly Meetup",
      "date": "15 Jun 2025",
      "url": "https://www.dfwtrn.org/event-6176250/",
      "total_attendees": 45,
      "created_at": "2025-06-18T17:30:00",
      "attendee_count": 45,
      "profile_count": 12
    }
  ],
  "meta": {
    "total": 127,
    "page": 1,
    "per_page": 5,
    "pages": 26
  }
}
```

### 4. Get Specific Event

**Endpoint:** `GET /api/events/{id}`

**Description:** Retrieve a specific event with attendee details.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | integer | Event ID |

**Query Parameters:**
| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `include_attendees` | boolean | Include attendee list | `?include_attendees=true` |
| `page` | integer | Page number for attendees | `?page=2` |
| `per_page` | integer | Attendees per page | `?per_page=20` |

**Example Request:**
```bash
curl "http://localhost:5000/api/events/6176250?include_attendees=true&per_page=10"
```

**Example Response:**
```json
{
  "success": true,
  "data": {
    "id": 6176250,
    "name": "DFWTRN Monthly Meetup",
    "date": "15 Jun 2025",
    "url": "https://www.dfwtrn.org/event-6176250/",
    "total_attendees": 45,
    "created_at": "2025-06-18T17:30:00",
    "attendee_count": 45,
    "profile_count": 12,
    "attendees": [
      {
        "id": 1,
        "event_date": "15 Jun 2025",
        "full_name": "John Smith",
        "first_name": "John",
        "last_name": "Smith",
        "profile_url": "https://www.dfwtrn.org/Sys/PublicProfile/12345",
        "is_anonymous": false,
        "guest_count": 0,
        "profile": {
          "company": "Tech Corp",
          "job_title": "Software Engineer"
        }
      }
    ]
  },
  "meta": {
    "total_attendees": 45,
    "page": 1,
    "per_page": 10,
    "pages": 5
  }
}
```

### 5. Search Attendees

**Endpoint:** `GET /api/search`

**Description:** Search attendees with advanced filtering.

**Query Parameters:**
| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `q` | string | Search query (name, company) | `?q=John` |
| `event_id` | integer | Filter by event | `?event_id=6176250` |
| `company` | string | Filter by company | `?company=Tech Corp` |
| `page` | integer | Page number | `?page=2` |
| `per_page` | integer | Items per page | `?per_page=20` |

**Example Request:**
```bash
curl "http://localhost:5000/api/search?q=John&company=Tech Corp"
```

**Example Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "event_id": 6176250,
      "full_name": "John Smith",
      "company": "Tech Corp",
      "job_title": "Software Engineer",
      "event_name": "DFWTRN Monthly Meetup",
      "event_date": "15 Jun 2025"
    }
  ],
  "meta": {
    "total": 1,
    "page": 1,
    "per_page": 20,
    "pages": 1,
    "query": "John",
    "filters": {
      "company": "Tech Corp"
    }
  }
}
```

### 6. Get Statistics

**Endpoint:** `GET /api/stats`

**Description:** Get overall statistics about the data.

**Example Request:**
```bash
curl "http://localhost:5000/api/stats"
```

**Example Response:**
```json
{
  "success": true,
  "data": {
    "total_attendees": 5847,
    "total_events": 127,
    "total_profiles": 892,
    "profile_coverage": 15.2,
    "anonymous_attendees": 234,
    "top_companies": [
      {
        "company": "Tech Corp",
        "count": 45
      },
      {
        "company": "Startup Inc",
        "count": 32
      }
    ],
    "most_active_attendees": [
      {
        "name": "John Smith",
        "event_count": 8
      },
      {
        "name": "Jane Doe",
        "event_count": 7
      }
    ],
    "recent_events": [
      {
        "id": 6176250,
        "name": "DFWTRN Monthly Meetup",
        "date": "15 Jun 2025",
        "attendees": 45
      }
    ]
  }
}
```

### 7. Get Profile Details

**Endpoint:** `GET /api/profiles/{id}`

**Description:** Retrieve detailed profile information.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | integer | Profile ID |

**Example Request:**
```bash
curl "http://localhost:5000/api/profiles/1"
```

**Example Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "attendee_id": 1,
    "profile_url": "https://www.dfwtrn.org/Sys/PublicProfile/12345",
    "email": "john.smith@techcorp.com",
    "phone": "+1-555-0123",
    "company": "Tech Corp",
    "job_title": "Senior Software Engineer",
    "bio": "Experienced developer with 10+ years in web technologies.",
    "member_since": "Jan 2020",
    "location": "Dallas, TX",
    "skills": "Python, JavaScript, React, SQL",
    "certifications": "AWS Certified Developer, PMP",
    "last_updated": "2025-06-18T17:30:00",
    "attendee": {
      "id": 1,
      "full_name": "John Smith",
      "event_id": 6176250,
      "event_date": "15 Jun 2025"
    },
    "fields": [
      {
        "field_name": "LinkedIn",
        "field_value": "https://linkedin.com/in/johnsmith",
        "field_type": "social"
      },
      {
        "field_name": "GitHub",
        "field_value": "https://github.com/johnsmith",
        "field_type": "social"
      }
    ]
  }
}
```

## 🔍 Advanced Queries

### Complex Filtering

**Multiple filters:**
```bash
curl "http://localhost:5000/api/attendees?event_id=6176250&company=Tech Corp&per_page=50"
```

**Date range filtering:**
```bash
curl "http://localhost:5000/api/attendees?event_date_start=2025-01-01&event_date_end=2025-06-30"
```

**Profile availability:**
```bash
curl "http://localhost:5000/api/attendees?has_profile=true"
```

### Pagination Examples

**First page:**
```bash
curl "http://localhost:5000/api/attendees?page=1&per_page=20"
```

**Next page:**
```bash
curl "http://localhost:5000/api/attendees?page=2&per_page=20"
```

**Large result set:**
```bash
curl "http://localhost:5000/api/attendees?per_page=100&limit=1000"
```

## 📊 Response Headers

All API responses include these headers:

```
Content-Type: application/json
X-Total-Count: 5847
X-Page: 1
X-Per-Page: 20
X-Total-Pages: 293
Cache-Control: no-cache
```

## 🚨 Error Handling

### HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request (invalid parameters) |
| 404 | Not Found (resource doesn't exist) |
| 500 | Internal Server Error |

### Error Response Format

```json
{
  "success": false,
  "error": "Invalid event_id parameter",
  "code": 400,
  "details": {
    "parameter": "event_id",
    "value": "invalid",
    "expected": "integer"
  }
}
```

### Common Error Scenarios

**Invalid event ID:**
```json
{
  "success": false,
  "error": "Event not found",
  "code": 404
}
```

**Invalid pagination:**
```json
{
  "success": false,
  "error": "Page number must be positive",
  "code": 400
}
```

**Database error:**
```json
{
  "success": false,
  "error": "Database connection failed",
  "code": 500
}
```

## 🔧 Rate Limiting

Currently, the API does not implement rate limiting as it's designed for local use. For production deployments, consider implementing rate limiting.

## 📈 Performance Tips

### Efficient Queries
1. **Use pagination**: Always use `per_page` parameter
2. **Limit results**: Use `limit` for large datasets
3. **Specific filters**: Use `event_id` instead of broad searches
4. **Avoid large exports**: Use pagination for large result sets

### Caching
- Responses are not cached by default
- Consider implementing client-side caching
- Use ETags for conditional requests

## 🔒 Security Considerations

### Data Privacy
- API returns only public data
- No sensitive information is exposed
- Profile data respects privacy settings

### Access Control
- API is designed for local use only
- No authentication required
- Consider firewall rules for production

## 📞 Testing the API

### Using curl

**Basic test:**
```bash
curl "http://localhost:5000/api/attendees?limit=5"
```

**Test with filters:**
```bash
curl "http://localhost:5000/api/attendees?event_id=6176250&per_page=10"
```

**Test search:**
```bash
curl "http://localhost:5000/api/search?q=John"
```

### Using Python

```python
import requests

# Get all attendees
response = requests.get("http://localhost:5000/api/attendees?limit=10")
data = response.json()

# Search attendees
response = requests.get("http://localhost:5000/api/search?q=John")
results = response.json()

# Get specific event
response = requests.get("http://localhost:5000/api/events/6176250")
event = response.json()
```

### Using JavaScript

```javascript
// Get all attendees
fetch('/api/attendees?limit=10')
  .then(response => response.json())
  .then(data => console.log(data));

// Search attendees
fetch('/api/search?q=John')
  .then(response => response.json())
  .then(results => console.log(results));
```

## 📋 API Versioning

Current API version: **v1**

Future versions will be available at `/api/v2/`, `/api/v3/`, etc.

---

*Next: [Data Model](data-model.md) or [Troubleshooting](troubleshooting.md)* 
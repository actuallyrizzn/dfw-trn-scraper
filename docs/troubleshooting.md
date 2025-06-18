# Troubleshooting Guide

This guide helps you resolve common issues with the DFWTRN Scraper and Dashboard. Each section includes symptoms, causes, and step-by-step solutions.

## 🚨 Quick Diagnosis

### Check System Status
```bash
# Test Python installation
python --version

# Test dependencies
python -c "import requests, bs4, flask, sqlite3; print('✓ All OK')"

# Check database
python tools/check_db.py

# Test dashboard
python tools/inspect_dashboard.py
```

## 🔧 Common Issues

### 1. Installation Problems

#### Issue: "Module not found" errors
**Symptoms:**
```
ModuleNotFoundError: No module named 'requests'
ModuleNotFoundError: No module named 'bs4'
ModuleNotFoundError: No module named 'flask'
```

**Causes:**
- Virtual environment not activated
- Dependencies not installed
- Python version mismatch

**Solutions:**
```bash
# 1. Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Verify installation
pip list | grep -E "(requests|bs4|flask)"
```

#### Issue: Python version problems
**Symptoms:**
```
SyntaxError: invalid syntax
AttributeError: 'str' object has no attribute 'decode'
```

**Solutions:**
```bash
# Check Python version (needs 3.7+)
python --version

# If using Python 2, use python3
python3 --version
python3 -m pip install -r requirements.txt
```

### 2. Scraping Issues

#### Issue: "Connection timeout" errors
**Symptoms:**
```
requests.exceptions.ConnectTimeout
requests.exceptions.ReadTimeout
```

**Causes:**
- Network connectivity issues
- Server overload
- Firewall blocking requests

**Solutions:**
```bash
# 1. Test internet connection
python -c "import requests; print(requests.get('https://www.google.com').status_code)"

# 2. Increase timeout and delay
python scrape_to_sql.py --all --delay 3.0 --workers 1

# 3. Test with single event first
python scrape_to_sql.py "https://www.dfwtrn.org/event-6176250/Attendees?elp=1"
```

#### Issue: "Database is locked" errors
**Symptoms:**
```
sqlite3.OperationalError: database is locked
```

**Causes:**
- Multiple processes accessing database
- Database file permissions
- SQLite WAL mode issues

**Solutions:**
```bash
# 1. Stop all running scrapers
# Press Ctrl+C in all terminal windows

# 2. Use single worker
python scrape_to_sql.py --all --workers 1

# 3. Check file permissions
ls -la attendees.db

# 4. Restart with fresh database (if needed)
rm attendees.db
python scrape_to_sql.py --all --limit 1
```

#### Issue: "Rate limited" or "403 Forbidden"
**Symptoms:**
```
HTTPError: 403 Forbidden
HTTPError: 429 Too Many Requests
```

**Causes:**
- Too many requests too quickly
- Server anti-bot protection
- IP address blocked

**Solutions:**
```bash
# 1. Increase delay significantly
python scrape_to_sql.py --all --delay 5.0 --workers 1

# 2. Use single worker only
python scrape_to_sql.py --all --workers 1 --delay 3.0

# 3. Wait and retry later
# Wait 1-2 hours before retrying

# 4. Test with VPN (if available)
```

#### Issue: "Memory error" or "Out of memory"
**Symptoms:**
```
MemoryError: Unable to allocate array
Killed (process killed by system)
```

**Causes:**
- Too many workers
- Large dataset processing
- Insufficient RAM

**Solutions:**
```bash
# 1. Reduce workers and limits
python scrape_to_sql.py --all --workers 1 --limit 10

# 2. Process in smaller batches
python scrape_to_sql.py --all --limit 5
python scrape_to_sql.py --all --limit 5 --offset 5

# 3. Close other applications
# Free up system memory
```

### 3. Database Issues

#### Issue: "Database file not found"
**Symptoms:**
```
sqlite3.OperationalError: no such table
FileNotFoundError: [Errno 2] No such file or directory: 'attendees.db'
```

**Causes:**
- Database not created
- Wrong working directory
- File permissions

**Solutions:**
```bash
# 1. Check current directory
pwd
ls -la attendees.db

# 2. Create database by running scraper
python scrape_to_sql.py --all --limit 1

# 3. Check database creation
python tools/check_db.py
```

#### Issue: "Database corruption" errors
**Symptoms:**
```
sqlite3.DatabaseError: database disk image is malformed
sqlite3.OperationalError: database or disk is full
```

**Solutions:**
```bash
# 1. Backup current database
cp attendees.db attendees_backup.db

# 2. Try to repair database
sqlite3 attendees.db "PRAGMA integrity_check;"

# 3. If corrupted, start fresh
rm attendees.db
python scrape_to_sql.py --all --limit 1
```

#### Issue: "Unique constraint failed"
**Symptoms:**
```
sqlite3.IntegrityError: UNIQUE constraint failed
```

**Causes:**
- Duplicate data insertion
- Database constraint violations

**Solutions:**
```bash
# 1. Check for duplicates
python tools/check_db.py

# 2. Clean database (if needed)
sqlite3 attendees.db "DELETE FROM attendees WHERE id NOT IN (SELECT MIN(id) FROM attendees GROUP BY event_id, full_name, event_date);"

# 3. Re-run scraper (it's idempotent)
python scrape_to_sql.py --all --limit 1
```

### 4. Dashboard Issues

#### Issue: "Dashboard won't start"
**Symptoms:**
```
Address already in use
Port 5000 is already in use
```

**Solutions:**
```bash
# 1. Use different port
python attendee_dashboard.py --port 8080

# 2. Find and kill process using port 5000
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -i :5000
kill -9 <PID>
```

#### Issue: "No data displayed in dashboard"
**Symptoms:**
- Dashboard loads but shows empty statistics
- "No events found" message
- Zero counts in all categories

**Solutions:**
```bash
# 1. Check if database has data
python tools/check_db.py

# 2. Verify database file exists
ls -la attendees.db

# 3. Check database permissions
chmod 644 attendees.db

# 4. Restart dashboard
python attendee_dashboard.py
```

#### Issue: "Search not working"
**Symptoms:**
- Search returns no results
- Search page errors
- Search times out

**Solutions:**
```bash
# 1. Check database indexes
python tools/check_db.py

# 2. Test search directly
python -c "
import sqlite3
conn = sqlite3.connect('attendees.db')
cursor = conn.execute('SELECT COUNT(*) FROM attendees WHERE full_name LIKE ?', ('%John%',))
print('Search results:', cursor.fetchone()[0])
"

# 3. Restart dashboard
python attendee_dashboard.py
```

#### Issue: "Export fails"
**Symptoms:**
- Export button doesn't work
- Download fails
- Empty export files

**Solutions:**
```bash
# 1. Check disk space
df -h  # macOS/Linux
dir    # Windows

# 2. Check file permissions
ls -la

# 3. Test export manually
curl "http://localhost:5000/api/attendees?limit=5" > test_export.json
```

### 5. Performance Issues

#### Issue: "Scraping is very slow"
**Symptoms:**
- Takes hours to scrape few events
- Very low processing rate
- High delay between requests

**Solutions:**
```bash
# 1. Increase workers (if network allows)
python scrape_to_sql.py --all --workers 3 --delay 1.0

# 2. Reduce delay (be respectful)
python scrape_to_sql.py --all --workers 2 --delay 0.5

# 3. Check network speed
speedtest-cli  # Install with: pip install speedtest-cli
```

#### Issue: "Dashboard is slow"
**Symptoms:**
- Long page load times
- Search takes seconds
- Export times out

**Solutions:**
```bash
# 1. Check database size
ls -lh attendees.db

# 2. Optimize database
sqlite3 attendees.db "ANALYZE; VACUUM;"

# 3. Use pagination
# Dashboard automatically paginates large datasets

# 4. Check system resources
top  # macOS/Linux
taskmgr  # Windows
```

## 🔍 Debug Mode

### Enable Debug Logging
```bash
# Scraper debug mode
python scrape_to_sql.py --all --limit 2 --verbose

# Dashboard debug mode
python attendee_dashboard.py --debug
```

### Check Logs
```bash
# Look for error patterns
grep -i error scraper.log
grep -i exception scraper.log
grep -i failed scraper.log
```

## 🛠️ Advanced Troubleshooting

### Database Diagnostics
```bash
# Check database integrity
sqlite3 attendees.db "PRAGMA integrity_check;"

# Check table structure
sqlite3 attendees.db ".schema"

# Check data counts
sqlite3 attendees.db "SELECT COUNT(*) FROM events; SELECT COUNT(*) FROM attendees; SELECT COUNT(*) FROM attendee_profiles;"

# Check for duplicates
sqlite3 attendees.db "SELECT event_id, full_name, event_date, COUNT(*) FROM attendees GROUP BY event_id, full_name, event_date HAVING COUNT(*) > 1;"
```

### Network Diagnostics
```bash
# Test connectivity to DFWTRN
curl -I https://www.dfwtrn.org

# Test specific event page
curl -I "https://www.dfwtrn.org/event-6176250/Attendees?elp=1"

# Check DNS resolution
nslookup www.dfwtrn.org

# Test with different user agent
curl -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" https://www.dfwtrn.org
```

### System Diagnostics
```bash
# Check Python environment
python -c "import sys; print(sys.version); print(sys.executable)"

# Check installed packages
pip list

# Check system resources
# Windows: taskmgr
# macOS: Activity Monitor
# Linux: htop or top
```

## 📞 Getting Help

### Information to Collect
When reporting issues, include:

1. **System Information:**
   ```bash
   python --version
   pip list
   uname -a  # macOS/Linux
   systeminfo  # Windows
   ```

2. **Error Messages:**
   - Full error traceback
   - Log files
   - Screenshots (for UI issues)

3. **Steps to Reproduce:**
   - Exact commands run
   - Expected vs actual behavior
   - When the issue started

4. **Environment Details:**
   - Operating system
   - Python version
   - Network environment
   - Any recent changes

### Common Solutions Summary

| Issue | Quick Fix | Full Solution |
|-------|-----------|---------------|
| Module not found | `pip install -r requirements.txt` | Activate venv, reinstall |
| Database locked | `--workers 1` | Stop all processes, restart |
| Connection timeout | `--delay 3.0` | Check network, increase timeout |
| Rate limited | `--delay 5.0 --workers 1` | Wait, use VPN, reduce load |
| Dashboard won't start | `--port 8080` | Kill process, check port |
| No data displayed | `python tools/check_db.py` | Verify database, check permissions |
| Search not working | Restart dashboard | Check indexes, test queries |
| Export fails | Check disk space | Verify permissions, test manually |

## 🔄 Recovery Procedures

### Complete Reset
If all else fails, start fresh:

```bash
# 1. Backup current data
cp attendees.db attendees_backup_$(date +%Y%m%d).db

# 2. Remove current database
rm attendees.db

# 3. Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# 4. Start fresh scraping
python scrape_to_sql.py --all --limit 5

# 5. Verify data
python tools/check_db.py
```

### Data Recovery
If you need to recover from backup:

```bash
# 1. Stop all processes
# 2. Restore from backup
cp attendees_backup_20250618.db attendees.db

# 3. Verify data integrity
python tools/check_db.py

# 4. Resume scraping
python scrape_to_sql.py --all
```

---

*Need more help? Check the [Error Reference](error-reference.md) for specific error codes and meanings.* 
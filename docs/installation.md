# Installation Guide

This guide will walk you through installing and setting up the DFWTRN Scraper on your system.

## 📋 Prerequisites

### System Requirements
- **Operating System**: Windows 10/11, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: Version 3.7 or higher
- **Memory**: Minimum 4GB RAM (8GB recommended)
- **Storage**: At least 1GB free space
- **Network**: Internet connection for scraping

### Required Software
- **Python 3.7+**: [Download from python.org](https://www.python.org/downloads/)
- **Git**: [Download from git-scm.com](https://git-scm.com/downloads)
- **SQLite**: Usually included with Python

## 🚀 Installation Steps

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/actuallyrizzn/dfw-trn-scraper.git

# Navigate to the project directory
cd dfw-trn-scraper
```

### Step 2: Set Up Virtual Environment

**Windows:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

**macOS/Linux:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt
```

### Step 4: Verify Installation

```bash
# Check Python version
python --version

# Verify packages are installed
pip list

# Test basic functionality
python -c "import requests, bs4, flask; print('All dependencies installed successfully!')"
```

## 🔧 Configuration

### Database Setup
The database will be automatically created on first run. No manual setup required.

### Environment Variables (Optional)
Create a `.env` file in the project root for custom configuration:

```bash
# Scraping settings
SCRAPE_DELAY=1.5
MAX_WORKERS=3
LOG_LEVEL=INFO

# Database settings
DB_FILE=attendees.db

# Dashboard settings
FLASK_HOST=localhost
FLASK_PORT=5000
FLASK_DEBUG=False
```

## 🧪 Testing the Installation

### Test Scraping
```bash
# Test with a single event
python scrape_to_sql.py --all --limit 1

# Check if data was collected
python tools/check_db.py
```

### Test Dashboard
```bash
# Start the dashboard
python attendee_dashboard.py

# Open browser to http://localhost:5000
```

## 🐛 Troubleshooting Installation

### Common Issues

**1. Python not found**
```bash
# Windows: Add Python to PATH
# macOS/Linux: Use python3 instead of python
python3 --version
```

**2. Virtual environment issues**
```bash
# Recreate virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

**3. Permission errors**
```bash
# Windows: Run as Administrator
# macOS/Linux: Use sudo if needed
sudo pip install -r requirements.txt
```

**4. Network connectivity issues**
```bash
# Test internet connection
python -c "import requests; print(requests.get('https://www.dfwtrn.org').status_code)"
```

### Platform-Specific Notes

**Windows:**
- Ensure Python is added to PATH during installation
- Use `venv\Scripts\activate` to activate virtual environment
- Use backslashes in file paths

**macOS:**
- Install Xcode Command Line Tools if needed: `xcode-select --install`
- Use `python3` instead of `python` if both versions are installed

**Linux (Ubuntu/Debian):**
```bash
# Install system dependencies
sudo apt update
sudo apt install python3-pip python3-venv git

# Install Python packages
sudo apt install python3-requests python3-bs4 python3-flask
```

## 🔒 Security Considerations

### Network Security
- The scraper makes HTTP requests to external websites
- Ensure your firewall allows outbound HTTP/HTTPS traffic
- Consider using a VPN if scraping from restricted networks

### Data Privacy
- Scraped data is stored locally in SQLite database
- No data is transmitted to external services
- Review the source website's terms of service

### File Permissions
```bash
# Set appropriate file permissions (Linux/macOS)
chmod 600 attendees.db
chmod 755 *.py
```

## 📦 Alternative Installation Methods

### Using Docker (Advanced)
```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "attendee_dashboard.py"]
```

### Using Conda
```bash
# Create conda environment
conda create -n dfwtrn python=3.9
conda activate dfwtrn

# Install packages
pip install -r requirements.txt
```

## ✅ Installation Verification

After installation, verify everything works:

1. **Database Creation**: Run scraper once to create database
2. **Web Dashboard**: Start dashboard and access via browser
3. **Data Export**: Test export functionality
4. **Search**: Verify search features work

### Quick Verification Script
```bash
#!/bin/bash
# Run this to verify installation

echo "Testing Python installation..."
python --version

echo "Testing dependencies..."
python -c "import requests, bs4, flask, sqlite3; print('✓ All dependencies OK')"

echo "Testing scraper..."
python scrape_to_sql.py --all --limit 1

echo "Testing dashboard..."
python attendee_dashboard.py &
sleep 5
curl -s http://localhost:5000 > /dev/null && echo "✓ Dashboard OK" || echo "✗ Dashboard failed"

echo "Installation verification complete!"
```

## 📞 Getting Help

If you encounter issues during installation:

1. Check the [Troubleshooting Guide](../docs/troubleshooting.md)
2. Review the [Error Reference](../docs/error-reference.md)
3. Check Python and package versions match requirements
4. Ensure all prerequisites are installed

---

*Next: [Quick Start Guide](quick-start.md)* 
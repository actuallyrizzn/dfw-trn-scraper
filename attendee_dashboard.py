#!/usr/bin/env python3
"""
DFWTRN Attendee Dashboard
Flask web application for exploring attendee data from the SQLite database.
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
from datetime import datetime
import os
import logging

app = Flask(__name__)
app.config['DATABASE'] = 'attendees.db'

def get_db():
    """Get database connection"""
    db = sqlite3.connect(app.config['DATABASE'])
    db.row_factory = sqlite3.Row
    return db

@app.route('/')
def index():
    """Dashboard overview page"""
    db = get_db()
    
    # Get summary statistics
    total_attendees = db.execute('SELECT COUNT(*) FROM attendees').fetchone()[0]
    total_events = db.execute('SELECT COUNT(*) FROM events').fetchone()[0]
    total_profiles = db.execute('SELECT COUNT(*) FROM attendee_profiles').fetchone()[0]
    
    # Get most recent event
    recent_event = db.execute('''
        SELECT * FROM events 
        ORDER BY created_at DESC 
        LIMIT 1
    ''').fetchone()
    
    # Get top attendees by name frequency
    top_names = db.execute('''
        SELECT first_name, last_name, COUNT(*) as count 
        FROM attendees 
        WHERE is_anonymous = 0 
        GROUP BY first_name, last_name 
        ORDER BY count DESC 
        LIMIT 10
    ''').fetchall()
    
    # Get anonymous vs named attendees
    anonymous_count = db.execute('''
        SELECT COUNT(*) FROM attendees WHERE is_anonymous = 1
    ''').fetchone()[0]
    
    named_count = total_attendees - anonymous_count
    
    db.close()
    
    return render_template('index.html',
                         total_attendees=total_attendees,
                         total_events=total_events,
                         total_profiles=total_profiles,
                         recent_event=recent_event,
                         top_names=top_names,
                         anonymous_count=anonymous_count,
                         named_count=named_count)

@app.route('/event/<int:event_id>')
def event_detail(event_id):
    """Show attendees for a specific event"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    offset = (page - 1) * per_page
    db = get_db()
    # Get event info
    event = db.execute('SELECT * FROM events WHERE id = ?', (event_id,)).fetchone()
    if not event:
        logging.error(f"Event not found: {event_id}")
        return render_template('event.html', event=None, attendees=[], page=1, total_pages=1, total_attendees=0, error="Event not found")
    # Get attendees with pagination and richer profile fields (no membership_level)
    attendees = db.execute('''
        SELECT a.*, ap.email, ap.company, ap.job_title, ap.phone
        FROM attendees a
        LEFT JOIN attendee_profiles ap ON a.id = ap.attendee_id
        WHERE a.event_id = ?
        ORDER BY a.event_date DESC, a.full_name
        LIMIT ? OFFSET ?
    ''', (event_id, per_page, offset)).fetchall()
    if not attendees:
        logging.warning(f"No attendees found for event {event_id}")
    # Get total count for pagination
    total_attendees = db.execute('''
        SELECT COUNT(*) FROM attendees WHERE event_id = ?
    ''', (event_id,)).fetchone()[0]
    total_pages = (total_attendees + per_page - 1) // per_page
    db.close()
    return render_template('event.html',
                         event=event,
                         attendees=attendees,
                         page=page,
                         total_pages=total_pages,
                         total_attendees=total_attendees,
                         error=None)

@app.route('/search')
def search():
    """Search attendees by name"""
    query = request.args.get('q', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = 20
    offset = (page - 1) * per_page
    if not query:
        return redirect(url_for('index'))
    db = get_db()
    # Search in attendees table with richer profile fields (no membership_level)
    attendees = db.execute('''
        SELECT a.*, e.event_name, ap.email, ap.company, ap.job_title, ap.phone
        FROM attendees a
        LEFT JOIN events e ON a.event_id = e.id
        LEFT JOIN attendee_profiles ap ON a.id = ap.attendee_id
        WHERE (a.full_name LIKE ? OR a.first_name LIKE ? OR a.last_name LIKE ?)
        ORDER BY a.event_date DESC, a.full_name
        LIMIT ? OFFSET ?
    ''', (f'%{query}%', f'%{query}%', f'%{query}%', per_page, offset)).fetchall()
    # Get total count for pagination
    total_results = db.execute('''
        SELECT COUNT(*) FROM attendees 
        WHERE (full_name LIKE ? OR first_name LIKE ? OR last_name LIKE ?)
    ''', (f'%{query}%', f'%{query}%', f'%{query}%')).fetchone()[0]
    total_pages = (total_results + per_page - 1) // per_page
    db.close()
    return render_template('search.html',
                         query=query,
                         attendees=attendees,
                         page=page,
                         total_pages=total_pages,
                         total_results=total_results)

@app.route('/api/attendees')
def api_attendees():
    """JSON API for attendees"""
    event_id = request.args.get('event_id', type=int)
    limit = request.args.get('limit', 50, type=int)
    
    db = get_db()
    
    if event_id:
        attendees = db.execute('''
            SELECT a.*, ap.email, ap.company, ap.job_title
            FROM attendees a
            LEFT JOIN attendee_profiles ap ON a.id = ap.attendee_id
            WHERE a.event_id = ?
            ORDER BY a.event_date DESC, a.full_name
            LIMIT ?
        ''', (event_id, limit)).fetchall()
    else:
        attendees = db.execute('''
            SELECT a.*, e.event_name, ap.email, ap.company, ap.job_title
            FROM attendees a
            LEFT JOIN events e ON a.event_id = e.id
            LEFT JOIN attendee_profiles ap ON a.id = ap.attendee_id
            ORDER BY a.event_date DESC, a.full_name
            LIMIT ?
        ''', (limit,)).fetchall()
    
    db.close()
    
    # Convert to dict for JSON serialization
    result = []
    for attendee in attendees:
        attendee_dict = dict(attendee)
        # Convert datetime objects to strings
        if attendee_dict.get('created_at'):
            attendee_dict['created_at'] = attendee_dict['created_at']
        result.append(attendee_dict)
    
    return jsonify(result)

@app.route('/api/events')
def api_events():
    """JSON API for events"""
    db = get_db()
    events = db.execute('SELECT * FROM events ORDER BY created_at DESC').fetchall()
    db.close()
    
    result = [dict(event) for event in events]
    return jsonify(result)

@app.route('/events')
def events():
    """List all events"""
    db = get_db()
    events = db.execute('SELECT * FROM events ORDER BY event_date DESC').fetchall()
    db.close()
    return render_template('events.html', events=events)

@app.route('/attendees')
def attendees():
    """Browse all attendees with pagination"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    offset = (page - 1) * per_page
    db = get_db()
    attendees = db.execute('''
        SELECT a.*, ap.email, ap.company, ap.job_title, ap.phone, e.event_name
        FROM attendees a
        LEFT JOIN attendee_profiles ap ON a.id = ap.attendee_id
        LEFT JOIN events e ON a.event_id = e.id
        ORDER BY a.event_date DESC, a.full_name
        LIMIT ? OFFSET ?
    ''', (per_page, offset)).fetchall()
    total_attendees = db.execute('SELECT COUNT(*) FROM attendees').fetchone()[0]
    total_pages = (total_attendees + per_page - 1) // per_page
    db.close()
    return render_template('attendees.html', attendees=attendees, page=page, total_pages=total_pages, total_attendees=total_attendees)

@app.route('/attendee/<int:attendee_id>')
def attendee_detail(attendee_id):
    """Show detail for a single attendee"""
    db = get_db()
    attendee = db.execute('''
        SELECT a.*, ap.email, ap.company, ap.job_title, ap.phone, ap.bio, ap.member_since, ap.location, ap.skills, ap.certifications, ap.profile_url as external_profile_url
        FROM attendees a
        LEFT JOIN attendee_profiles ap ON a.id = ap.attendee_id
        WHERE a.id = ?
    ''', (attendee_id,)).fetchone()
    db.close()
    if not attendee:
        return render_template('attendee.html', attendee=None, error="Attendee not found")
    return render_template('attendee.html', attendee=attendee, error=None)

@app.template_filter('date_format')
def date_format(value):
    """Format date for display"""
    if not value:
        return ''
    try:
        # Parse the date string and format it
        dt = datetime.strptime(value, '%d %b %Y')
        return dt.strftime('%B %d, %Y')
    except:
        return value

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 
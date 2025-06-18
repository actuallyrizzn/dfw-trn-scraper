#!/usr/bin/env python3
import sqlite3

conn = sqlite3.connect('attendees.db')
c = conn.cursor()
c.execute('SELECT id, event_name, event_date, total_attendees FROM events LIMIT 20')
events = c.fetchall()
print('All events (up to 20):')
for e in events:
    print(f'  ID: {e[0]}, Name: {e[1]}, Date: {e[2]}, Attendees: {e[3]}')
conn.close() 
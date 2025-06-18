#!/usr/bin/env python3
import sqlite3

conn = sqlite3.connect('attendees.db')
c = conn.cursor()
c.execute('''SELECT id, attendee_id, company, job_title, email, phone FROM attendee_profiles WHERE company IS NOT NULL OR job_title IS NOT NULL OR email IS NOT NULL OR phone IS NOT NULL LIMIT 10''')
rows = c.fetchall()
print('Sample attendee_profiles with real data:')
for row in rows:
    print(row)
conn.close() 
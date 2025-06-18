#!/usr/bin/env python3
import sqlite3

def check_database():
    try:
        conn = sqlite3.connect('attendees.db')
        cursor = conn.cursor()
        
        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        print(f"Tables: {tables}")
        
        # Check schema for each table
        for table in tables:
            cursor.execute(f"PRAGMA table_info({table})")
            columns = cursor.fetchall()
            print(f"\n{table} schema:")
            for col in columns:
                print(f"  {col[1]} ({col[2]})")
        
        # Check counts
        print(f"\nRecord counts:")
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"{table}: {count} records")
        
        # Check sample data with column names
        if 'attendees' in tables:
            cursor.execute("SELECT * FROM attendees LIMIT 2")
            attendees = cursor.fetchall()
            cursor.execute("PRAGMA table_info(attendees)")
            attendee_cols = [col[1] for col in cursor.fetchall()]
            print(f"\nSample attendees:")
            for attendee in attendees:
                for i, col in enumerate(attendee_cols):
                    print(f"  {col}: {attendee[i]}")
                print()
        
        if 'attendee_profiles' in tables:
            cursor.execute("SELECT * FROM attendee_profiles LIMIT 2")
            profiles = cursor.fetchall()
            cursor.execute("PRAGMA table_info(attendee_profiles)")
            profile_cols = [col[1] for col in cursor.fetchall()]
            print(f"\nSample profiles:")
            for profile in profiles:
                for i, col in enumerate(profile_cols):
                    print(f"  {col}: {profile[i]}")
                print()
        
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_database() 
import sqlite3
import logging
import os

def load_to_sqlite(data, db_path="data/warehouse.db"):
    """
    Phase 5: Validated data into a Relational Database.
    """
    if not data:
        logging.warning("No data provided to load into SQLite.")
        return

    try:
        # Connect to SQLite (creates the file if it doesn't exist)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 1. Create Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                name TEXT,
                email TEXT,
                city TEXT,
                zipcode TEXT,
                company_name TEXT,
                processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 2. Insert Data (using parameterized queries to prevent SQL injection)
        query = '''
            INSERT OR REPLACE INTO users (user_id, name, email, city, zipcode, company_name)
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        
        # Prepare data for bulk insertion (tuples)
        records_to_insert = [
            (r['user_id'], r['name'], r['email'], r['city'], r['zipcode'], r['company_name'])
            for r in data
        ]

        cursor.executemany(query, records_to_insert)
        conn.commit()
        logging.info(f"Successfully loaded {len(records_to_insert)} records into {db_path}.")

    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

def run_insights(db_path="data/warehouse.db"):
    """
    Phase 6: Run SQL queries to generate business insights.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        print("\n--- Business Insights ---")

        # Insight 1: Count users per city
        print("\n[Users per City]")
        cursor.execute("SELECT city, COUNT(*) FROM users GROUP BY city ORDER BY COUNT(*) DESC")
        for row in cursor.fetchall():
            print(f"{row[0]}: {row[1]}")

        # Insight 2: Find users with .net or .org emails (Technical domain check)
        print("\n[Users with .net or .org Emails]")
        cursor.execute("SELECT name, email FROM users WHERE email LIKE '%.net' OR email LIKE '%.org'")
        for row in cursor.fetchall():
            print(f"{row[0]} ({row[1]})")

    except sqlite3.Error as e:
        logging.error(f"Insight query failed: {e}")
    finally:
        if conn:
            conn.close()
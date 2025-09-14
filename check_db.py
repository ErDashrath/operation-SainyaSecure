import sqlite3

def check_database():
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    print("Existing tables:", tables)
    
    # Check each table structure if they exist
    for table in tables:
        if not table.startswith('sqlite_'):
            cursor.execute(f"PRAGMA table_info({table})")
            columns = cursor.fetchall()
            print(f"\nTable: {table}")
            for col in columns:
                print(f"  {col[1]} ({col[2]})")
            
            # Count rows
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"  Rows: {count}")
    
    conn.close()

if __name__ == "__main__":
    check_database()
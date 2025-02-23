import sqlite3

DATABASE = "census_data.db"

def init_db():
    """Initialize the database and create the table."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS census_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                year INTEGER NOT NULL,
                state TEXT NOT NULL,
                county TEXT NOT NULL,
                tract TEXT NOT NULL,
                population INTEGER NOT NULL
            );
        """)
        conn.commit()

if __name__ == '__main__':
    init_db()
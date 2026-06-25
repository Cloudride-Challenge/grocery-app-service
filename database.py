import os
import psycopg2

# שליפת פרטי ה-DB ממשתני סביבה (שה-ECS יזריק לקונטיינר)
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "grocery_db")
DB_USER = os.getenv("DB_USER", "grocery_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")

def get_db_connection():
    """מייצר חיבור חדש לבסיס הנתונים"""
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

def init_db():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS grocery_items (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL
            );
        """)
        conn.commit()
        cur.close()
        conn.close()
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Database initialization failed: {e}")

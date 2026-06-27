import psycopg2

class GroceryStorage:
    def __init__(self, table_name: str, db_host: str, db_name: str, db_user: str, db_password: str):
        self.table_name = table_name
        self.db_host = db_host 
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password

    def _get_connection(self):
        return psycopg2.connect(
            host=self.db_host,
            database=self.db_name,
            user=self.db_user,
            password=self.db_password
        )

    def init_db(self):
        try:
            conn = self._get_connection()
            cur = conn.cursor()
            cur.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.table_name} (
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

    def get_all_items(self) -> list:
        conn = self._get_connection()
        cur = conn.cursor()
        cur.execute(f"SELECT name FROM {self.table_name};")
        items = [row[0] for row in cur.fetchall()] # row[0] שולף רק את הטקסט הנקי
        cur.close()
        conn.close()
        return items

    def add_item(self, item_name: str) -> None:
        conn = self._get_connection()
        cur = conn.cursor()
        cur.execute(f"INSERT INTO {self.table_name} (name) VALUES (%s);", (item_name,))
        conn.commit()
        cur.close()
        conn.close()

import sqlite3

def create_connection(db_file):
    """Creates a connection to the SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def create_table(conn, create_table_sql):
    """Creates a table in the database."""
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Exception as e:
        print(f"Error creating table: {e}")

def insert_url(conn, url):
    """Inserts a new URL into the database."""
    sql = ''' INSERT INTO urls(original_url) VALUES(?) '''
    cur = conn.cursor()
    cur.execute(sql, (url,))
    conn.commit()
    return cur.lastrowid

def get_short_url(conn, short_code):
    """Retrieves the original URL based on the short code."""
    sql = ''' SELECT original_url FROM urls WHERE short_code = ? '''
    cur = conn.cursor()
    cur.execute(sql, (short_code,))
    row = cur.fetchone()
    if row:
        return row[0]
    else:
        return None

def close_connection(conn):
    """Closes the database connection."""
    if conn:
        conn.close()

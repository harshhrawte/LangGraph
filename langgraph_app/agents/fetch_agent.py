from ..utils.db import get_db_connection

def fetch_customer_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customer_data_cleaned LIMIT 50;")  # scope can vary
    rows = cursor.fetchall()
    colnames = [desc[0] for desc in cursor.description]
    conn.close()
    return [dict(zip(colnames, row)) for row in rows]

import sqlite3

def build_db():
    conn = sqlite3.connect("image_db.db")
    c = conn.cursor()
    # Create table
    c.execute('''CREATE TABLE image_db
                 (common_name text, image_link text)''')
    conn.close()
    return 0

build_db()
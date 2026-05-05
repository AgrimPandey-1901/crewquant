from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT"),
    sslmode="require"
)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS reports (
    id SERIAL PRIMARY KEY,
    job_id VARCHAR(50) NOT NULL,
    blob_url VARCHAR NOT NULL,
    summary VARCHAR NOT NULL,  
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")
cur.execute("SELECT * FROM reports LIMIT 1;")
print(cur.fetchall())

conn.commit()
print("✅ Table created!")

cur.close()
conn.close()
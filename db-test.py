import mariadb
import sys

try:
    conn = mariadb.connect(
        user="admin",
        password="K03cmErgBSz07mMfhDs6",
        host="db-warrants.c58gq2a6gh56.ap-southeast-1.rds.amazonaws.com",
        port=3306,
        database="ccass"
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

print("Connected to MariaDB!")
# Get Cursor
cur = conn.cursor()
cur.execute("INSERT INTO ccass_summary (created_date, ticker, shareholding, percentage) VALUES ('2025-04-15', '9988', '123123', '0.25');")
conn.commit()

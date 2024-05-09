import sqlite3

# Connect to your SQLite database
conn = sqlite3.connect("election.db")
cursor = conn.cursor()

# Update the values
cursor.execute(
    """
    UPDATE analysis_datas
    SET Percentage_of_B = REPLACE(Percentage_of_B, ',', '.')
    WHERE Percentage_of_B LIKE '%,%';
"""
)

# Commit the changes and close the connection
conn.commit()
conn.close()

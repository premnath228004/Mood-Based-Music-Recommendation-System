import sqlite3

# Connect to the database
conn = sqlite3.connect('music.db')
cursor = conn.cursor()

# Get total count of songs
cursor.execute('SELECT COUNT(*) FROM songs')
total_count = cursor.fetchone()[0]
print(f'Total songs in database: {total_count}')

# Get count of Indian songs
cursor.execute("SELECT COUNT(*) FROM songs WHERE nationality='Indian'")
indian_count = cursor.fetchone()[0]
print(f'Indian songs in database: {indian_count}')

# Get count by nationality
cursor.execute('SELECT nationality, COUNT(*) FROM songs GROUP BY nationality')
results = cursor.fetchall()
print('\nSongs by nationality:')
for nationality, count in results:
    print(f'  {nationality}: {count} songs')

# Close the connection
conn.close()
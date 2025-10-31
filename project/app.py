from flask import Flask, jsonify, request, render_template
import sqlite3
import os
import requests
import hashlib

app = Flask(__name__)

# Last.fm API configuration
LAST_FM_API_KEY = "YOUR_LAST_FM_API_KEY"  # You would need to get a real API key from https://www.last.fm/api
LAST_FM_API_URL = "http://ws.audioscrobbler.com/2.0/"

# Initialize the database
def init_db():
    conn = sqlite3.connect('music.db')
    cursor = conn.cursor()
    
    # Create songs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            artist TEXT NOT NULL,
            genre TEXT NOT NULL,
            nationality TEXT NOT NULL,
            mood TEXT NOT NULL
        )
    ''')
    
    # Check if table is empty, then insert sample data
    cursor.execute('SELECT COUNT(*) FROM songs')
    if cursor.fetchone()[0] == 0:
        sample_songs = [
            # Existing English songs
            ("Happy", "Pharrell Williams", "Pop", "American", "happy"),
            ("Can't Stop the Feeling", "Justin Timberlake", "Pop", "American", "happy"),
            ("Uptown Funk", "Mark Ronson ft. Bruno Mars", "Funk", "American", "happy"),
            ("Someone Like You", "Adele", "Pop", "British", "sad"),
            ("Stay With Me", "Sam Smith", "Soul", "British", "sad"),
            ("All I Want", "Kodaline", "Indie", "Irish", "sad"),
            ("Thunder", "Imagine Dragons", "Rock", "American", "energetic"),
            ("Shut Up and Dance", "Walk the Moon", "Rock", "American", "energetic"),
            ("Shake It Off", "Taylor Swift", "Pop", "American", "energetic"),
            ("Weightless", "Marconi Union", "Ambient", "British", "calm"),
            ("Clair de Lune", "Claude Debussy", "Classical", "French", "calm"),
            ("River Flows in You", "Yiruma", "Piano", "Korean", "calm"),
            ("Perfect", "Ed Sheeran", "Pop", "British", "romantic"),
            ("All of Me", "John Legend", "R&B", "American", "romantic"),
            ("La Vie En Rose", "Édith Piaf", "Chanson", "French", "romantic"),
            
            # Hindi Songs
            ("Tum Hi Ho", "Arijit Singh", "Romantic", "Indian", "romantic"),
            ("Kal Ho Naa Ho", "Sonu Nigam", "Romantic", "Indian", "sad"),
            ("Chaiyya Chaiyya", "Sukhwinder Singh", "Dance", "Indian", "energetic"),
            ("Jai Ho", "A.R. Rahman", "Dance", "Indian", "energetic"),
            ("Kabira", "Tochi Raina", "Spiritual", "Indian", "calm"),
            ("Gerua", "Arijit Singh", "Romantic", "Indian", "romantic"),
            ("Senorita", "Vishal-Shekhar", "Romantic", "Indian", "romantic"),
            ("Ae Dil Hai Mushkil", "Arijit Singh", "Romantic", "Indian", "sad"),
            ("Bekhayali", "Sachet Tandon", "Emotional", "Indian", "sad"),
            ("Ghungroo", "Arijit Singh", "Dance", "Indian", "energetic"),
            ("Mere Sapno Ki Rani", "Kumar Sanu", "Romantic", "Indian", "romantic"),
            ("Yeh Jo Des Hai Tera", "Swaroop Khan", "Patriotic", "Indian", "energetic"),
            ("Ae Watan", "Arijit Singh", "Patriotic", "Indian", "energetic"),
            ("Tum Tak", "Arijit Singh", "Romantic", "Indian", "romantic"),
            ("Raabta", "Arijit Singh", "Romantic", "Indian", "romantic"),
            ("Channa Mereya", "Arijit Singh", "Romantic", "Indian", "sad"),
            ("Kar Gayi Chull", "Badshah", "Party", "Indian", "energetic"),
            ("Swag Se Swagat", "Vishal-Shekhar", "Party", "Indian", "energetic"),
            ("Morni Banke", "Guru Randhawa", "Party", "Indian", "energetic"),
            ("Nashe Si Chadh Gayi", "Arijit Singh", "Romantic", "Indian", "happy"),
            ("Balam Pichkari", "Vishal-Shekhar", "Party", "Indian", "happy"),
            ("Malhari", "Vishal-Shekhar", "Dance", "Indian", "energetic"),
            ("Deewani Mastani", "Shreya Ghoshal", "Romantic", "Indian", "romantic"),
            ("Ghar More Pardesiya", "Shreya Ghoshal", "Classical", "Indian", "romantic"),
            ("Khairiyat", "Arijit Singh", "Romantic", "Indian", "happy"),
            
            # More Hindi Songs
            ("Kala Chashma", "Neha Kakkar", "Party", "Indian", "happy"),
            ("Aankh Marey", "Neha Kakkar", "Party", "Indian", "happy"),
            ("Gali Ke Sapne", "Shankar Mahadevan", "Emotional", "Indian", "sad"),
            ("Tum Hi Aana", "Jubin Nautiyal", "Romantic", "Indian", "romantic"),
            ("Dil Diyan Gallan", "Atif Aslam", "Romantic", "Indian", "romantic"),
            ("Mere Liye Tum Kaafi Ho", "Ayushmann Khurrana", "Romantic", "Indian", "romantic"),
            ("Tera Yaar Hoon Main", "Arijit Singh", "Friendship", "Indian", "happy"),
            ("Pal Pal Dil Ke Paas", "KK", "Romantic", "Indian", "romantic"),
            ("Tum Se Hi", "Mohit Chauhan", "Romantic", "Indian", "romantic"),
            ("Rabba", "Shankar Mahadevan", "Emotional", "Indian", "sad"),
            ("Phir Bhi Tumko Chaahunga", "Arijit Singh", "Romantic", "Indian", "romantic"),
            ("Tujhe Kitna Chahne Lage", "Arijit Singh", "Romantic", "Indian", "sad"),
            ("Ve Maahi", "Arijit Singh", "Romantic", "Indian", "romantic"),
            ("Sooraj Dooba Hain", "Arijit Singh", "Romantic", "Indian", "romantic"),
            ("Sunny Sunny", "Yo Yo Honey Singh", "Party", "Indian", "happy"),
            ("Blue Eyes", "Yo Yo Honey Singh", "Party", "Indian", "happy"),
            ("Lahore", "Guru Randhawa", "Party", "Indian", "happy"),
            ("Ishq Tera Tadpaave", "Rahat Fateh Ali Khan", "Romantic", "Indian", "romantic"),
            ("Tere Naam", "Udit Narayan", "Romantic", "Indian", "romantic"),
            ("Mere Mehboob Qayamat Hogi", "Mohammed Rafi", "Romantic", "Indian", "romantic"),
            ("Ae Mere Watan Ke Logo", "Lata Mangeshkar", "Patriotic", "Indian", "energetic"),
            ("Vande Mataram", "Lata Mangeshkar", "Patriotic", "Indian", "energetic"),
            ("Sandese Aate Hai", "Suresh Wadkar", "Patriotic", "Indian", "sad"),
            ("Dil Ibadat", "K.K.", "Romantic", "Indian", "romantic"),
            ("Tum Mile", "Javed Ali", "Romantic", "Indian", "romantic"),
            
            # Punjabi Songs
            ("Morni Banke", "Guru Randhawa", "Party", "Indian", "happy"),
            ("Lahore", "Guru Randhawa", "Party", "Indian", "happy"),
            ("Patola", "Guru Randhawa", "Party", "Indian", "happy"),
            ("High Rated Gabru", "Guru Randhawa", "Party", "Indian", "energetic"),
            ("Ishq Tera Tadpaave", "Rahat Fateh Ali Khan", "Romantic", "Indian", "romantic"),
            ("Laung Laachi", "Mannat Noor", "Romantic", "Indian", "romantic"),
            ("Sargi", "Akhil", "Romantic", "Indian", "romantic"),
            ("Suit", "Guru Randhawa", "Party", "Indian", "happy"),
            ("Blackia", "Karan Aujla", "Emotional", "Indian", "sad"),
            ("5 Taara", "Diljit Dosanjh", "Romantic", "Indian", "romantic"),
            ("Eyes On You", "Diljit Dosanjh", "Romantic", "Indian", "romantic"),
            ("Jind Mahi", "Diljit Dosanjh", "Party", "Indian", "happy"),
            ("Proper Patola", "Badshah", "Party", "Indian", "energetic"),
            ("Bad Boy", "Vishal Dadlani", "Party", "Indian", "energetic"),
            ("Aankh Marey", "Neha Kakkar", "Party", "Indian", "happy"),
            ("Chogada", "Darshan Raval", "Romantic", "Indian", "romantic"),
            ("Nazar Na Lag Jaaye", "Payal Dev", "Romantic", "Indian", "romantic"),
            ("Dilbar", "Neha Kakkar", "Party", "Indian", "happy"),
            ("Kamariya", "Sanju Sharma", "Party", "Indian", "happy"),
            ("Nainowale Ne", "Arijit Singh", "Romantic", "Indian", "romantic"),
            ("Genda Phool", "Badshah", "Party", "Indian", "happy"),
            ("Taaron Ke Shehar", "Akhil", "Romantic", "Indian", "romantic"),
            ("Kala Chashma", "Neha Kakkar", "Party", "Indian", "happy"),
            ("Sunny Sunny", "Yo Yo Honey Singh", "Party", "Indian", "happy"),
            ("Blue Eyes", "Yo Yo Honey Singh", "Party", "Indian", "happy"),
            
            # More Punjabi Songs
            ("Desi Kalakaar", "Yo Yo Honey Singh", "Party", "Indian", "energetic"),
            ("Love Dose", "Yo Yo Honey Singh", "Party", "Indian", "happy"),
            ("Dope Shope", "Yo Yo Honey Singh", "Party", "Indian", "happy"),
            ("White Brown Black", "Karan Aujla", "Emotional", "Indian", "sad"),
            ("Tochan", "Karan Aujla", "Emotional", "Indian", "sad"),
            ("Same Beef", "Bohemia", "Hip Hop", "Indian", "energetic"),
            ("295", "Sidhu Moose Wala", "Hip Hop", "Indian", "energetic"),
            ("Old Skool", "Sidhu Moose Wala", "Hip Hop", "Indian", "energetic"),
            ("Legend", "Sidhu Moose Wala", "Hip Hop", "Indian", "energetic"),
            ("So High", "Sidhu Moose Wala", "Hip Hop", "Indian", "romantic"),
            ("Brown Munde", "AP Dhillon", "Hip Hop", "Indian", "happy"),
            ("Excuses", "AP Dhillon", "Hip Hop", "Indian", "sad"),
            ("Summer High", "AP Dhillon", "Hip Hop", "Indian", "romantic"),
            ("Without You", "AP Dhillon", "Hip Hop", "Indian", "sad"),
            ("Peaches", "AP Dhillon", "Hip Hop", "Indian", "happy"),
            ("Butterfly", "Super Singh", "Party", "Indian", "happy"),
            ("52 Bars", "Karan Aujla", "Hip Hop", "Indian", "energetic"),
            ("Headshot", "Karan Aujla", "Hip Hop", "Indian", "energetic"),
            ("Prada", "Jass Manak", "Party", "Indian", "happy"),
            ("Yaar Mod Do", "Jass Manak", "Party", "Indian", "happy"),
            ("Jaana Ve", "Jass Manak", "Romantic", "Indian", "romantic"),
            ("Dhaka", "Jass Manak", "Party", "Indian", "happy"),
            ("Barsaat", "Arjan Dhillon", "Romantic", "Indian", "romantic"),
            ("Kinnari", "Arjan Dhillon", "Romantic", "Indian", "romantic"),
            ("Style", "Arjan Dhillon", "Party", "Indian", "happy"),
            
            # Additional Hindi/Punjabi Songs
            ("Tere Hawaale", "Arijit Singh", "Emotional", "Indian", "sad"),
            ("Kesariya", "Arijit Singh", "Romantic", "Indian", "romantic"),
            ("Raatan Lambiyan", "Jubin Nautiyal", "Romantic", "Indian", "romantic"),
            ("Doobey", "Nakash Aziz", "Emotional", "Indian", "sad"),
            ("Param Sundari", "A.R. Rahman", "Dance", "Indian", "energetic"),
            ("Ghungroo", "Arijit Singh", "Dance", "Indian", "energetic"),
            ("Namo Namo", "Amit Trivedi", "Devotional", "Indian", "calm"),
            ("Om Shanti Om", "Vishal-Shekhar", "Dance", "Indian", "energetic"),
            ("Malang", "Vishal-Shekhar", "Dance", "Indian", "energetic"),
            ("Agar Tum Saath Ho", "Arijit Singh", "Romantic", "Indian", "sad"),
            ("Tum Hi Ho", "Arijit Singh", "Romantic", "Indian", "romantic"),
            ("Hamari Adhuri Kahani", "Arijit Singh", "Romantic", "Indian", "sad"),
            ("Janam Janam", "Arijit Singh", "Romantic", "Indian", "romantic"),
            ("Saiyaan", "KK", "Romantic", "Indian", "romantic"),
            ("Tum Se Hi", "Mohit Chauhan", "Romantic", "Indian", "romantic"),
            ("Abhi Toh Party Shuru Hui Hai", "Badshah", "Party", "Indian", "happy"),
            ("Saturday Saturday", "Imran Khan", "Party", "Indian", "happy"),
            ("Bom Diggy Diggy", "Zack Knight", "Party", "Indian", "happy"),
            ("Guru Randhawa", "Lahore", "Party", "Indian", "happy"),
            ("Dil Chori", "Yo Yo Honey Singh", "Party", "Indian", "happy")
        ]
        
        cursor.executemany('''
            INSERT INTO songs (name, artist, genre, nationality, mood)
            VALUES (?, ?, ?, ?, ?)
        ''', sample_songs)
    
    conn.commit()
    conn.close()

# Function to get artist image from Last.fm
def get_artist_image(artist_name):
    try:
        # For demo purposes, we'll return a placeholder image
        # In a real implementation, you would use the Last.fm API
        # This is a placeholder that generates a colored image based on the artist name
        return f"https://ui-avatars.com/api/?name={artist_name}&background=random&size=128"
    except Exception as e:
        print(f"Error fetching image for {artist_name}: {e}")
        # Return a default placeholder
        return "https://via.placeholder.com/128x128.png?text=?"

# Get songs by mood
def get_songs_by_mood(mood):
    conn = sqlite3.connect('music.db')
    cursor = conn.cursor()
    
    # Query for songs matching the mood or genre
    cursor.execute('''
        SELECT id, name, artist, genre, nationality, mood
        FROM songs
        WHERE mood LIKE ? OR genre LIKE ?
    ''', (f'%{mood}%', f'%{mood}%'))
    
    songs = cursor.fetchall()
    conn.close()
    
    # Convert to list of dictionaries and add image URLs
    song_list = []
    for song in songs:
        song_dict = {
            'id': song[0],
            'name': song[1],
            'artist': song[2],
            'genre': song[3],
            'nationality': song[4],
            'mood': song[5],
            'image': get_artist_image(song[2])  # Add image URL
        }
        song_list.append(song_dict)
    
    return song_list

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# API route for getting recommendations
@app.route('/recommendations')
def recommendations():
    mood = request.args.get('mood', '').lower()
    if not mood:
        return jsonify({'error': 'Mood parameter is required'}), 400
    
    songs = get_songs_by_mood(mood)
    return jsonify(songs)

# API route for getting all songs (for testing)
@app.route('/songs')
def all_songs():
    conn = sqlite3.connect('music.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, artist, genre, nationality, mood FROM songs')
    songs = cursor.fetchall()
    conn.close()
    
    song_list = []
    for song in songs:
        song_dict = {
            'id': song[0],
            'name': song[1],
            'artist': song[2],
            'genre': song[3],
            'nationality': song[4],
            'mood': song[5],
            'image': get_artist_image(song[2])  # Add image URL
        }
        song_list.append(song_dict)
    
    return jsonify(song_list)

if __name__ == '__main__':
    # Initialize the database
    init_db()
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)
z# Mood-Based Music Recommendation System

## 🎯 Objective
The main objective of this project is to design and develop a Mood-Based Music Recommendation System that recommends songs according to the user's mood. The system analyzes user input in the form of emojis or text descriptions and displays suitable songs from the database.

## 🧠 Project Description
Music is deeply connected to human emotions. This project creates an intelligent and interactive system that recommends songs based on the user's current mood. The front end is developed using HTML, CSS, and JavaScript to provide a visually appealing and user-friendly interface.

Users can either:
- Select an emoji representing their mood
- Type a word describing how they feel (e.g., "happy", "sad", "calm")

The input is sent to the backend, where Python acts as the bridge between the front end and the SQL database. The database stores detailed information about each song, including:
- Song ID
- Song Name
- Artist Name
- Genre
- Artist Nationality
- Mood Tag

Based on the detected mood, Python queries the SQL database to fetch songs with matching mood or genre tags and displays them on the web interface dynamically.

## ⚙️ Technologies Used
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python (Flask)
- **Database**: SQLite
- **Connectivity**: sqlite3 library

## 🧩 Key Features
- Interactive mood selection using emojis or text input
- Dynamic music recommendation based on mood analysis
- Clean, responsive, and modern front-end design
- Real-time backend connection with SQL database through Python
- Categorization of songs by mood, genre, artist, and nationality

## 🚀 Setup Instructions

1. **Install Python** (if not already installed)
   - Download from [python.org](https://www.python.org/downloads/)

2. **Clone or download this repository**

3. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Access the application**:
   Open your browser and go to `http://localhost:5000`

## 📁 Project Structure
```
mood-music-recommender/
│
├── app.py              # Flask backend application
├── music.db            # SQLite database (created automatically)
├── requirements.txt    # Python dependencies
├── README.md           # This file
├── index.html          # Main HTML file
├── styles.css          # Styling
└── script.js           # Frontend JavaScript
```

## 🌈 Expected Outcome
By the end of this project, users will experience a personalized and emotion-aware music recommendation platform, where music suggestions feel intuitive and human-like. It demonstrates the connection between data, design, and emotion — blending creativity with computer science.

## 🤝 Contributing
Feel free to fork this project and submit pull requests. Any contributions are welcome!

## 📄 License
This project is open source and available under the MIT License.
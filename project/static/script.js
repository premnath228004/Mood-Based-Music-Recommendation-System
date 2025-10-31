// Get DOM elements
const moodButtons = document.querySelectorAll('.mood-btn');
const moodInput = document.getElementById('mood-input');
const submitButton = document.getElementById('submit-mood');
const songList = document.getElementById('song-list');

// Add event listeners to mood buttons
moodButtons.forEach(button => {
    button.addEventListener('click', () => {
        const mood = button.getAttribute('data-mood');
        getRecommendations(mood);
    });
});

// Add event listener to submit button
submitButton.addEventListener('click', () => {
    const mood = moodInput.value.trim().toLowerCase();
    if (mood) {
        getRecommendations(mood);
    } else {
        alert('Please enter your mood!');
    }
});

// Function to get recommendations from the backend
async function getRecommendations(mood) {
    try {
        // Show loading state
        songList.innerHTML = '<p class="placeholder">Loading recommendations...</p>';
        
        // Call the backend API
        const response = await fetch(`/recommendations?mood=${encodeURIComponent(mood)}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const songs = await response.json();
        displayRecommendations(songs);
    } catch (error) {
        console.error('Error fetching recommendations:', error);
        songList.innerHTML = '<p class="placeholder">Error loading recommendations. Please try again.</p>';
    }
}

// Function to display recommendations
function displayRecommendations(songs) {
    if (songs.length === 0) {
        songList.innerHTML = '<p class="placeholder">No songs found for this mood. Try another mood!</p>';
        return;
    }
    
    songList.innerHTML = '';
    
    songs.forEach(song => {
        // Create song card element
        const songCard = document.createElement('div');
        songCard.className = 'song-card';
        
        // Create the song header with artist photo
        const songHeader = document.createElement('div');
        songHeader.className = 'song-header';
        
        // Create artist photo element
        const artistPhoto = document.createElement('img');
        artistPhoto.className = 'artist-photo';
        artistPhoto.src = song.image;
        artistPhoto.alt = `${song.artist} photo`;
        artistPhoto.onerror = function() {
            // If the image fails to load, show a placeholder with the first letter
            this.onerror = null;
            this.src = `https://ui-avatars.com/api/?name=${song.artist}&background=random&size=128`;
        };
        
        // Create song info container
        const songInfo = document.createElement('div');
        songInfo.className = 'song-info';
        
        // Create song title element
        const songTitle = document.createElement('div');
        songTitle.className = 'song-title';
        songTitle.textContent = song.name;
        
        // Create song artist element
        const songArtist = document.createElement('div');
        songArtist.className = 'song-artist';
        songArtist.textContent = `by ${song.artist}`;
        
        // Append title and artist to song info
        songInfo.appendChild(songTitle);
        songInfo.appendChild(songArtist);
        
        // Append photo and info to header
        songHeader.appendChild(artistPhoto);
        songHeader.appendChild(songInfo);
        
        // Create song tags container
        const songTags = document.createElement('div');
        songTags.className = 'song-tags';
        
        // Create genre tag
        const songGenre = document.createElement('span');
        songGenre.className = 'song-genre';
        songGenre.textContent = song.genre;
        
        // Create nationality tag
        const songNationality = document.createElement('span');
        songNationality.className = 'song-nationality';
        songNationality.textContent = song.nationality;
        
        // Create mood tag
        const songMood = document.createElement('span');
        songMood.className = 'song-mood';
        songMood.textContent = song.mood;
        
        // Append tags to tags container
        songTags.appendChild(songGenre);
        songTags.appendChild(songNationality);
        songTags.appendChild(songMood);
        
        // Append header and tags to song card
        songCard.appendChild(songHeader);
        songCard.appendChild(songTags);
        
        // Append song card to song list
        songList.appendChild(songCard);
    });
}
// Search functionality
async function searchSongs() {
    const query = document.getElementById("searchQuery").value;
    const type = document.getElementById("searchType").value;
    const resultsDiv = document.getElementById("results");

    if (!query) {
        resultsDiv.innerHTML = "Please enter a song ID or song name.";
        return;
    }

    try {
        const response = await fetch(`/search?query=${query}&type=${type}`);
        const data = await response.json();

        if (data.results && data.results.length > 0) {
            let resultsHTML = "<h3>Search Results:</h3>";
            const searchResults = []; // Array to store the songs for the player

            data.results.forEach(song => {
                resultsHTML += `<div class="song">
                                    <strong>Song ID:</strong> ${song.song_id}<br>
                                    <strong>Song Name:</strong> ${song.song_name}<br>
                                    <strong>Similarity Score:</strong> ${song.similarity_score}<br>
                                    <strong>Src:</strong> ${song.url}<br>
                                </div>`;
                searchResults.push({ title: song.song_name, url: song.url });
            });

            resultsDiv.innerHTML = resultsHTML;
            initializePlayer(searchResults); // Initialize player with search results

        } else {
            resultsDiv.innerHTML = "No results found.";
        }
    } catch (error) {
        resultsDiv.innerHTML = "Error fetching results.";
    }
}

// Music player functionality
let currentIndex = 0;
let currentSong = null;
let songs = []; // Store songs for playback

function initializePlayer(songList) {
    songs = songList; // Set songs to the search results
    currentIndex = 0;
    if (songs.length > 0) {
        playSong(currentIndex);
    }
}

// Function to play a song
function playSong(index) {
    if (currentSong) currentSong.unload(); // Stop the current song if any

    currentSong = new Howl({
        src: [songs[index].url],
        html5: true, // Ensures compatibility with larger files
        onend: function() {
            nextSong(); // Automatically play the next song when current one ends
        }
    });

    document.getElementById("current-song").innerText = `Current Song: ${songs[index].title}`;
    currentSong.play();
}

// Play, Pause, Previous, and Next functions
function togglePlayPause() {
    if (currentSong.playing()) {
        currentSong.pause();
    } else {
        currentSong.play();
    }
}

function nextSong() {
    currentIndex = (currentIndex + 1) % songs.length;
    playSong(currentIndex);
}

function prevSong() {
    currentIndex = (currentIndex - 1 + songs.length) % songs.length;
    playSong(currentIndex);
}

// Attach event listeners
document.getElementById("search-button").addEventListener("click", searchSongs);
document.getElementById("play").addEventListener("click", () => playSong(currentIndex));
document.getElementById("pause").addEventListener("click", togglePlayPause);
document.getElementById("next").addEventListener("click", nextSong);
document.getElementById("prev").addEventListener("click", prevSong);


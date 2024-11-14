from flask import Flask, render_template, request, jsonify, send_from_directory
import sys
import os
import random
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'search'))
from search import search_by_song_id, search_by_song_name

app = Flask(
    __name__,
    template_folder="../frontend/templates",  # Path to your templates folder
    static_folder="../frontend/static"        # Path to your static folder
)
# MP3_FOLDER = '../../data/processed_mp3'
MP3_FOLDER = '../../data/raw_mp3'

@app.route('/')
def index():
    return render_template('index.html')  # Serve the frontend HTML

@app.route('/mp3/<filename>')
def get_music(filename):
    return send_from_directory(MP3_FOLDER, filename)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    search_type = request.args.get('type', 'song_id')  # Default to 'song_id'
    
    # Validate input
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400
    
    # Perform search based on the type of search (song_id or song_name)
    if search_type == 'song_id':
        try:
            if query == 'random':
                files = os.listdir(MP3_FOLDER)
                query = random.sample(files, 1)[0][:-4]
                results = search_by_song_id(int(query), top_k=30)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    elif search_type == 'song_name':
        try:
            results = search_by_song_name(query, top_k=30)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Invalid search type. Use 'song_id' or 'song_name'"}), 400

    # Add URLs for each song to serve them from the backend
    for song in results:
        song['url'] = f"/mp3/{song['song_id']}.mp3"

    return jsonify({"results": results}), 200

if __name__ == '__main__':
    app.run(debug=True)


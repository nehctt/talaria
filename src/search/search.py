from qdrant_client import QdrantClient
from qdrant_client.http import models as qdrant_models
import numpy as np


def search_by_song_id(song_id, collection_name="song_embeddings", top_k=10):
    """
    Search for a song by its ID and return the top K similar songs.
    """
    # Connect to Qdrant service
    client = QdrantClient(host="localhost", port=6333)
    
    # Fetch the song's embedding based on the song_id
    result = client.retrieve(
        collection_name=collection_name,
        ids=[song_id],
        with_payload=True,
        with_vectors=True
    )
    
    if not result:
        print(f"Song with ID {song_id} not found.")
        return []
    
    song_embedding = result[0].vector  # Retrieve the embedding of the song by its ID

    # Perform the similarity search based on the song's embedding
    return search_similar_songs(song_embedding, collection_name, top_k)


def search_by_song_name(song_name, collection_name="song_embeddings", top_k=10):
    """
    Search for a song by its name and return the top K similar songs.
    """
    # Connect to Qdrant service
    client = QdrantClient(host="localhost", port=6333)
    
    # Perform a scroll query to find the song_name
    query = qdrant_models.Filter(
        must=[
            qdrant_models.FieldCondition(key="song_name", match=qdrant_models.MatchText(text=song_name))
        ]
    )

    # Initialize the scroll search
    scroll_response = client.scroll(
        collection_name=collection_name,
        scroll_filter=query,
        limit=1,
        with_payload=True,
        with_vectors=True
    )
    
    # Check if any results are found
    if not scroll_response[0]:
        print(f"Song with name '{song_name}' not found.")
        return []

    song_embedding = scroll_response[0][0].vector  # Retrieve the song's embedding

    # Perform the similarity search based on the song's embedding
    return search_similar_songs(song_embedding, collection_name, top_k)


def search_similar_songs(song_embedding, collection_name="song_embeddings", top_k=10):
    """
    Search for the top K most similar songs to the provided song embedding.
    """
    # Connect to Qdrant service
    client = QdrantClient(host="localhost", port=6333)

    # Perform the similarity search
    results = client.search(
        collection_name=collection_name,
        query_vector=song_embedding,
        limit=top_k,
        with_payload=True  # Include payload (song_name) in the result
    )

    # Print and return the results with song names
    similar_songs = []
    for result in results:
        song_name = result.payload.get("song_name", "Unknown Song")
        similar_songs.append({
            "song_id": result.id,
            "song_name": song_name,
            "similarity_score": result.score  # Cosine similarity score
        })
        print(f"Song ID: {result.id}, Song Name: {song_name}, Similarity Score: {result.score}")

    return similar_songs


if __name__ == "__main__":
    # Example: search by song ID
    song_id = 24110603094  # Replace with actual song_id
    print(f"search by id: {song_id}")
    similar_songs_by_id = search_by_song_id(song_id)

    # Example: search by song name
    song_name = "是非題"
    print(f"search by name: {song_name}")
    similar_songs_by_name = search_by_song_name(song_name)


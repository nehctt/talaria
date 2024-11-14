import os
import csv
from datetime import datetime

def process_songs(input_dir, output_dir, csv_path):
    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Create or open the CSV file and add headers if it doesn't exist
    if not os.path.exists(csv_path):
        with open(csv_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["song_id", "song_name"])

    # Set the date prefix for song_id based on today's date in YYMMDD format
    date_prefix = datetime.now().strftime("%y%m%d")
    
    # Determine starting index by reading existing entries in CSV
    current_index = 1
    if os.path.exists(csv_path):
        with open(csv_path, 'r') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)
            if len(rows) > 1:  # Skip header row
                last_id = rows[-1][0]
                current_index = int(last_id[6:]) + 1

    # Process each MP3 file in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith(".mp3"):
            song_name = filename[:-4]  # Remove .mp3
            song_id = f"{date_prefix}{str(current_index).zfill(5)}"  # Generate song_id
            new_filename = f"{song_id}.mp3"
            
            # Rename file to use song_id
            original_path = os.path.join(input_dir, filename)
            new_path = os.path.join(output_dir, new_filename)
            os.rename(original_path, new_path)
            print(f"Renamed '{filename}' to '{new_filename}'")

            # Append song_id and original song_name to the CSV file
            with open(csv_path, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([song_id, song_name])

            current_index += 1  # Increment for the next file

    print("Processing complete.")

# Paths
input_dir = "../../data/raw_mp3"        # Directory containing original MP3 files
output_dir = "../../data/raw_mp3" # Directory to save renamed MP3 files
csv_path = "../../data/song_id.csv" # CSV file to store song_id and song_name mapping

# Run the processing function
process_songs(input_dir, output_dir, csv_path)

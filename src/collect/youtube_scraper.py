import yt_dlp
import os
import argparse


def download_song(video_url, output_path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f"{output_path}/%(title)s.%(ext)s",
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=False)
        filename = f"{output_path}/{info_dict['title']}.mp3"

        if os.path.exists(filename):
            print(f"Skipping '{info_dict['title']}' (already downloaded)")
        else:
            print(f"Downloading '{info_dict['title']}'")
            ydl.download([video_url])
            print("Download complete.")


def download_playlist(playlist_url, output_path):
    def exists_hook(d):
        filename = f"{output_path}/{d['info_dict']['title']}.mp3"
        if os.path.exists(filename):
            print(f"Skipping {d['info_dict']['title']} (already downloaded)")
            return True  # Skip download if file exists

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f"{output_path}/%(title)s.%(ext)s",
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
		'ignoreerrors': True,
        'progress_hooks': [exists_hook],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlist_url])
        print("Playlist download complete.")

if __name__ == '__main__':
    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--video_url", type=str, help="URL of the YouTube video to download")
    parser.add_argument("--playlist_url", type=str, help="URL of the YouTube playlist to download")
    args = parser.parse_args()

    if args.video_url:
        download_song(args.video_url, "../../data/raw_mp3/")
    elif args.playlist_url:
        download_playlist(args.playlist_url, "../../data/raw_mp3/")

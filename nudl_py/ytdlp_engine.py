"""ytdlp_engine.py - Core yt-dlp downloader engine for video-based SNS."""

import os
import yt_dlp

# Define the target download folder
DOWNLOAD_DIR = "downloads"

def download_video(url: str):
    """
    Downloads media using yt-dlp core. 
    Saves the file into the downloads directory named after the content ID.
    """
    # Create the downloads directory if it doesn't exist yet
    if not os.path.exists(DOWNLOAD_DIR):
        print(f"    [Engine] Creating download directory: '{DOWNLOAD_DIR}/'...")
        os.makedirs(DOWNLOAD_DIR)

    print(f"    [Engine] Extracting stream data and initiating download...")
    
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        
        # This forces yt-dlp to save files as 'downloads/ID.ext'
        'outtmpl': os.path.join(DOWNLOAD_DIR, '%(id)s.%(ext)s'),
        
        'quiet': False,
        'no_warnings': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"    [Engine] Download completed successfully!")
        
    except yt_dlp.utils.DownloadError as de:
        print(f"    [!] [Engine] Download failed (Content might be private, deleted, or blocked): {de}")
    except Exception as e:
        print(f"    [!] [Engine] Unexpected error: {e}")
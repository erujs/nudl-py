"""ytdlp_engine.py - Core yt-dlp downloader engine for video-based SNS."""

import os
import yt_dlp

# Define the target download folder
DOWNLOAD_DIR = "downloads"

def download_video(url: str):
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)

    base_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(DOWNLOAD_DIR, '%(id)s.%(ext)s'),
        'quiet': False,
        'no_warnings': True,
    }

    for browser in ('firefox', 'brave'):
        ydl_opts = {**base_opts, 'cookiesfrombrowser': (browser,)}
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            print(f"    [Engine] Download completed successfully using {browser} cookies!")
            return
        except yt_dlp.utils.DownloadError as de:
            print(f"    [!] [Engine] {browser} cookies failed, trying next... ({de})")
            continue
        except Exception as e:
            print(f"    [!] [Engine] Unexpected error: {e}")
            return

    print("    [!] [Engine] All cookie sources failed.")
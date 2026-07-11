"""download_router.py - Directs URLs to their specific downloader engines."""

# Import our unified video engine
from .ytdlp_engine import download_video

def route_download(platform: str, url: str):
    """Matches the platform name and routes it to the proper script engine."""
    
    # Send all video-based platforms to our yt-dlp engine
    if platform in ["YT", "TT", "RD"]:
        download_video(url)
        
    elif platform in ["IG", "FB"]:
        # Saved as placeholders for when you integrate gallery-dl later
        print(f"    [Router] {platform} support is planned for a future update.")
        
    else:
        print(f"    [Router] Unknown platform error.")
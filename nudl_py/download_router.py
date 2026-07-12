"""download_router.py - Directs URLs to their specific downloader engines."""

from .ytdlp_engine import download_video

def route_download(platform: str, url: str):
    """Matches the platform name and routes it to the proper script engine."""
    u = url.lower()
    
    # Catch static photos/posts early across IG, FB, and Reddit
    if (platform == "IG" and "/p/" in u) or \
       (platform == "FB" and not any(x in u for x in ["/videos/", "/watch", "/reel", "fb.watch"])) or \
       (platform == "RD" and "i.redd.it" in u):
        print(f"    [Router] Skipping: Static photo/text posts are not supported for {platform}.")
        return

    # Route all validated video platforms to the engine
    if platform in ["YT", "TT", "RD", "IG", "FB"]:
        download_video(url)
    else:
        print(f"    [Router] Unknown platform error.")
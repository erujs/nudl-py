"""download_router.py - Directs URLs to their specific downloader engines."""

from .ytdlp_engine import download_video
from .platforms import SUPPORTED_PLATFORMS


def route_download(platform: str, url: str):
    """Matches the platform name and routes it to the proper script engine."""
    u = url.lower()
    plat = SUPPORTED_PLATFORMS.get(platform)

    if plat is None:
        print("    [Router] Unknown platform error.")
        return

    if plat.is_static_post and plat.is_static_post(u):
        print(f"    [Router] Skipping: Static photo/text posts are not supported for {platform}.")
        return

    download_video(url)
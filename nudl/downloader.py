import os
import subprocess
import requests
import sys
from urllib.parse import urlparse
from yt_dlp import YoutubeDL
from nudl.utils.extractors import extract_post_id

"""
Supported URL patterns and which downloader handles them:

───────────────────────────────────────────────
Instagram:
  /p/<post_id>  →  gallery-dl
    e.g. https://www.instagram.com/p/<post_id>?img_index=1
         https://www.instagram.com/p/<post_id>/
  /reel/<post_id>  →  yt-dlp
    e.g. https://www.instagram.com/reel/<post_id>/

───────────────────────────────────────────────
Facebook:
  /photo/?fbid=<post_id>  →  gallery-dl
    e.g. https://www.facebook.com/photo/?fbid=<post_id>
  /posts/<post_id>
    e.g. https://www.facebook.com/posts/<post_id>
  /watch?v=<post_id>  →  yt-dlp
    e.g. https://www.facebook.com/watch?v=<post_id>
  /reel/<post_id>  →  yt-dlp
    e.g. https://www.facebook.com/reel/<post_id>

───────────────────────────────────────────────
TikTok:
  /video/<post_id>  →  yt-dlp
    e.g. https://www.tiktok.com/@username/video/<post_id>

───────────────────────────────────────────────
YouTube:
  /watch?v=<post_id>  →  yt-dlp
    e.g. https://www.youtube.com/watch?v=<post_id>
  /shorts/<post_id>  →  yt-dlp
    e.g. https://www.youtube.com/shorts/<post_id>

───────────────────────────────────────────────
Reddit:
  /comments/<post_id>  →  gallery-dl
    e.g. https://www.reddit.com/r/<subreddit>/comments/<post_id>

───────────────────────────────────────────────
"""


def download_image(url: str, output_dir: str = "downloads"):
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()

        filename = os.path.basename(url.split("?")[0])
        filepath = os.path.join(output_dir, filename)

        with open(filepath, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)

        print(f"Downloaded image: {filepath}")
    except Exception as e:
        print(f"ERROR: Failed to download image from {url}: {e}", file=sys.stderr)


def download_with_yt_dlp(url: str, output_dir: str, cookies_dir: str):
    hostname = urlparse(url).netloc.lower()
    short_domain = hostname.replace("www.", "").split(".")[0]

    # yt-dlp base options
    # Uncomment the extra parameters to hide yt-dlp logging outputs
    ydl_opts = {
        "format": "best",
        "outtmpl": f"{output_dir}/%(id)s.%(ext)s",
        # "quiet": True,
        # "no_warnings": True, 
        "merge_output_format": "mp4",
        "addmetadata": True,
        "embedthumbnail": True,
        "allow_unplayable_formats": True,
    }

    cookies_path = os.path.join(cookies_dir, f"{short_domain}.txt")
    if os.path.exists(cookies_path):
        ydl_opts["cookiefile"] = cookies_path
    else:
        print(f"WARNING: No cookies found for {short_domain}. Proceeding without cookies.")
        print(f"If login is required, run: nudl-login {short_domain}")
        print(f"Expected cookies at: {cookies_path}")

    post_id = extract_post_id(url)

    # Run yt-dlp
    with YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=True)
            filepath = ydl.prepare_filename(info)
            print(f"File downloaded for {post_id}: {filepath}")
            print(f"yt-dlp finished downloading from {url}")

                
        except Exception as e:
            print(f"ERROR: yt-dlp failed to download from {url}: {e}", file=sys.stderr)


def download_with_gallery_dl(url: str, output_dir: str, cookies_dir: str):
    try:
        hostname = urlparse(url).netloc.lower()
        short_domain = hostname.replace("www.", "").split(".")[0]

        cookies_path = os.path.join(cookies_dir, f"{short_domain}.txt")
        if not os.path.exists(cookies_path):
            print(f"WARNING: No cookies found for {short_domain}. Skipping.")
            print(f"This URL likely requires login. Please run:")
            print(f"  nudl-login {short_domain}")
            print(f"Expected cookies at: {cookies_path}")
            return

        post_id = extract_post_id(url)
        post_dir = os.path.join(output_dir, post_id)
        os.makedirs(post_dir, exist_ok=True)

        # gallery-dl base options
        command = [
            sys.executable, "-m", "gallery_dl",
            f"--cookies={cookies_path}",
            "-d", post_dir,
            url,
        ]
        
        # Run gallery-dl
        # Uncomment the extra parameters to hide gallery-dl logging outputs
        subprocess.run(
            command, check=True,
            # stdout=subprocess.PIPE,
            # stderr=subprocess.DEVNULL
        )

        # Gather downloaded files (optimized: use os.scandir instead of glob)
        all_files = []
        for root, _, files in os.walk(post_dir):
            for file in files:
                all_files.append(os.path.join(root, file))
        
        file_count = len(all_files)
        
        print(f"Files downloaded for {post_id} ({file_count}):")
        for filepath in all_files:
            print(f"  {filepath}")

        # Rename only for Instagram and Reddit
        should_rename = "instagram" in hostname or "reddit" in hostname
        
        if should_rename and file_count > 0:
            if file_count == 1:
                old_path = all_files[0]
                ext = os.path.splitext(old_path)[1]
                new_path = os.path.join(os.path.dirname(old_path), f"{post_id}{ext}")
                os.rename(old_path, new_path)
                print(f"Renamed single file -> {post_id}{ext}")
            else:
                for i, old_path in enumerate(sorted(all_files), start=1):
                    ext = os.path.splitext(old_path)[1]
                    new_path = os.path.join(os.path.dirname(old_path), f"{i}_{post_id}{ext}")
                    os.rename(old_path, new_path)
                print(f"Renamed {file_count} files with index + post_id")
        elif not should_rename:
            print(f"Keeping original filenames")

        print(f"gallery-dl finished downloading from {url}")

    except Exception as e:
        print(f"ERROR: gallery-dl failed to download from {url}: {e}", file=sys.stderr)


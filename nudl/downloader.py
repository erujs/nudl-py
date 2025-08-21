import os
import re
import subprocess
import requests
from urllib.parse import urlparse
from yt_dlp import YoutubeDL


def get_cookies_path(short_domain: str, cookies_dir: str) -> str:
    """Return the cookie path inside the nudl-py-config/.nudl_cookies folder."""
    return os.path.join(cookies_dir, f"{short_domain}.txt")


def download_video(url: str, output_dir: str, cookies_dir: str):
    hostname = urlparse(url).netloc.lower()
    short_domain = hostname.replace("www.", "").split(".")[0]

    ydl_opts = {
        "format": "best",
        "outtmpl": f"{output_dir}/%(title).80s~%(id)s.%(ext)s",
        "merge_output_format": "mp4",
    }

    cookies_path = get_cookies_path(short_domain, cookies_dir)
    if os.path.exists(cookies_path):
        ydl_opts["cookiefile"] = cookies_path
    else:
        print(f"⚠️ No cookies found for {short_domain}. Proceeding without cookies.")
        print(f"👉 If login is required, run: nudl-login {short_domain}")
        print(f"(Expected cookies at: {cookies_path})\n")

    with YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=True)
            original_filename = ydl.prepare_filename(info)

            if "packaged-media.redd.it" in url:
                clean_filename = original_filename.split("?")[0]
                if clean_filename != original_filename:
                    os.rename(original_filename, clean_filename)
                    print(f"✅ Reddit video renamed to: {clean_filename}")
                else:
                    print(f"✅ Reddit video saved as: {original_filename}")
            else:
                print(f"✅ Downloaded: {original_filename}")
        except Exception as e:
            print(f"❌ Failed to download video from {url}: {e}")


def download_image(url: str, output_dir: str = "downloads"):
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()

        filename = os.path.basename(url.split("?")[0])
        filepath = os.path.join(output_dir, filename)

        with open(filepath, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)

        print(f"🖼️ Downloaded image: {filepath}")
    except Exception as e:
        print(f"❌ Failed to download image from {url}: {e}")


def extract_code_from_url(url: str) -> str:
    match = re.search(r"/(?:p|reel|photo|video)/([a-zA-Z0-9_-]+)", url)
    if not match:
        path = urlparse(url).path.strip("/").split("/")
        return path[-1] if path else "media"
    return match.group(1)


def download_with_gallery_dl(url: str, output_dir: str, cookies_dir: str):
    try:
        hostname = urlparse(url).netloc.lower()
        short_domain = hostname.replace("www.", "").split(".")[0]

        cookies_path = get_cookies_path(short_domain, cookies_dir)
        if not os.path.exists(cookies_path):
            print(f"⚠️ No cookies found for {short_domain}. Skipping.")
            print(f"👉 This URL likely requires login. Please run:")
            print(f"   nudl-login {short_domain}")
            print(f"(Expected cookies at: {cookies_path})\n")
            return

        post_code = extract_code_from_url(url)
        filename_template = f"{post_code}.{{extension}}"

        command = [
            "gallery-dl",
            f"--cookies={cookies_path}",
            "--filename", filename_template,
            "-d", output_dir,
            url,
        ]

        subprocess.run(command, check=True)
        print(f"🖼️ gallery-dl finished downloading from {url}")

    except FileNotFoundError:
        print("❌ gallery-dl is not installed. Please run: pip install gallery-dl")
    except subprocess.CalledProcessError as e:
        print(f"❌ gallery-dl failed with error: {e}")

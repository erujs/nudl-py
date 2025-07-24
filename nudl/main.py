# nudl/main.py

import os
from urllib.parse import urlparse
from nudl.downloader import download_video, download_image, download_with_gallery_dl

IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff")
URLS_FILE = os.path.join(os.path.dirname(__file__), "..", "urls.txt")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "downloads")


def ensure_urls_file():
    if not os.path.exists(URLS_FILE):
        with open(URLS_FILE, "w", encoding="utf-8") as f:
            f.write("# Paste one URL per line below:\n")
        print(f"📝 Created {URLS_FILE}. Please paste your URLs into it.")
        input("⏸️ Press Enter to continue after you're done...")


def read_urls(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]


def is_direct_image_url(url: str) -> bool:
    return url.lower().endswith(IMAGE_EXTENSIONS)


def should_use_gallery_dl(url: str) -> bool:
    parsed = urlparse(url)
    hostname = parsed.netloc.lower()
    path = parsed.path.lower()

    if "instagram.com" in hostname and path.startswith("/p/"):
        return True
    if "facebook.com" in hostname and "/photo" in path:
        return True
    return False


def main():
    ensure_urls_file()

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    urls = read_urls(URLS_FILE)
    if not urls:
        print("⚠️ No valid URLs found in urls.txt.")
        return

    for url in urls:
        print(f"\n⬇️ Downloading: {url}")
        if is_direct_image_url(url):
            download_image(url, OUTPUT_DIR)
        elif should_use_gallery_dl(url):
            download_with_gallery_dl(url, OUTPUT_DIR)
        else:
            download_video(url, OUTPUT_DIR)

    print(f"\n✅ Done. Processed {len(urls)} item(s).")


if __name__ == "__main__":
    main()

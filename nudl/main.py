import os
from urllib.parse import urlparse
from nudl.downloader import download_video, download_image, download_with_gallery_dl
from nudl.config import CONFIG_DIR, URLS_FILE, OUTPUT_DIR, COOKIES_DIR, ensure_structure

IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff")


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
    ensure_structure()

    urls = read_urls(URLS_FILE)
    if not urls:
        print("⚠️ No valid URLs found in urls.txt.")
        return

    for url in urls:
        print(f"\n⬇️ Downloading: {url}")
        if is_direct_image_url(url):
            download_image(url, OUTPUT_DIR)
        elif should_use_gallery_dl(url):
            download_with_gallery_dl(url, OUTPUT_DIR, COOKIES_DIR)
        else:
            download_video(url, OUTPUT_DIR, COOKIES_DIR)

    print(f"\n✅ Done. Processed {len(urls)} item(s).")


if __name__ == "__main__":
    main()

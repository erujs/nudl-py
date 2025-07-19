import os
from nudl_py.downloader import download_video

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
        download_video(url, OUTPUT_DIR)

    print(f"\n✅ Done. Downloaded {len(urls)} video(s).")

if __name__ == "__main__":
    main()

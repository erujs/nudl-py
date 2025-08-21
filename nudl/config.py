import os

# Root config directory in the folder where the command was executed
CONFIG_DIR = os.path.join(os.getcwd(), "nudl-py-config")

# Subpaths
URLS_FILE = os.path.join(CONFIG_DIR, "urls.txt")
OUTPUT_DIR = os.path.join(CONFIG_DIR, "downloads")
COOKIES_DIR = os.path.join(CONFIG_DIR, ".nudl_cookies")


def ensure_structure():
    """Ensure config, downloads, and cookies dirs exist."""
    os.makedirs(CONFIG_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(COOKIES_DIR, exist_ok=True)

    if not os.path.exists(URLS_FILE):
        with open(URLS_FILE, "w", encoding="utf-8") as f:
            f.write("# Paste one URL per line below:\n")
        print(f"📝 Created {URLS_FILE}. Please paste your URLs into it.")
        input("⏸️ Press Enter to continue after you're done...")

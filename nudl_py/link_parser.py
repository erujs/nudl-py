"""link_parser.py - Handles text file creation, validation, and reading."""

import os

LINKS_FILE = "links.txt"

def get_links() -> list[str] | None:
    """
    Checks the links file. Creates it if missing, flags it if empty.
    Returns a list of links if successful, otherwise returns None.
    """
    # 1. Check if the file DOES NOT exist
    if not os.path.exists(LINKS_FILE):
        print(f"[!] '{LINKS_FILE}' does not exist. We are going to create it for you...")
        
        with open(LINKS_FILE, "w", encoding="utf-8") as f:
            f.write("# Paste your links here (one per line)\n")
            
        print(f"[+] '{LINKS_FILE}' has been created! Please add your links to it and rerun the script.")
        return None

    # 2. If the file DOES exist, read and clean it
    with open(LINKS_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    actual_links = [line.strip() for line in lines if line.strip() and not line.startswith("#")]

    # 3. Check if it's empty
    if not actual_links:
        print(f"[!] '{LINKS_FILE}' exists, but it is empty! Please add some links before running.")
        return None

    return actual_links
"""nudl-py entry point."""

import time
import random
from .link_parser import get_links
from .domain_checker import identify_domain
from .download_router import route_download

def main():
    print("--- Welcome to nudl-py ---")
    
    # 1. Fetch links
    links = get_links()
    if links is None:
        return

    total_links = len(links)
    print(f"[+] Found active links! Analyzing and processing...\n")
    
    # 2. Loop and Route
    for index, link in enumerate(links, 1):
        print(f"----------------------------------------")
        print(f"Item {index} of {total_links}: {link}")
        
        # Identify the domain
        platform = identify_domain(link)
        
        if platform:
            print(f"[+] Identified as: {platform}")
            # Hand it off to the router script!
            route_download(platform, link)
        else:
            print(f"[!] Unsupported domain. Skipping as of the moment.")
            
        # 3. Randomizer Delay
        # Only sleep if there are more items remaining in the batch file
        if index < total_links:
            # Generate a random float between 4.0 and 11.0 seconds
            cooldown = random.uniform(4.0, 11.0)
            
            print(f"[*] Cooldown: Sleeping for {cooldown:.2f} seconds to mimic activity...")
            time.sleep(cooldown)

    print(f"\n----------------------------------------")
    print("[+] All items processed!")


if __name__ == "__main__":
    main()
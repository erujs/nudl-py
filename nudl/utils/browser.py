import sys
import webbrowser

SUPPORTED_SITES = {
    "instagram": "https://www.instagram.com/accounts/login/",
    "facebook": "https://www.facebook.com/login",
    "tiktok": "https://www.tiktok.com/login",
}

def open_supported_site(site: str) -> bool:
    """Open a supported site's login page in the default web browser.
    
    Returns:
        bool: True if successful, False otherwise.
    """
    site = site.lower()
    if site not in SUPPORTED_SITES:
        print(f"ERROR: Unsupported site: {site}", file=sys.stderr)
        print(f"Supported sites: {', '.join(SUPPORTED_SITES.keys())}")
        return False

    url = SUPPORTED_SITES[site]
    print(f"Opening {site.capitalize()} login page...")
    webbrowser.open(url, new=2)  # open in new tab if possible
    print(f"Browser opened: {url}")
    print("\nNext steps:")
    print("  1. Log in to the site in your browser")
    print("  2. Export your cookies using a browser extension (e.g., 'Get cookies.txt LOCALLY')")
    print(f"  3. Save the cookies file to the expected location for {site}")
    return True

def login_main():
    """CLI entry point: nudl-login <site>"""
    if len(sys.argv) != 2:
        print("Usage: nudl-login <site>", file=sys.stderr)
        print(f"Supported sites: {', '.join(SUPPORTED_SITES.keys())}")
        sys.exit(1)

    success = open_supported_site(sys.argv[1])
    sys.exit(0 if success else 1)
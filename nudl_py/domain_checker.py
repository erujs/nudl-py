"""domain_checker.py - Identifies and validates domains for nudl-py."""

from urllib.parse import urlparse

# A mapping of domain keywords to their clean platform names
SUPPORTED_PLATFORMS = {
    "youtube.com": "YT",
    "youtu.be": "YT",
    "tiktok.com": "TT",
    "reddit.com": "RD",
    "instagram.com": "IG",
    "facebook.com": "FB"
}

def identify_domain(url: str) -> str | None:
    """
    Parses a URL and returns the platform name if supported.
    Returns None if the domain is not recognized.
    """
    try:
        parsed_url = urlparse(url)
        # netloc extracts the domain (e.g., 'www.youtube.com' or 'tiktok.com')
        domain = parsed_url.netloc.lower()
        
        # Check if any of our supported platform keywords are inside the domain string
        for keyword, platform_name in SUPPORTED_PLATFORMS.items():
            if keyword in domain:
                return platform_name
                
        return None
    except Exception:
        return None
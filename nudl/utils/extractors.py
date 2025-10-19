import re
from urllib.parse import urlparse, parse_qs

# Pre-compiled regex for cleaning (avoid recompilation on each call)
CLEAN_PATTERN = re.compile(r"[^a-zA-Z0-9_-]")

# Centralized rules with optimized structure
PLATFORM_RULES = {
    "instagram": {
        "query_keys": [],
        "path_keys": ["p", "reel"],
        "short_domain": None
    },
    "facebook": {
        "query_keys": ["fbid", "v"],
        "path_keys": ["reel", "video", "videos"],
        "short_domain": None
    },
    "tiktok": {
        "query_keys": [],
        "path_keys": ["video", "photo"],
        "short_domain": None
    },
    "youtube": {
        "query_keys": ["v"],
        "path_keys": ["shorts"],
        "short_domain": "youtu.be"
    },
    "reddit": {
        "query_keys": [],
        "path_keys": ["comments"],
        "short_domain": None
    }
}

# Generic fallback query keys
GENERIC_QUERY_KEYS = ("viewkey", "id", "video_id", "vid")

def extract_post_id(url: str) -> str:
    """
    Efficiently extracts post/reel/video IDs across major platforms.
    Supports generic patterns like ?viewkey=xxxxxx or ?id=xxxxxx.
    """
    parsed = urlparse(url)
    hostname = parsed.netloc.lower()
    path_parts = [p for p in parsed.path.strip("/").split("/") if p]  # Filter empty parts
    query = parse_qs(parsed.query)
    
    post_id = None
    
    # --- Platform-specific extraction ---
    for domain, rules in PLATFORM_RULES.items():
        if domain not in hostname:
            continue
            
        # Check query parameters first (fastest)
        if rules["query_keys"]:
            for key in rules["query_keys"]:
                if key in query:
                    post_id = query[key][0]
                    break
        
        # Check path-based extraction
        if not post_id and rules["path_keys"]:
            path_set = set(path_parts)  # O(1) lookup
            for key in rules["path_keys"]:
                if key in path_set:
                    idx = path_parts.index(key)
                    if idx + 1 < len(path_parts):
                        post_id = path_parts[idx + 1]
                        break
        
        # Check short domain format
        if not post_id and rules["short_domain"] and rules["short_domain"] in hostname:
            if path_parts:
                post_id = path_parts[0]
        
        break  # Found matching domain, stop searching
    
    # --- Generic fallback ---
    if not post_id:
        # Try common query parameters
        for key in GENERIC_QUERY_KEYS:
            if key in query:
                post_id = query[key][0]
                break
        
        # Last resort: use last path segment
        if not post_id and path_parts:
            post_id = path_parts[-1]
    
    # --- Clean and return ---
    if post_id:
        post_id = CLEAN_PATTERN.sub("", post_id)
    
    return post_id or "unknown_post"
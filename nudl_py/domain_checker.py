"""domain_checker.py - Identifies and validates domains for nudl-py."""

from urllib.parse import urlparse
from .platforms import SUPPORTED_PLATFORMS


def identify_domain(url: str) -> str | None:
    try:
        domain = urlparse(url).netloc.lower()
        for code, platform in SUPPORTED_PLATFORMS.items():
            if any(keyword in domain for keyword in platform.domains):
                return code
        return None
    except Exception:
        return None
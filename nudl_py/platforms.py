"""platforms.py - Single source of truth for supported platforms."""

from typing import Callable, NamedTuple, Optional


class Platform(NamedTuple):
    code: str
    domains: tuple[str, ...]
    # Returns True if this specific URL is a static (non-video) post to skip.
    is_static_post: Optional[Callable[[str], bool]] = None


SUPPORTED_PLATFORMS: dict[str, Platform] = {
    "YT": Platform("YT", ("youtube.com", "youtu.be")),
    "TT": Platform("TT", ("tiktok.com",)),
    "RD": Platform("RD", ("reddit.com",),
                   is_static_post=lambda u: "i.redd.it" in u),
    "IG": Platform("IG", ("instagram.com",),
                   is_static_post=lambda u: "/p/" in u),
    "FB": Platform("FB", ("facebook.com", "fb.watch"),
                   is_static_post=lambda u: not any(
                       x in u for x in ["/videos/", "/watch", "/reel", "fb.watch"]
                   )),
}
import sys
from nudl.auth.browser import login_and_save_cookies

SUPPORTED_SITES = {
    "instagram": "https://www.instagram.com/accounts/login/",
    "facebook": "https://www.facebook.com/login",
    "tiktok": "https://www.tiktok.com/login"
}

def login_main():
    if len(sys.argv) != 2:
        print("❌ Usage: nudl-login <site>")
        print(f"✅ Supported sites: {', '.join(SUPPORTED_SITES)}")
        sys.exit(1)

    site = sys.argv[1].lower()

    if site not in SUPPORTED_SITES:
        print(f"❌ Unsupported site: {site}")
        print(f"✅ Supported sites: {', '.join(SUPPORTED_SITES)}")
        sys.exit(1)

    login_url = SUPPORTED_SITES[site]
    print(f"🌐 Opening login page for {site}...")

    login_and_save_cookies(site, login_url)

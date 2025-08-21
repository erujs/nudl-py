import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from nudl.config import COOKIES_DIR


def login_and_save_cookies(site: str, login_url: str):
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(login_url)
        print("🔐 Please complete the login in the browser window.")
        print("⚠️ Do NOT close the browser manually.")
        print("   Once you finish logging in, return here and press Enter.")
        print("   The browser will close automatically after that.")
        input("⏸️ Press Enter here AFTER you've successfully logged in...")

        cookies = driver.get_cookies()
        driver.quit()

        save_cookies_as_netscape(site, cookies)
    except Exception as e:
        driver.quit()
        print(f"❌ Failed to capture cookies for {site}: {e}")


def save_cookies_as_netscape(site: str, cookies: list):
    os.makedirs(COOKIES_DIR, exist_ok=True)
    path = os.path.join(COOKIES_DIR, f"{site}.txt")

    with open(path, "w", encoding="utf-8") as f:
        f.write("# Netscape HTTP Cookie File\n")
        for cookie in cookies:
            domain = cookie["domain"]
            include_subdomains = "TRUE" if domain.startswith(".") else "FALSE"
            path_value = cookie.get("path", "/")
            secure = "TRUE" if cookie.get("secure", False) else "FALSE"
            expiry = int(cookie.get("expiry", 0))
            name = cookie["name"]
            value = cookie["value"]

            f.write(
                f"{domain}\t{include_subdomains}\t{path_value}\t{secure}\t{expiry}\t{name}\t{value}\n"
            )

    print(f"✅ Saved cookies for {site} to: {path}")

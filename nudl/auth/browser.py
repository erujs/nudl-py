# nudl/auth/browser.py

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def login_and_save_cookies(site: str, login_url: str):
    # Setup Selenium with Chrome (can be extended for Firefox)
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(login_url)
        print("🔐 Please complete the login in the browser window.")
        input("⏸️ Press Enter here AFTER you've successfully logged in...")

        cookies = driver.get_cookies()
        driver.quit()

        # Save cookies
        save_cookies_as_netscape(site, cookies)
    except Exception as e:
        driver.quit()
        print(f"❌ Failed to capture cookies for {site}: {e}")

def save_cookies_as_netscape(site: str, cookies: list):
    cookies_dir = os.path.expanduser("~/.nudl_cookies")
    os.makedirs(cookies_dir, exist_ok=True)

    path = os.path.join(cookies_dir, f"{site}.txt")

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

            f.write(f"{domain}\t{include_subdomains}\t{path_value}\t{secure}\t{expiry}\t{name}\t{value}\n")

    print(f"✅ Saved cookies for {site} to: {path}")

# nudl-py

Python Media Downloader ~ A Python-based CLI tool for downloading media from popular social media platforms.  
This project was scaffolded using [cc-py](https://github.com/erujs/cc-py), a Cookiecutter template for building Python CLI applications.

## Dependencies

Ensure you have the following dependencies installed (if you haven’t already):

- **Python 3.8+** - required to develop and run the project
- **pipx** (recommended) – for installing and running the generated CLI apps in isolated environments
- **ffmpeg** - required by yt-dlp to merge streams, embed thumbnails, and add metadata

### Other dependencies will be installed automatically when you install this package

- **yt-dlp** – used for downloading videos and audio from supported platforms (e.g., YouTube, Twitter, TikTok, etc.)
- **gallery-dl** – used for downloading media from social platforms that require authentication or handle images better (e.g., Instagram posts, Facebook photos, reddit)

## Installation

You can install using `pipx` (recommended) or clone the repo directly:

### Option 1: Install with pipx
```bash
pipx install git+https://github.com/erujs/nudl-py.git
```

### Option 2: Clone the repo
```bash
pip install -e .
```

## Usage

```bash
nudl-py 
# Run the main CLI to start the program.
#
# On first run, this will create a folder called `nudl-py-config`
# in the directory where the command is executed. Inside it, you’ll find:
#
# - `downloads/` → the folder where downloaded media will be saved
# - `urls.txt` → a text file where you can paste media URLs (one per line)
#
# The CLI will guide you through the process.
# On subsequent runs, simply update `urls.txt` and your downloads
# will appear in the `downloads/` folder.
```

```bash
nudl-login <social-media>
# Authenticate and save login cookies for private or logged-in URLs.
#
# Example:
#   nudl-login tiktok
#
# Supported platforms: facebook, instagram, tiktok
#
# Some platforms require login cookies
# to access private or restricted media. Running this command will:
# - Launch a login url from your default browser
# - Allow you to log in manually
# - Will prompt you to export your cookies using browser extension (e.g., Get cookies.txt LOCALLY)
# - Then you will need to Save your cookies to `nudl-py-config/.nudl_cookies/`
#
# The CLI will guide you through the process.
# Once cookies are saved, you can run `nudl-py` to download
# private or logged-in content from the chosen platform.
```

## 🧾 License
MIT — do whatever you want with it.

✨ Happy coding!
If you find this project useful, a ⭐ on the repo is always appreciated!
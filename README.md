# nudl-py

A minimal yet powerful Python media downloader that supports links from most popular media platforms.

Built for personal use with a simple workflow:  
just paste your URLs into a `urls.txt` file and run `nudl-py` from the command line.

## 🚀 Usage

You can install using `pipx` (recommended) or clone the repo directly:

### Option 1: Install with pipx
```bash
pipx install git+https://github.com/erujs/nudl-py.git
nudl-py
```

### Option 2: Clone the repo
```bash
pip install -e .
nudl-py
```

## 📥 Downloading Media
On first run:

- A nudl-py-config/ folder will be created on the current directory the command was executed.
- Open nudl-py-config/urls.txt then paste one media URL per line, save the file, then press Enter.
- Files will be saved to the nudl-py-config/downloads/ folder.

🎞️ Videos are downloaded using yt-dlp.  
🖼️ Posts and images (e.g. Instagram, Facebook) use gallery-dl.  

## 🔐 Downloading from Private/Logged-in URLs
Some platforms (like Instagram or Facebook) require login cookies.

To download from those (in this example instagram):

```bash
nudl-login instagram
```

This will open a browser window where you can log in.  
After login, your cookies are saved to nudl-py-config/.nudl_cookies/

### 📝 Reddit Video Note  
For Reddit, make sure to right-click the video and choose “Copy video address” — not just the post URL.  
This ensures the downloader grabs the actual media file.  

Example:  
✅ Correct: https://packaged-media.redd.it/xyzabc123/pb/...  
❌ Incorrect: https://www.reddit.com/r/.../comments/...  

## 📦 Dependencies
- yt_dlp
- gallery-dl
- selenium (used for login)
- Python 3.8+
Also ensure ffmpeg is installed for best media format support.

## 🧾 License
MIT — do whatever you want with it.
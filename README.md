# nudl-py

A minimal yet powerful Python video downloader that supports links from most popular video and media platforms — all powered by yt_dlp.

Built for personal use with a simple workflow:  
just paste your URLs into a `urls.txt` file and run `nudl-py` from the command line.

## 🚀 Usage

You can install using `pipx` (recommended) or clone the repo directly:

Option 1: Install with pipx
```bash
pipx install git+https://github.com/your-username/nudl-py.git
nudl-py
```

Option 2: Clone the repo
```bash
pip install -e .
nudl-py
```

On the first run, a file named urls.txt will be created in your current directory.  
Open it, paste one video URL per line, save the file, then press Enter to continue.  
Files are saved to the downloads/ folder.  

📝 Reddit Video Note  
For Reddit, make sure to right-click the video and choose “Copy video address” — not just the post URL.  
This ensures the downloader grabs the actual media file.  

Example:  
✅ Correct: https://packaged-media.redd.it/xyzabc123/pb/...  
❌ Incorrect: https://www.reddit.com/r/.../comments/...  

## 📦 Dependencies
- yt_dlp
- Python 3.8+

Make sure ffmpeg is installed on your system for best results.

## 🧾 License
MIT — do whatever you want with it.
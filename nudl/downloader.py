import os
from yt_dlp import YoutubeDL

def download_video(url: str, output_dir: str = "downloads"):
    ydl_opts = {
        "format": "best",
        "outtmpl": f"{output_dir}/%(title).80s~%(id)s.%(ext)s",
        "merge_output_format": "mp4",
    }

    with YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=True)
            original_filename = ydl.prepare_filename(info)

            # Only apply renaming logic for Reddit URLs
            if "packaged-media.redd.it" in url:
                clean_filename = original_filename.split("?")[0]
                if clean_filename != original_filename:
                    os.rename(original_filename, clean_filename)
                    print(f"✅ Reddit video renamed to: {clean_filename}")
                else:
                    print(f"✅ Reddit video saved as: {original_filename}")
            else:
                print(f"✅ Downloaded: {original_filename}")

        except Exception as e:
            print(f"❌ Failed to download {url}: {e}")

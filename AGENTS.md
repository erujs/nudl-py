# AGENTS.md

## Project overview

nudl-py ("Not yoUr DownLoader") is a CLI batch downloader built on `yt-dlp`. It reads a
list of links from `links.txt`, identifies which platform each URL belongs to, skips
static (non-video) posts, and downloads the rest into `downloads/`.

## Commands

```bash
pip install -e ".[dev]"   # install project + dev deps (pytest)
python -m nudl_py.main    # run directly
nudl_py                   # run via installed console script (pyproject [project.scripts])
pytest                    # run tests
```

## Architecture

Pipeline, one module per stage, wired together in `nudl_py/main.py`:

- `link_parser.py` — reads `links.txt` from the current working directory; creates it
  with a placeholder comment if missing, and returns `None` if it's missing or empty.
- `domain_checker.py` — `identify_domain(url)` matches the URL's netloc against
  `SUPPORTED_PLATFORMS` domains and returns a platform code (e.g. `"YT"`) or `None`.
- `platforms.py` — single source of truth for supported platforms. Each `Platform`
  NamedTuple carries a `code`, its `domains` tuple, and an optional `is_static_post(url)`
  predicate used to skip non-video content (e.g. Reddit image posts, Instagram `/p/`
  posts, Facebook posts that aren't `/videos/`, `/watch`, `/reel`, or `fb.watch`).
- `download_router.py` — looks up the platform, skips it if `is_static_post` matches,
  otherwise hands the URL to the engine.
- `ytdlp_engine.py` — wraps `yt_dlp.YoutubeDL`. Tries browser cookies from `firefox`
  then `brave` in order (via `cookiesfrombrowser`), falling through to the next browser
  on `DownloadError`. Downloads land in `downloads/<id>.<ext>`.

`main.py` loops over links, adds a randomized 4–11s sleep between downloads (skipped
after the last item) to avoid looking like automated bulk activity.

## Conventions

- Adding a new platform means adding one entry to `SUPPORTED_PLATFORMS` in
  `platforms.py` — no changes needed elsewhere in the pipeline.
- User-facing progress messages are printed directly (no logging module), prefixed
  with tags like `[+]`, `[!]`, `[*]`, and router/engine output is indented with
  `    [Router]` / `    [Engine]` to visually nest under the per-link header.

## Gotchas

- `links.txt` and `downloads/` are created relative to the current working directory,
  not the package location — run `nudl_py`/`python -m nudl_py.main` from wherever you
  want those to live.
- Downloading requires a local Firefox or Brave profile with valid session cookies for
  the target site (`cookiesfrombrowser`); there's no other auth path, and if both
  browsers fail the link is silently skipped.

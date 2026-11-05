"""
Background dictionary downloader.
"""
import os
import threading
import urllib.request
from typing import Callable


def download_enable_dictionary(target_path: str,
                               on_success: Callable[[str], None],
                               on_error: Callable[[str], None],
                               on_progress: Callable[[str], None]) -> None:
    """Download official tournament Scrabble ENABLE1 dictionary in background."""
    url = "https://raw.githubusercontent.com/raun/Scrabble/master/words.txt"

    def worker():
        try:
            on_progress("Downloading official Scrabble word list...")
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=12) as response, open(target_path, 'wb') as f:
                f.write(response.read())
            on_success(target_path)
        except Exception as e:
            on_error(str(e))

    threading.Thread(target=worker, daemon=True).start()


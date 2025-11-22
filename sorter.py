"""
sorter.py
Watches a folder (watch_folder/) and sorts files into categorized folders.
Generates AI summaries (via ai_summary.py) and logs operations (via log_handler.py).
Hybrid approach: AI calls are optional; falls back to local heuristics if no API key.
"""
import os
import shutil
import time
import hashlib
from pathlib import Path
from log_handler import LogHandler
from ai_summary import summarize_file

WATCH_DIR = Path(__file__).parent / "watch_folder"
DEST_DIR = Path(__file__).parent / "sorted"
LOG_FILE = Path(__file__).parent / "logs" / "log.json"

CATEGORIES = {
    "images": [".png", ".jpg", ".jpeg", ".gif", ".bmp"],
    "documents": [".pdf", ".docx", ".doc", ".txt", ".md"],
    "spreadsheets": [".xls", ".xlsx", ".csv"],
    "audio": [".mp3", ".wav", ".ogg"],
    "video": [".mp4", ".mkv", ".mov"],
    "archives": [".zip", ".tar", ".gz"],
    "code": [".py", ".js", ".java", ".c", ".cpp", ".ipynb"]
}

def file_hash(path, algo="sha256"):
    h = hashlib.new(algo)
    with open(path, "rb") as f:
        while True:
            data = f.read(8192)
            if not data:
                break
            h.update(data)
    return h.hexdigest()

def classify_by_extension(filename):
    ext = Path(filename).suffix.lower()
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    return "others"

def ensure_dirs():
    WATCH_DIR.mkdir(parents=True, exist_ok=True)
    DEST_DIR.mkdir(parents=True, exist_ok=True)
    (Path(__file__).parent / "logs").mkdir(parents=True, exist_ok=True)
    for cat in list(CATEGORIES.keys()) + ["others"]:
        (DEST_DIR / cat).mkdir(parents=True, exist_ok=True)

def process_file(path, log_handler):
    path = Path(path)
    category = classify_by_extension(path.name)
    dest = DEST_DIR / category / path.name
    # avoid overwrite
    if dest.exists():
        base, ext = path.stem, path.suffix
        i = 1
        while dest.exists():
            dest = DEST_DIR / category / f"{base}_{i}{ext}"
            i += 1
    # compute hash
    h = file_hash(path)
    # attempt AI summary (may return None if no API set)
    summary = summarize_file(path)
    # move the file
    shutil.move(str(path), str(dest))
    log_entry = {
        "timestamp": int(time.time()),
        "original_name": path.name,
        "destination": str(dest),
        "category": category,
        "hash": h,
        "ai_summary": summary
    }
    log_handler.append(log_entry)
    print(f"Processed {path.name} -> {category} (hash={h[:8]})")

def watch_loop(poll_seconds=2):
    ensure_dirs()
    log_handler = LogHandler(LOG_FILE)
    print("Watching folder:", WATCH_DIR)
    while True:
        files = [p for p in WATCH_DIR.iterdir() if p.is_file()]
        for f in files:
            try:
                process_file(f, log_handler)
            except Exception as e:
                print("Error processing", f, e)
        time.sleep(poll_seconds)

if __name__ == "__main__":
    watch_loop()

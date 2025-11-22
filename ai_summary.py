"""
ai_summary.py
Provides a summarize_file(path) function that tries an AI call if configured,
or falls back to lightweight heuristics (first lines, metadata) when no API key is set.
"""
import os
import hashlib
from pathlib import Path

# Toggle AI usage via environment variable AI_API_ENABLED (set to "1" to enable)
USE_AI = os.getenv("AI_API_ENABLED", "0") == "1"

def summarize_text_content(text, max_len=200):
    s = " ".join(text.strip().split())
    return s[:max_len] + ("..." if len(s) > max_len else "")

def summarize_file(path):
    path = Path(path)
    ext = path.suffix.lower()
    # If AI disabled, use heuristics
    if not USE_AI:
        try:
            if ext in [".txt", ".md", ".py", ".java", ".js"]:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    lines = [next(f) for _ in range(10)]
                return summarize_text_content(" ".join(lines))
            elif ext in [".pdf"]:
                return "PDF file - content summary not available in offline mode."
            elif ext in [".jpg", ".png", ".jpeg", ".gif"]:
                return "Image file - visual content."
            else:
                return f"File type {ext} detected."
        except Exception as e:
            return None
    else:
        # Placeholder: In real usage, implement an API call to an LLM (e.g., OpenAI/GPT)
        # This code intentionally does not perform network requests.
        return "AI-generated summary (API integration required)."

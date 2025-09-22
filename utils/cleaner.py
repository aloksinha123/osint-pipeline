# utils/cleaner.py
import re
from langdetect import detect

def clean_text(text):
    text = re.sub(r"http\S+", "", text)  # remove URLs
    text = re.sub(r"[^A-Za-z0-9\s]", "", text)  # remove symbols
    return text.strip()

def filter_english(records):
    out = []
    for r in records:
        txt = (r.get("text") or "").strip()
        if not txt:
            continue
        try:
            if detect(txt) == "en":
                out.append(r)
        except Exception:
            out.append(r)  # keep if detection fails
    return out

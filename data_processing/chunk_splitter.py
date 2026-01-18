import os
import re
import json
from itertools import count

INPUT_DIR = "filtered_sources"
OUTPUT_DIR = "chunks"

MIN_WORDS = 150
MAX_WORDS = 800

os.makedirs(OUTPUT_DIR, exist_ok=True)

chunk_id_counter = count(1)

def word_count(text):
    return len(text.split())

def split_large_text(text, max_words):
    words = text.split()
    parts = []
    for i in range(0, len(words), max_words):
        parts.append(" ".join(words[i:i+max_words]))
    return parts
RISK_KEYWORDS = {
    "high": [
        "termination", "harassment", "disciplinary",
        "violation", "investigation", "legal action"
    ],
    "medium": [
        "leave", "benefits", "performance",
        "working hours", "promotion", "compensation"
    ]
}

def infer_risk_level(text: str) -> str:
    t = text.lower()
    for level, keywords in RISK_KEYWORDS.items():
        if any(k in t for k in keywords):
            return level
    return "low"

for filename in os.listdir(INPUT_DIR):
    file_path = os.path.join(INPUT_DIR, filename)

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        raw = f.read()

    lines = raw.splitlines()

    # Extract SOURCE and PATH
    source = "unknown"
    path = "unknown"
    content_start = 0

    for i, line in enumerate(lines):
        if line.startswith("SOURCE:"):
            source = line.replace("SOURCE:", "").strip()
        elif line.startswith("PATH:"):
            path = line.replace("PATH:", "").strip()
        elif line.strip() == "":
            content_start = i + 1
            break

    content = "\n".join(lines[content_start:]).strip()
    if not content:
        continue

    # Split on ## headings
    sections = re.split(r"\n(?=## )", content)

    for section in sections:
        lines = section.strip().splitlines()
        if not lines:
            continue

        heading = lines[0].replace("##", "").strip() if lines[0].startswith("##") else "General"
        body = "\n".join(lines[1:]).strip()

        if word_count(body) < MIN_WORDS:
            continue

        # Further split on ### if too large
        sub_sections = [body]
        if word_count(body) > MAX_WORDS:
            sub_sections = re.split(r"\n(?=### )", body)

        for sub in sub_sections:
            sub = sub.strip()
            if not sub:
                continue

            wc = word_count(sub)

            if wc > MAX_WORDS:
                parts = split_large_text(sub, MAX_WORDS)
            else:
                parts = [sub]

            for part in parts:
                if word_count(part) < MIN_WORDS:
                    continue

                risk_level = infer_risk_level(part)

                chunk = {
                    "chunk_id": f"chunk_{next(chunk_id_counter):06d}",
                    "source": source,
                    "path": path,
                    "heading": heading,
                    "text": part,
                    "risk_level": risk_level
                }

                out_file = os.path.join(
                    OUTPUT_DIR,
                    f"{chunk['chunk_id']}.json"
                )

                with open(out_file, "w", encoding="utf-8") as out:
                    json.dump(chunk, out, indent=2, ensure_ascii=False)

print("Chunking complete.")
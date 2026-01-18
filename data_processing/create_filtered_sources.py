import os

INPUT_DIR = "parsed_sources"
FILTERED_DIR = "filtered_sources"

os.makedirs(FILTERED_DIR, exist_ok=True)

MIN_CHARS = 500

kept = 0

for fname in os.listdir(INPUT_DIR):
    path = os.path.join(INPUT_DIR, fname)
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    content_only = "\n".join(
        line for line in text.splitlines()
        if not line.strip().startswith(("{%", "{{", "<", ">"))
    )

    if len(content_only) < MIN_CHARS:
        continue

    with open(os.path.join(FILTERED_DIR, fname), "w", encoding="utf-8") as out:
        out.write(content_only)

    kept += 1

print(f"Kept {kept} meaningful source files.")
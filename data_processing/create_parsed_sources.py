import re
import os

INPUT_FILE = "gitlab_handbook_compiled.txt"
OUTPUT_DIR = "parsed_sources"

os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(INPUT_FILE, "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# Split on SOURCE delimiters
blocks = re.split(r"=+\nSOURCE:", text)

for i, block in enumerate(blocks[1:]):  # first split is junk
    header, content = block.split("\n====================", 1)

    # Extract source and path
    lines = header.strip().splitlines()
    source = lines[0].strip()
    path = lines[1].replace("PATH:", "").strip() if len(lines) > 1 else "unknown"

    filename = f"{i}_{source.replace('.','_')}.txt"

    with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as out:
        out.write(f"SOURCE: {source}\n")
        out.write(f"PATH: {path}\n\n")
        out.write(content.strip())

print(f"Created {len(blocks)-1} source files.")
#!/usr/bin/env python3
"""Tile frames into labeled contact sheets so each thumbnail can be traced back to its file."""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

src = Path(sys.argv[1])
out_stem = sys.argv[2] if len(sys.argv) > 2 else str(src / "sheet")
per_sheet = int(sys.argv[3]) if len(sys.argv) > 3 else 12
cols = int(sys.argv[4]) if len(sys.argv) > 4 else 6
TW, LABEL = 200, 18

frames = sorted(p for p in src.iterdir() if p.suffix.lower() in {".png", ".jpg", ".jpeg"})
if not frames:
    sys.exit(f"no frames in {src}")

for s in range((len(frames) + per_sheet - 1) // per_sheet):
    batch = frames[s * per_sheet : (s + 1) * per_sheet]
    thumbs = []
    for p in batch:
        im = Image.open(p).convert("RGB")
        thumbs.append((p.name, im.resize((TW, round(im.height * TW / im.width)))))
    th = max(t.height for _, t in thumbs)
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * TW, rows * (th + LABEL)), "white")
    d = ImageDraw.Draw(sheet)
    for i, (name, t) in enumerate(thumbs):
        x, y = (i % cols) * TW, (i // cols) * (th + LABEL)
        d.text((x + 4, y + 4), name, fill="black")
        sheet.paste(t, (x, y + LABEL))
    path = f"{out_stem}{s + 1}.jpg"
    sheet.save(path, quality=88)
    print(path)

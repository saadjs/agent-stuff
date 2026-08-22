#!/usr/bin/env python3
"""Crop a frame, then pad it to an exact aspect ratio using its own background color.

usage: crop_pad.py <src> <dst> <top> <bottom> [W:H] [left] [right]
  top/bottom  y pixels to cut (status bar / tab bar); bottom is measured from the top edge,
              or pass 0 for "to the bottom edge".
"""
import sys

from PIL import Image

src, dst = sys.argv[1], sys.argv[2]
top, bottom = int(sys.argv[3]), int(sys.argv[4])
ratio = sys.argv[5] if len(sys.argv) > 5 else "9:16"
rw, rh = (int(v) for v in ratio.split(":"))

im = Image.open(src).convert("RGB")
left = int(sys.argv[6]) if len(sys.argv) > 6 else 0
right = int(sys.argv[7]) if len(sys.argv) > 7 else im.width
im = im.crop((left, top, right, bottom or im.height))

w, h = im.size
bg = im.getpixel((3, 3))
if h < round(w * rh / rw):
    H = round(w * rh / rw)
    out = Image.new("RGB", (w, H), bg)
    out.paste(im, (0, (H - h) // 2))
else:
    W = round(h * rw / rh)
    out = Image.new("RGB", (W, h), bg)
    out.paste(im, ((W - w) // 2, 0))

out.save(dst, quality=92)
print(f"{dst} {out.size[0]}x{out.size[1]}")

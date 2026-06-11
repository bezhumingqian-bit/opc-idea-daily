#!/usr/bin/env python3
"""Generate MUJI-style OPC app icons (192x192 and 512x512)."""
from PIL import Image, ImageDraw, ImageFont
import os

# MUJI palette
BG = (250, 248, 243)      # paper
INK = (139, 111, 71)      # accent (warm brown)
INK_DARK = (26, 26, 26)   # dark text

def find_font(size, bold=False):
    """Find a Chinese-capable system font on macOS."""
    candidates = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()

def make_icon(size: int) -> Image.Image:
    img = Image.new("RGB", (size, size), BG)
    draw = ImageDraw.Draw(img)

    # Rounded rectangle frame (subtle)
    pad = int(size * 0.04)
    radius = int(size * 0.18)
    draw.rounded_rectangle(
        [pad, pad, size - pad, size - pad],
        radius=radius,
        outline=INK,
        width=max(1, int(size * 0.012))
    )

    # Top label "OPC"
    label_font = find_font(int(size * 0.10), bold=True)
    label = "OPC"
    bbox = draw.textbbox((0, 0), label, font=label_font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    draw.text(((size - w) / 2, size * 0.20), label, fill=INK, font=label_font)

    # Big number "01" (vol number)
    num_font = find_font(int(size * 0.34), bold=True)
    num = "01"
    bbox = draw.textbbox((0, 0), num, font=num_font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    draw.text(((size - w) / 2, size * 0.50 - h / 2), num, fill=INK_DARK, font=num_font)

    # Bottom small label
    sub_font = find_font(int(size * 0.075))
    sub = "IDEA"
    bbox = draw.textbbox((0, 0), sub, font=sub_font)
    w = bbox[2] - bbox[0]
    draw.text(((size - w) / 2, size * 0.80), sub, fill=INK, font=sub_font)

    return img

out_dir = "/Users/darkngiht/WorkBuddy/2026-06-09-16-52-35/opc-idea-site"
for size in (192, 512):
    img = make_icon(size)
    img.save(os.path.join(out_dir, f"icon-{size}.png"), "PNG", optimize=True)
    print(f"✅ icon-{size}.png ({size}x{size})")
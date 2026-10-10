"""Renders PNG icons and the social share image from assets/icon.svg.

Run from the project root:  python3 scripts/make_images.py
Requires macOS (uses Quick Look to rasterize the SVG) and Pillow.
"""
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"


def render_svg(size):
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(
            ["qlmanage", "-t", "-s", str(size), "-o", tmp, str(ASSETS / "icon.svg")],
            check=True,
            capture_output=True,
        )
        img = Image.open(Path(tmp) / "icon.svg.png").convert("RGBA").copy()
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        [0, 0, img.size[0] - 1, img.size[1] - 1], radius=int(img.size[0] * 14 / 64), fill=255
    )
    img.putalpha(mask)
    return img


def font(size, bold=True):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def main():
    icon = render_svg(1024)

    for name, size in [("icon-192.png", 192), ("icon-512.png", 512), ("favicon-32.png", 32)]:
        icon.resize((size, size), Image.LANCZOS).save(ASSETS / name)

    touch = Image.new("RGBA", (180, 180), "#13294b")
    small = icon.resize((180, 180), Image.LANCZOS)
    touch.alpha_composite(small)
    touch.convert("RGB").save(ASSETS / "apple-touch-icon.png")

    w, h = 1200, 630
    og = Image.new("RGB", (w, h), "#0c1c36")
    draw = ImageDraw.Draw(og)
    for y in range(h):
        t = y / h
        r = int(12 + (26 - 12) * t)
        g = int(28 + (53 - 28) * t)
        b = int(54 + (96 - 54) * t)
        draw.line([(0, y), (w, y)], fill=(r, g, b))
    draw.rectangle([0, h - 14, w, h], fill="#f29a3b")

    og.paste(icon.resize((200, 200), Image.LANCZOS), (90, 110), icon.resize((200, 200), Image.LANCZOS))
    draw.text((90, 350), "Stakich Websites", font=font(76), fill="#ffffff")
    draw.text((92, 445), "Trusted websites for small businesses", font=font(38, bold=False), fill="#c9d8ee")
    draw.text((92, 497), "at a fair price.", font=font(38, bold=False), fill="#f29a3b")
    og.save(ASSETS / "og-image.png", optimize=True)
    print("images written")


if __name__ == "__main__":
    main()

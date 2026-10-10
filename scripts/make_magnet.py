"""Makes print-ready car and truck magnet designs with the QR code.

Run from the project root:  python3 scripts/make_magnet.py
Writes 300 DPI PNG + PDF files (with 1/8 inch bleed) to "Car Magnets/".
"""
from pathlib import Path

from PIL import Image, ImageDraw

from make_qr import NAVY, NAVY_DARK, ORANGE, SKY, font, qr_panel

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "Car Magnets"
DPI = 300
BLEED = int(DPI * 0.125)
PHONE = "(423) 227-7681"


def fit(d, text, size, max_w, bold=True):
    while size > 10 and d.textlength(text, font=font(size, bold)) > max_w:
        size -= 4
    return font(size, bold)


def magnet(w_in, h_in, name):
    w, h = int(w_in * DPI) + BLEED * 2, int(h_in * DPI) + BLEED * 2
    img = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(img)
    for y in range(h):
        t = y / h
        d.line([(0, y), (w, y)], fill=tuple(int(a + (b - a) * t) for a, b in zip(NAVY_DARK, (26, 53, 96))))
    band_h = int(0.95 * DPI)
    band_top = h - BLEED - band_h
    d.rectangle([0, band_top, w, h], fill=ORANGE)
    band_f = font(int(0.7 * DPI))
    band = "stakichwebsites.com"
    d.text(((w - d.textlength(band, font=band_f)) / 2, band_top + (band_h - band_f.size) // 2 - int(0.05 * DPI)), band, font=band_f, fill=NAVY_DARK)

    safe = BLEED + int(0.6 * DPI)
    area_top, area_bottom = safe, band_top - int(0.5 * DPI)
    area_h = area_bottom - area_top

    scan_f = font(int(0.55 * DPI))
    scan_gap = int(0.15 * DPI)
    panel = qr_panel(int(min(area_h - scan_f.size - scan_gap, w * 0.36)) * 100 // 116)
    px = w - safe - panel.width
    py = area_top + (area_h - panel.height - scan_gap - scan_f.size) // 2
    img.paste(panel, (px, py), panel)
    scan = "Scan me"
    d.text((px + (panel.width - d.textlength(scan, font=scan_f)) / 2, py + panel.height + scan_gap), scan, font=scan_f, fill=(255, 255, 255))

    text_w = px - safe - int(0.6 * DPI)
    x = safe
    logo_side = int(1.5 * DPI)
    f1 = fit(d, "Stakich Websites", int(1.6 * DPI), text_w)
    f2 = fit(d, "Websites for small businesses", int(0.8 * DPI), text_w, bold=False)
    f_call = font(int(0.65 * DPI))
    f3 = fit(d, PHONE, int(1.35 * DPI), text_w)
    gaps = [int(0.35 * DPI), int(0.25 * DPI), int(0.6 * DPI), int(0.15 * DPI)]
    block = logo_side + f1.size + f2.size + f_call.size + f3.size + sum(gaps)
    y = area_top + (area_h - block) // 2
    logo = Image.open(ROOT / "assets" / "icon-512.png").convert("RGBA").resize((logo_side, logo_side), Image.LANCZOS)
    img.paste(logo, (x, y), logo)
    y += logo_side + gaps[0]
    d.text((x, y), "Stakich Websites", font=f1, fill=(255, 255, 255))
    y += f1.size + gaps[1]
    d.text((x, y), "Websites for small businesses", font=f2, fill=SKY)
    y += f2.size + gaps[2]
    d.text((x, y), "Call or text", font=f_call, fill=ORANGE)
    y += f_call.size + gaps[3]
    d.text((x, y), PHONE, font=f3, fill=(255, 255, 255))

    OUT.mkdir(exist_ok=True)
    png = OUT / f"{name}.png"
    img.save(png, dpi=(DPI, DPI), optimize=True)
    img.save(OUT / f"{name}.pdf", "PDF", resolution=DPI)
    return png


def main():
    magnet(18, 12, "Car magnet 18x12 in - PRINT THIS")
    magnet(24, 12, "Truck magnet 24x12 in - PRINT THIS")
    print("wrote Car Magnets/")


if __name__ == "__main__":
    main()

"""Makes the QR code image and a vertical TikTok video that both scan to stakichwebsites.com.

Run from the project root:  python3 scripts/make_qr.py
Requires Pillow, qrcode, and imageio-ffmpeg (bundled ffmpeg).
"""
import math
import subprocess
from pathlib import Path

import imageio_ffmpeg
import qrcode
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "qr"
URL = "https://stakichwebsites.com"
NAVY = (19, 41, 75)
NAVY_DARK = (12, 28, 54)
ORANGE = (242, 154, 59)
SKY = (201, 216, 238)


def font(size, bold=True):
    for path in [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
    ]:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def qr_image(side):
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, border=0, box_size=20)
    qr.add_data(URL)
    qr.make(fit=True)
    img = qr.make_image(fill_color=NAVY, back_color="white").convert("RGBA")
    img = img.resize((side, side), Image.NEAREST)
    logo_side = int(side * 0.22)
    pad = int(logo_side * 0.14)
    plate = Image.new("RGBA", (logo_side + pad * 2, logo_side + pad * 2), (0, 0, 0, 0))
    ImageDraw.Draw(plate).rounded_rectangle([0, 0, plate.width - 1, plate.height - 1], radius=pad * 2, fill="white")
    logo = Image.open(ROOT / "assets" / "icon-512.png").convert("RGBA").resize((logo_side, logo_side), Image.LANCZOS)
    plate.alpha_composite(logo, (pad, pad))
    img.alpha_composite(plate, ((side - plate.width) // 2, (side - plate.height) // 2))
    return img


def qr_panel(side):
    frame = int(side * 0.08)
    panel = Image.new("RGBA", (side + frame * 2, side + frame * 2), (0, 0, 0, 0))
    ImageDraw.Draw(panel).rounded_rectangle([0, 0, panel.width - 1, panel.height - 1], radius=frame * 2, fill="white")
    panel.alpha_composite(qr_image(side), (frame, frame))
    return panel


def gradient(w, h):
    img = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(img)
    for y in range(h):
        t = y / h
        d.line([(0, y), (w, y)], fill=tuple(int(a + (b - a) * t) for a, b in zip(NAVY_DARK, (26, 53, 96))))
    return img


def centered(d, w, y, text, f, fill):
    tw = d.textlength(text, font=f)
    d.text(((w - tw) / 2, y), text, font=f, fill=fill)


def card():
    w, h = 1080, 1350
    img = gradient(w, h).convert("RGBA")
    d = ImageDraw.Draw(img)
    centered(d, w, 90, "Scan to visit", font(64), (255, 255, 255))
    centered(d, w, 172, "stakichwebsites.com", font(58), ORANGE)
    panel = qr_panel(700)
    img.alpha_composite(panel, ((w - panel.width) // 2, 300))
    centered(d, w, 1170, "Stakich Websites", font(52), (255, 255, 255))
    centered(d, w, 1240, "Trusted websites at a fair price", font(36, bold=False), SKY)
    img.convert("RGB").save(OUT / "stakichwebsites-qr.png", optimize=True)


def ease(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def video(seconds=9, fps=30):
    w, h = 1080, 1920
    base = gradient(w, h).convert("RGBA")
    panel = qr_panel(720)
    glow = Image.new("RGBA", (panel.width + 160, panel.height + 160), (0, 0, 0, 0))
    ImageDraw.Draw(glow).rounded_rectangle([60, 60, glow.width - 60, glow.height - 60], radius=120, fill=ORANGE + (255,))
    glow = glow.filter(ImageFilter.GaussianBlur(40))
    f_big, f_mid, f_small = font(92), font(64), font(44, bold=False)
    out = OUT / "stakichwebsites-qr-tiktok.mp4"
    cmd = [
        imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}", "-r", str(fps), "-i", "-",
        "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
        "-shortest", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high", "-crf", "20",
        "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", str(out),
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(seconds * fps):
        t = i / fps
        img = base.copy()
        d = ImageDraw.Draw(img)
        a = ease(t / 0.6)
        if a > 0:
            layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
            ld = ImageDraw.Draw(layer)
            centered(ld, w, 210 + (1 - a) * 40, "Need a website?", f_big, (255, 255, 255, int(255 * a)))
            centered(ld, w, 330 + (1 - a) * 40, "Scan me with your camera", f_mid, ORANGE + (int(255 * a),))
            img.alpha_composite(layer)
        s = ease((t - 0.4) / 0.8)
        if s > 0:
            pulse = 1 + 0.025 * math.sin(max(0, t - 1.2) * 2 * math.pi / 1.6)
            scale = (0.6 + 0.4 * s) * pulse
            gw = int(glow.width * scale)
            g = glow.resize((gw, gw), Image.BILINEAR)
            g.putalpha(g.getchannel("A").point(lambda v: int(v * s * (0.55 + 0.25 * math.sin(t * 3)))))
            img.alpha_composite(g, ((w - gw) // 2, 520 + (panel.height - gw) // 2))
            pw = int(panel.width * scale)
            p = panel.resize((pw, pw), Image.NEAREST if scale >= 0.99 else Image.BILINEAR)
            img.alpha_composite(p, ((w - pw) // 2, 520 + (panel.height - pw) // 2))
        b = ease((t - 1.6) / 0.6)
        if b > 0:
            layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
            ld = ImageDraw.Draw(layer)
            centered(ld, w, 1470, "stakichwebsites.com", f_mid, (255, 255, 255, int(255 * b)))
            centered(ld, w, 1560, "Trusted websites at a fair price", f_small, SKY + (int(255 * b),))
            centered(ld, w, 1640, "Starter $199 + $49/mo  ·  No contract", f_small, ORANGE + (int(255 * b),))
            img.alpha_composite(layer)
        proc.stdin.write(img.convert("RGB").tobytes())
    proc.stdin.close()
    proc.wait()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    card()
    video()
    print("wrote assets/qr/stakichwebsites-qr.png and stakichwebsites-qr-tiktok.mp4")


if __name__ == "__main__":
    main()

"""Create localized Open Graph images from the existing POLIS cover art.

Usage: python tools/render_og.py
Requires Pillow, and does not modify the source artwork.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
WIDTH, HEIGHT = 1200, 630
GOLD = (225, 192, 139, 255)
CREAM = (243, 237, 219, 255)


def font(size: int, bold: bool = False):
    preferred = (
        "/usr/share/fonts/truetype/lato/Lato-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/lato/Lato-Regular.ttf"
    )
    try:
        return ImageFont.truetype(preferred, size)
    except OSError:
        return ImageFont.truetype("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf", size)


def render_og(locale: str, title: str, tagline: str):
    with Image.open(ASSETS / "cover-art.webp") as source:
        art = source.convert("RGB")
    # Crop from the bottom to preserve the dominant POLIS wordmark in the original art.
    scaled_h = round(art.height * WIDTH / art.width)
    art = art.resize((WIDTH, scaled_h), Image.Resampling.LANCZOS)
    frame = art.crop((0, 0, WIDTH, HEIGHT)).convert("RGBA")

    overlay = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Small cartographic masthead, kept well clear of the original art's POLIS title.
    draw.rounded_rectangle((31, 24, 253, 69), radius=8,
                           fill=(7, 20, 31, 218), outline=(208, 171, 111, 190), width=1)
    draw.ellipse((47, 40, 60, 53), outline=GOLD, width=2)
    draw.line((53, 36, 53, 57), fill=GOLD, width=1)
    draw.line((43, 46, 64, 46), fill=GOLD, width=1)
    draw.text((76, 34), title, font=font(20, bold=True), fill=GOLD)

    # Legible descriptor at thumbnail size, without replacing the cover's title.
    top = 552
    for y in range(top, HEIGHT):
        alpha = int(182 + 35 * ((y - top) / (HEIGHT - top)))
        draw.line((0, y, WIDTH, y), fill=(5, 17, 29, alpha))
    draw.line((41, 553, WIDTH - 42, 553), fill=(222, 186, 126, 177), width=1)
    draw.text((43, 572), tagline, font=font(29, bold=True), fill=CREAM)
    draw.text((WIDTH - 122, 583), f"{locale} · V6", font=font(15, bold=True), fill=GOLD)

    final = Image.alpha_composite(frame, overlay).convert("RGB")
    output = ASSETS / f"og-cover-{locale.lower()}.png"
    final.save(output, format="PNG", optimize=True)
    print(f"Created {output.relative_to(ROOT)} ({WIDTH}×{HEIGHT})")


if __name__ == "__main__":
    render_og("PT", "DOCUMENTAÇÃO", "Entregas de software verificáveis")
    render_og("EN", "DOCUMENTATION", "Verifiable software delivery")

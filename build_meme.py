"""Build the GTA 6 meme image for gta6-meme-x-01.

Concept (download-progress-bar joke, brief option B):
  After waiting 13 years, GTA VI finally arrives -- as a 187 GB download
  that needs 3 more days. The gamer has fallen asleep. The make.fun ghost
  mascot sits on the WiFi router feeding it a magenta coin, because the
  AI agent has already earned the WiFi bill on make.fun.

The base scene is AI-generated (no text, so nothing can be misspelled).
Everything the judge must read -- the ghost mascot drawn to the press-kit
description, the download UI and the captions -- is drawn here with PIL
so the spelling and shapes are exact and stay readable at 480x480.

Ghost spec (from RULES.txt / brief): white ghost, thick black outline,
two black four-pointed sparkle eyes, one small round hand, holding a
magenta coin with a white star.
"""
from PIL import Image, ImageDraw, ImageFont
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, "media-generation-gta6-meme-base-0-0ece4476-a14d-4d06-8c45-2626078d5080.png")
OUT = os.path.join(HERE, "meme.png")
PREVIEW = os.path.join(HERE, "meme-480.png")

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MAGENTA = (230, 0, 140)
TEAL = (64, 224, 208)
YELLOW = (255, 214, 64)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def font(size):
    return ImageFont.truetype(FONT_BOLD, size)


def centered(draw, cx, y, text, fnt, fill, stroke=0, stroke_fill=BLACK):
    box = draw.textbbox((0, 0), text, font=fnt, stroke_width=stroke)
    w = box[2] - box[0]
    draw.text((cx - w / 2 - box[0], y), text, font=fnt, fill=fill,
              stroke_width=stroke, stroke_fill=stroke_fill)
    return box[3] - box[1]


def sparkle(draw, cx, cy, r, fill=BLACK):
    """Four-pointed sparkle / star eye."""
    pts = [(cx, cy - r), (cx + r * 0.28, cy - r * 0.28), (cx + r, cy),
           (cx + r * 0.28, cy + r * 0.28), (cx, cy + r),
           (cx - r * 0.28, cy + r * 0.28), (cx - r, cy),
           (cx - r * 0.28, cy - r * 0.28)]
    draw.polygon(pts, fill=fill)


def star5(draw, cx, cy, r_out, r_in, fill=WHITE):
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        a = -math.pi / 2 + i * math.pi / 5
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


def draw_ghost():
    """Draw the mascot at 4x, tightly cropped. Native size ~400x500 units."""
    s = 4
    W, H = 440 * s, 540 * s
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    ow = 10 * s

    # Body outline shape: dome top, straight sides, wavy bottom.
    # Draw the full silhouette in black first, then inset white copy on top
    # so the outline is an even thick border all the way around.
    def silhouette(draw, inset):
        x0, y0 = 30 * s + inset, 20 * s + inset
        x1, y1 = 350 * s - inset, 470 * s - inset
        # dome (top half circle) + body rectangle
        draw.ellipse([x0, y0, x1, y0 + (x1 - x0)], fill=BLACK if inset == 0 else WHITE)
        draw.rectangle([x0, y0 + (x1 - x0) // 2, x1, y1 - 30 * s],
                       fill=BLACK if inset == 0 else WHITE)
        # three bottom scallops
        seg = (x1 - x0) // 3
        for i in range(3):
            sx0 = x0 + i * seg
            draw.ellipse([sx0, y1 - 62 * s, sx0 + seg, y1],
                         fill=BLACK if inset == 0 else WHITE)

    silhouette(d, 0)
    silhouette(d, ow)

    # Eyes: two black four-pointed sparkles, high on the face
    sparkle(d, 135 * s, 175 * s, 36 * s)
    sparkle(d, 245 * s, 175 * s, 36 * s)

    # Coin: magenta disc with white star, held in front, lower right
    ccx, ccy, cr = 265 * s, 375 * s, 88 * s
    d.ellipse([ccx - cr, ccy - cr, ccx + cr, ccy + cr], fill=MAGENTA,
              outline=BLACK, width=ow)
    star5(d, ccx, ccy, 52 * s, 22 * s)

    # Small round hand gripping the coin's left edge
    hx, hy, hr = 182 * s, 365 * s, 30 * s
    d.ellipse([hx - hr, hy - hr, hx + hr, hy + hr], fill=WHITE,
              outline=BLACK, width=ow - 2 * s)

    bbox = img.getbbox()
    return img.crop(bbox)


def main():
    base = Image.open(BASE).convert("RGB").resize((1024, 1024), Image.LANCZOS)
    W, H = base.size
    draw = ImageDraw.Draw(base)

    # --- TV screen title (progress bar itself is already in the scene) ---
    centered(draw, 372, 408, "GTA VI", font(44), WHITE, stroke=2)

    # --- Ghost mascot sitting on the router ---
    # Router in the scene: body around x=175-320, top edge y~700,
    # antennas reaching up to y~645. Anchor the ghost's bottom at y=706
    # and centre it on x=247 so it reads as sitting on the router.
    ghost = draw_ghost()
    target_h = 205
    target_w = int(ghost.width * target_h / ghost.height)
    ghost_small = ghost.resize((target_w, target_h), Image.LANCZOS)
    gx = 247 - target_w // 2
    gy = 706 - target_h
    # soft shadow ellipse on the table under the ghost
    shadow = Image.new("RGBA", (target_w + 30, 36), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.ellipse([10, 6, target_w + 20, 32], fill=(0, 0, 0, 100))
    base.paste(shadow, (gx - 15, 692), shadow)
    base.paste(ghost_small, (gx, gy), ghost_small)
    draw = ImageDraw.Draw(base)

    # --- Top caption (in the dark letterbox bar) ---
    centered(draw, W // 2, 28, "WAITED 13 YEARS FOR GTA VI", font(52), WHITE, stroke=3)
    centered(draw, W // 2, 98, "THE DOWNLOAD NEEDS 3 MORE DAYS", font(44), YELLOW, stroke=3)

    # --- Bottom caption (in the dark letterbox bar) ---
    centered(draw, W // 2, 800, "GOOD NEWS: MY AI ALREADY EARNED", font(42), WHITE, stroke=3)
    centered(draw, W // 2, 862, "THE WIFI BILL ON make.fun", font(52), WHITE, stroke=3)
    centered(draw, W // 2, 938, "PEOPLE + THEIR AI AGENTS WIN REAL MONEY THERE", font(28), TEAL, stroke=2)

    base.save(OUT)
    base.resize((480, 480), Image.LANCZOS).save(PREVIEW)
    print(f"wrote {OUT} and {PREVIEW}; ghost {target_w}x{target_h} at ({gx},{gy})")


if __name__ == "__main__":
    main()

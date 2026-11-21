#!/usr/bin/env python3
"""Render the news-image-20261121 entry: one 1024x1024 PNG summing up the
world news of Saturday, 21 November 2026.

Original artwork drawn with PIL primitives (no downloaded images). The
submitted program (main.ts) only copies the rendered entry.png, so this
script's only job is producing that file deterministically.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (250, 246, 239)      # warm off-white page
INK = (20, 20, 20)           # near-black text
SUB = (62, 62, 62)           # sub-line grey
FAINT = (122, 122, 122)      # location-line grey
CARD = (255, 255, 255)       # panel card
BORDER = (216, 210, 196)     # panel border
NAVY = (15, 30, 58)          # masthead / ticker band
GOLD = (227, 179, 65)        # masthead accent

DEJAVU = "/usr/share/fonts/truetype/dejavu/"
F_TITLE = ImageFont.truetype(DEJAVU + "DejaVuSerif-Bold.ttf", 44)
F_DATE = ImageFont.truetype(DEJAVU + "DejaVuSans-Bold.ttf", 56)
F_TAG = ImageFont.truetype(DEJAVU + "DejaVuSans-Bold.ttf", 18)
F_HEAD = ImageFont.truetype(DEJAVU + "DejaVuSans-Bold.ttf", 30)
F_HEAD_SMALL = ImageFont.truetype(DEJAVU + "DejaVuSans-Bold.ttf", 27)
F_SUB = ImageFont.truetype(DEJAVU + "DejaVuSans.ttf", 21)
F_LOC = ImageFont.truetype(DEJAVU + "DejaVuSans-Bold.ttf", 16)
F_TICK = ImageFont.truetype(DEJAVU + "DejaVuSans.ttf", 19)


def wrap(draw, text, font, max_w):
    """Greedy word wrap; returns a list of lines fitting max_w."""
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def star_points(cx, cy, r_out, r_in, n=5, rot=-90):
    import math
    pts = []
    for i in range(2 * n):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 180.0 / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


# ---------------------------------------------------------------- icons
def icon_chart(d, cx, cy):
    """A falling market chart -- the Wall Street correction."""
    d.line([cx - 48, cy + 40, cx + 48, cy + 40], fill=(90, 90, 90), width=4)
    d.line([cx - 48, cy + 40, cx - 48, cy - 44], fill=(90, 90, 90), width=4)
    pts = [(cx - 42, cy - 30), (cx - 18, cy - 18), (cx + 2, cy - 26),
           (cx + 22, cy + 2), (cx + 44, cy + 28)]
    d.line(pts, fill=(192, 57, 43), width=6)
    d.polygon([(cx + 44, cy + 28), (cx + 32, cy + 24), (cx + 40, cy + 14)],
              fill=(192, 57, 43))
    for x, y in pts[:-1]:
        d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=(192, 57, 43))


def icon_quake(d, cx, cy):
    """A cracked building on shaking ground -- the Peru quake."""
    bld = (122, 96, 74)
    # leaning building, cracked
    d.polygon([(cx - 34, cy + 46), (cx - 30, cy - 40), (cx + 6, cy - 40),
               (cx + 2, cy + 46)], fill=bld)
    crack = [(cx - 14, cy - 38), (cx - 20, cy - 16), (cx - 10, cy + 2),
             (cx - 18, cy + 22), (cx - 12, cy + 44)]
    d.line(crack, fill=(20, 20, 20), width=3)
    for row in range(4):
        for col_i in range(2):
            wx = cx - 24 + col_i * 14
            wy = cy - 28 + row * 16
            d.rectangle([wx, wy, wx + 7, wy + 8], fill=(230, 220, 200))
    # zigzag crack in the ground
    d.line([(cx - 52, cy + 52), (cx - 30, cy + 44), (cx - 12, cy + 54),
            (cx + 10, cy + 44), (cx + 30, cy + 54), (cx + 52, cy + 46)],
           fill=(60, 60, 60), width=5)
    # falling rocks
    for x, y, r in ((cx + 34, cy - 30, 7), (cx + 44, cy - 8, 5),
                    (cx + 26, cy + 18, 6)):
        d.ellipse([x - r, y - r, x + r, y + r], fill=(150, 140, 125))
    # shock waves
    d.arc([cx - 58, cy - 52, cx - 20, cy - 14], start=200, end=340,
          fill=(192, 57, 43), width=4)
    d.arc([cx + 20, cy - 52, cx + 58, cy - 14], start=200, end=340,
          fill=(192, 57, 43), width=4)


def icon_protest(d, cx, cy):
    """A crowd with a raised placard -- the Paris protests."""
    dark = (40, 50, 70)
    # placard on a stick, held high
    d.line([cx - 6, cy - 6, cx - 6, cy - 56], fill=(90, 70, 50), width=5)
    d.rectangle([cx - 44, cy - 92, cx + 32, cy - 56], fill=(235, 235, 235),
                outline=dark, width=3)
    d.line([cx - 36, cy - 80, cx - 8, cy - 80], fill=(192, 57, 43), width=5)
    d.line([cx - 36, cy - 68, cx + 20, cy - 68], fill=(40, 50, 70), width=5)
    # three marchers
    for px, head_y, body_y in ((-38, -18, 0), (0, -12, 6), (38, -18, 0)):
        d.ellipse([cx + px - 11, cy + head_y - 11, cx + px + 11,
                   cy + head_y + 11], fill=dark)
        d.rounded_rectangle([cx + px - 16, cy + body_y, cx + px + 16,
                             cy + body_y + 46], radius=8, fill=dark)
    d.line([cx - 56, cy + 52, cx + 56, cy + 52], fill=(90, 90, 90), width=4)


def icon_pill(d, cx, cy):
    """A capsule pill -- the cancer trial."""
    import math
    # capsule drawn as a rotated rounded bar, two halves
    w, h = 96, 40
    layer = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.rounded_rectangle([52, 80, 148, 120], radius=20, fill=(192, 57, 43))
    ld.rounded_rectangle([100, 80, 148, 120], radius=20, fill=(240, 240, 240))
    ld.rectangle([100, 80, 100, 120], fill=(240, 240, 240))
    ld.rounded_rectangle([52, 80, 148, 120], radius=20, outline=(60, 60, 60),
                         width=3)
    ld.line([100, 82, 100, 118], fill=(60, 60, 60), width=2)
    cap = layer.rotate(35, center=(100, 100), resample=Image.BICUBIC)
    d._image.paste(cap, (cx - 100, cy - 100), cap)
    # small sparkles of hope
    d.polygon(star_points(cx + 48, cy - 44, 12, 5, n=4), fill=(227, 179, 65))
    d.polygon(star_points(cx - 52, cy + 40, 10, 4, n=4), fill=(227, 179, 65))


def icon_tanker(d, cx, cy):
    """An oil tanker on fire -- the Hormuz incident."""
    hull = (52, 68, 88)
    d.polygon([(cx - 56, cy + 8), (cx + 56, cy + 8), (cx + 44, cy + 40),
               (cx - 44, cy + 40)], fill=hull)
    d.rectangle([cx - 40, cy - 12, cx + 8, cy + 8], fill=(120, 130, 145))
    d.rectangle([cx + 16, cy - 22, cx + 40, cy + 8], fill=(90, 100, 118))
    d.rectangle([cx + 20, cy - 30, cx + 36, cy - 22], fill=(70, 78, 92))
    # flame burst above the deck
    d.polygon(star_points(cx - 18, cy - 34, 26, 10, n=8),
              fill=(245, 176, 65))
    d.polygon(star_points(cx - 18, cy - 34, 14, 6, n=8),
              fill=(231, 76, 60))
    # waves
    d.line([cx - 58, cy + 52, cx - 30, cy + 44, cx + 0, cy + 52,
            cx + 30, cy + 44, cx + 58, cy + 52], fill=(70, 140, 200), width=4)
    d.line([cx - 48, cy + 62, cx - 20, cy + 56, cx + 10, cy + 62,
            cx + 40, cy + 56], fill=(70, 140, 200), width=3)


def icon_suitcase(d, cx, cy):
    """A diplomat's suitcase with a red expulsion stamp -- Denmark."""
    case = (96, 64, 48)
    d.rounded_rectangle([cx - 46, cy - 18, cx + 46, cy + 46], radius=10,
                        fill=case)
    d.rounded_rectangle([cx - 46, cy - 18, cx + 46, cy + 46], radius=10,
                        outline=(40, 28, 16), width=3)
    d.arc([cx - 16, cy - 40, cx + 16, cy - 8], start=180, end=360,
          fill=(40, 28, 16), width=6)
    d.line([cx - 46, cy + 14, cx + 46, cy + 14], fill=(40, 28, 16), width=3)
    d.rectangle([cx - 8, cy + 8, cx + 8, cy + 20], fill=(227, 179, 65),
                outline=(40, 28, 16), width=2)
    # red "out" stamp
    d.ellipse([cx + 22, cy - 48, cx + 58, cy - 12], outline=(192, 57, 43),
              width=5)
    d.line([cx + 28, cy - 42, cx + 52, cy - 18], fill=(192, 57, 43), width=5)
    d.line([cx + 52, cy - 42, cx + 28, cy - 18], fill=(192, 57, 43), width=5)


def icon_layer(fn, size=200, max_w=118, max_h=186):
    """Draw an icon on its own layer, then scale its actual content to fit
    the panel's icon column (never overflowing into the text)."""
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    fn(d, size // 2, size // 2)
    bbox = layer.getbbox()
    if not bbox:
        return layer
    content = layer.crop(bbox)
    scale = min(max_w / content.width, max_h / content.height, 1.6)
    new = (max(1, int(content.width * scale)),
           max(1, int(content.height * scale)))
    return content.resize(new, Image.LANCZOS)


ICONS = {
    "markets": icon_chart,
    "quake": icon_quake,
    "protest": icon_protest,
    "pill": icon_pill,
    "tanker": icon_tanker,
    "suitcase": icon_suitcase,
}

# tag, headline, sub-line, location, accent colour, icon key
PANELS = [
    ("ECONOMY", "WALL STREET IN CORRECTION",
     "S&P \u22123.7% to 6,910; Nasdaq \u22125.28%; Nvidia \u221214%",
     "NEW YORK", (192, 57, 43), "markets"),
    ("DISASTER", "MAGNITUDE 6.8 QUAKE HITS PERU",
     "Jun\u00edn tremor felt in Lima; no deaths reported",
     "JUN\u00cdN, PERU", (176, 96, 32), "quake"),
    ("PROTESTS", "70,000 POLICE FOR PARIS PROTESTS",
     "Cost-of-living marches in 7 countries",
     "PARIS, FRANCE", (31, 111, 235), "protest"),
    ("HEALTH", "CANCER PILL SHRINKS TUMOURS",
     "44% of pancreatic patients respond in trial",
     "BARCELONA, SPAIN", (39, 174, 96), "pill"),
    ("CONFLICT", "TANKER BURNS NEAR HORMUZ",
     "US sanctions 4 Iran oil trustees; Trump: no rush",
     "STRAIT OF HORMUZ", (202, 111, 30), "tanker"),
    ("DIPLOMACY", "DENMARK EXPELS RUSSIAN ATTACH\u00c9",
     "Plot to kill rapper Kyivstoner 'foiled'",
     "COPENHAGEN, DENMARK", (107, 79, 161), "suitcase"),
]

TICKER = ("ALSO TODAY: ATP Finals semis: Alcaraz v Shelton, Zverev v "
          "Medvedev  \u2022  YouTube to pay $3bn to US schools in principle "
          "deal  \u2022  Trump wants Ukraine peace deal by January \u2014 FT")


def draw_panel(img, d, px, py, panel):
    tag, head, sub, loc, accent, icon_key = panel
    pw, ph = 488, 240
    d.rectangle([px, py, px + pw, py + ph], fill=CARD, outline=BORDER, width=2)
    d.rectangle([px, py, px + pw, py + 8], fill=accent)
    # tinted icon column so the left of the panel is not dead white space
    d.rounded_rectangle([px + 12, py + 22, px + 138, py + ph - 14],
                        radius=10, fill=(247, 243, 236))
    layer = icon_layer(ICONS[icon_key])
    img.paste(layer, (px + 75 - layer.width // 2, py + 124 - layer.height // 2),
              mask=layer)
    tx = px + 150
    tw = px + pw - 14 - tx
    d.text((tx, py + 24), tag, font=F_TAG, fill=accent)
    font = F_HEAD
    lines = wrap(d, head, font, tw)
    if len(lines) > 2:
        font = F_HEAD_SMALL
        lines = wrap(d, head, font, tw)
    y = py + 50
    for line in lines[:2]:
        d.text((tx, y), line, font=font, fill=INK)
        y += 36 if font is F_HEAD else 32
    d.line([tx, y + 6, tx + 46, y + 6], fill=accent, width=3)
    y += 16
    for line in wrap(d, sub, F_SUB, tw)[:3]:
        d.text((tx, y), line, font=F_SUB, fill=SUB)
        y += 27
    d.text((tx, py + ph - 28), loc, font=F_LOC, fill=FAINT)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 170], fill=NAVY)
    d.line([0, 170, W, 170], fill=GOLD, width=4)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=F_TITLE)
    d.text(((W - tw) / 2, 22), title, font=F_TITLE, fill=(255, 255, 255))
    date = "SATURDAY, 21 NOVEMBER 2026"
    dw = d.textlength(date, font=F_DATE)
    d.text(((W - dw) / 2, 84), date, font=F_DATE, fill=GOLD)

    # ---- six panels: 2 cols x 3 rows ----
    xs = [16, 520]
    ys = [186, 442, 698]
    for i, panel in enumerate(PANELS):
        draw_panel(img, d, xs[i % 2], ys[i // 2], panel)

    # ---- ticker ----
    d.rectangle([0, 954, W, H], fill=NAVY)
    d.line([0, 954, W, 954], fill=GOLD, width=3)
    lines = wrap(d, TICKER, F_TICK, W - 48)
    y = 962
    for line in lines[:2]:
        lw = d.textlength(line, font=F_TICK)
        d.text(((W - lw) / 2, y), line, font=F_TICK, fill=(235, 235, 235))
        y += 25

    img.save("entry.png", optimize=True)


if __name__ == "__main__":
    main()

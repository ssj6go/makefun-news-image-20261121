"""Draw the news-image-20261121 entry: one 1024x1024 newspaper-style image
summing up Saturday 21 November 2026.

Everything is drawn from scratch with PIL (stdlib + PIL only). No randomness,
no network, no external assets: running this script twice produces
byte-identical PNG output.

Layout: a navy masthead naming the day, six story panels in a 2x3 grid
(each with a drawn scene, a headline and a sub-line), and a two-line
ticker strip along the bottom.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
HERE = Path(__file__).resolve().parent
OUT = HERE / "entry.png"

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
SANS = FONT_DIR / "DejaVuSans.ttf"
SANS_BOLD = FONT_DIR / "DejaVuSans-Bold.ttf"

NAVY = (15, 30, 51)
GOLD = (242, 193, 78)
BACKGROUND = (232, 228, 216)
PAPER = (251, 250, 246)
PANEL_EDGE = (217, 210, 192)
INK = (20, 20, 20)
SUB_INK = (68, 68, 68)
WHITE = (255, 255, 255)

MASTHEAD_H = 112
TICKER_H = 76
MARGIN = 14
GAP = 12


def font(size, bold=False):
    return ImageFont.truetype(str(SANS_BOLD if bold else SANS), size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns the lines that fit inside max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- scenes
# Each scene draws inside a box (x, y, w, h) and never outside it.

def scene_economy(d, x, y, w, h):
    """A falling market line over a grid, with the day's drop in red."""
    d.rounded_rectangle([x, y, x + w, y + h], radius=6, fill=(238, 243, 246))
    for gy in (y + 28, y + 56, y + 84):
        d.line([x + 10, gy, x + w - 10, gy], fill=(210, 220, 228), width=1)
    pts = [(x + 18, y + 14), (x + 62, y + 30), (x + 106, y + 24),
           (x + 150, y + 50), (x + 194, y + 62), (x + 238, y + 88)]
    d.line(pts, fill=(179, 38, 30), width=4, joint="curve")
    cx = x + w - 88
    d.polygon([(cx - 13, y + 26), (cx + 13, y + 26), (cx, y + 50)],
              fill=(179, 38, 30))
    d.text((cx, y + 56), "-3.7%", font=font(30, bold=True),
           fill=(179, 38, 30), anchor="ma")


def scene_quake(d, x, y, w, h):
    """Two buildings on shaking ground; one is cracked, rocks are falling."""
    d.rounded_rectangle([x, y, x + w, y + h], radius=6, fill=(220, 232, 239))
    ground_y = y + h - 26
    d.rectangle([x, ground_y + 6, x + w, y + h], fill=(201, 177, 138))
    wave = [(x + i, ground_y + (4 if (i // 12) % 2 else -4))
            for i in range(0, w + 1, 12)]
    d.line(wave, fill=(150, 124, 82), width=3)
    d.rectangle([x + 30, y + 26, x + 110, ground_y + 6], fill=(139, 154, 168))
    d.rectangle([x + 130, y + 44, x + 200, ground_y + 6], fill=(168, 182, 194))
    for row in range(3):
        for col in range(2):
            d.rectangle([x + 42 + col * 30, y + 36 + row * 18,
                         x + 56 + col * 30, y + 46 + row * 18],
                        fill=(60, 75, 88))
    for row in range(2):
        for col in range(2):
            d.rectangle([x + 140 + col * 28, y + 54 + row * 16,
                         x + 152 + col * 28, y + 62 + row * 16],
                        fill=(90, 104, 116))
    crack = [(x + 70, y + 26), (x + 64, y + 44), (x + 74, y + 62),
             (x + 66, y + 78), (x + 72, ground_y)]
    d.line(crack, fill=(30, 30, 30), width=2)
    for rx, ry, r in [(x + 300, y + 30, 7), (x + 360, y + 54, 9),
                      (x + 420, y + 26, 6)]:
        d.line([rx - 16, ry - 14, rx - 6, ry - 5], fill=(120, 100, 80), width=2)
        d.ellipse([rx - r, ry - r, rx + r, ry + r], fill=(120, 100, 80))
    d.text((x + w - 14, ground_y - 12), "M 6.8", font=font(24, bold=True),
           fill=(122, 74, 18), anchor="rb")


def scene_protest(d, x, y, w, h):
    """A street crowd with placards, police shields, and the Eiffel Tower."""
    d.rounded_rectangle([x, y, x + w, y + h], radius=6, fill=(244, 234, 214))
    base = y + h - 8
    tx = x + w - 120
    d.line([tx, base, tx + 55, y + 10], fill=(107, 93, 79), width=5)
    d.line([tx + 110, base, tx + 55, y + 10], fill=(107, 93, 79), width=5)
    d.line([tx + 55, y + 2, tx + 55, y + 12], fill=(107, 93, 79), width=3)
    d.line([tx + 18, base - 34, tx + 92, base - 34], fill=(107, 93, 79), width=4)
    d.line([tx + 30, base - 62, tx + 80, base - 62], fill=(107, 93, 79), width=3)
    colors = [(179, 38, 30), (31, 78, 121), (30, 122, 70),
              (200, 140, 40), (91, 58, 142), (40, 40, 40)]
    for i, c in enumerate(colors):
        fx = x + 24 + i * 34
        fy = base - 14 - (6 if i % 2 else 0)
        d.ellipse([fx - 7, fy - 22, fx + 7, fy - 8], fill=(232, 190, 150))
        d.rounded_rectangle([fx - 8, fy - 8, fx + 8, fy + 14],
                            radius=5, fill=c)
        if i % 2 == 0:
            d.line([fx + 8, fy - 6, fx + 18, fy - 26], fill=(90, 90, 90), width=2)
            d.rectangle([fx + 10, fy - 40, fx + 30, fy - 26],
                        fill=WHITE, outline=(90, 90, 90))
    for i in range(4):
        sx = x + 230 + i * 24
        d.rounded_rectangle([sx, base - 22, sx + 20, base],
                            radius=4, fill=(47, 85, 151))


def scene_health(d, x, y, w, h):
    """A capsule, then a tumour shrinking from large to small."""
    d.rounded_rectangle([x, y, x + w, y + h], radius=6, fill=(230, 243, 234))
    cy = y + h // 2
    cx0, cy0, cx1, cy1 = x + 24, cy - 20, x + 170, cy + 20
    d.rounded_rectangle([cx0, cy0, cx1, cy1], radius=20,
                        fill=WHITE, outline=(150, 150, 150), width=2)
    d.rounded_rectangle([cx0, cy0, cx0 + 73, cy1], radius=20, fill=(214, 69, 65))
    d.rectangle([cx0 + 53, cy0, cx0 + 73, cy1], fill=(214, 69, 65))
    ax0, ax1 = x + 196, x + 244
    d.line([ax0, cy, ax1, cy], fill=(30, 122, 70), width=4)
    d.polygon([(ax1, cy - 10), (ax1, cy + 10), (ax1 + 14, cy)],
              fill=(30, 122, 70))
    d.ellipse([x + 288, cy - 30, x + 348, cy + 30], fill=(154, 165, 173))
    bx0, bx1 = x + 358, x + 382
    d.line([bx0, cy, bx1, cy], fill=(30, 122, 70), width=3)
    d.polygon([(bx1, cy - 7), (bx1, cy + 7), (bx1 + 9, cy)], fill=(30, 122, 70))
    d.ellipse([x + 400, cy - 13, x + 426, cy + 13], fill=(30, 122, 70))


def scene_tanker(d, x, y, w, h):
    """A tanker burning at dusk, smoke rising over the sea."""
    d.rounded_rectangle([x, y, x + w, y + h], radius=6, fill=(247, 232, 216))
    sea_y = y + h - 34
    d.rectangle([x, sea_y, x + w, y + h], fill=(31, 78, 121))
    for wx in range(x + 10, x + w - 10, 46):
        d.arc([wx, sea_y + 8, wx + 34, sea_y + 26], start=180, end=360,
              fill=WHITE, width=2)
    d.polygon([(x + 60, sea_y - 6), (x + 380, sea_y - 6),
               (x + 360, sea_y + 18), (x + 80, sea_y + 18)], fill=(34, 49, 64))
    d.rectangle([x + 300, sea_y - 30, x + 350, sea_y - 6], fill=(240, 240, 240))
    d.rectangle([x + 320, sea_y - 42, x + 336, sea_y - 30], fill=(180, 40, 40))
    for fx, fh, col in [(x + 150, 34, (249, 115, 22)),
                        (x + 180, 44, (250, 204, 21)),
                        (x + 210, 30, (249, 115, 22))]:
        d.polygon([(fx - 12, sea_y - 6), (fx, sea_y - 6 - fh),
                   (fx + 12, sea_y - 6)], fill=col)
    for sx, sy, r in [(x + 170, sea_y - 52, 9), (x + 195, sea_y - 60, 10),
                      (x + 220, sea_y - 52, 8)]:
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(120, 120, 120))


def scene_diplomacy(d, x, y, w, h):
    """The Danish flag, the Russian flag, and an exit arrow to the door."""
    d.rounded_rectangle([x, y, x + w, y + h], radius=6, fill=(240, 236, 226))
    base = y + h - 10
    for px in (x + 60, x + 210):
        d.line([px, y + 14, px, base], fill=(90, 90, 90), width=3)
        d.ellipse([px - 4, y + 8, px + 4, y + 16], fill=(90, 90, 90))
    fx, fy, fw, fh = x + 64, y + 16, 84, 52
    d.rectangle([fx, fy, fx + fw, fy + fh], fill=(198, 12, 48))
    d.rectangle([fx + 26, fy, fx + 38, fy + fh], fill=WHITE)
    d.rectangle([fx, fy + 20, fx + fw, fy + 32], fill=WHITE)
    fx2 = x + 214
    d.rectangle([fx2, fy, fx2 + fw, fy + 17], fill=WHITE, outline=(160, 160, 160))
    d.rectangle([fx2, fy + 17, fx2 + fw, fy + 35], fill=(0, 57, 166))
    d.rectangle([fx2, fy + 35, fx2 + fw, fy + fh], fill=(213, 0, 50))
    ax0, ax1, ay = x + 330, x + 400, y + 42
    d.line([ax0, ay, ax1, ay], fill=(179, 38, 30), width=5)
    d.polygon([(ax1, ay - 10), (ax1, ay + 10), (ax1 + 14, ay)],
              fill=(179, 38, 30))
    d.rectangle([x + 424, y + 16, x + 456, base], outline=(90, 90, 90), width=3)
    d.ellipse([x + 446, y + 60, x + 452, y + 66], fill=(90, 90, 90))


# ---------------------------------------------------------------- layout

PANELS = [
    ("ECONOMY", (179, 38, 30), "WALL STREET IN CORRECTION",
     "S&P −3.7% to 6,910, its 7th straight fall; Nasdaq −5.28%. "
     "Nvidia −14% after an SEC probe report.",
     scene_economy),
    ("DISASTER", (122, 74, 18), "MAGNITUDE 6.8 QUAKE HITS PERU",
     "Junín quake at 00:09 GMT, felt in Lima; rocks fell onto the "
     "Costa Verde highway. No casualties reported.",
     scene_quake),
    ("PROTESTS", (31, 78, 121), "70,000 POLICE FOR PARIS PROTESTS",
     "Paris march 14:00 République→Nation; Yellow Vests mark 8 years; "
     "500+ actions across 7 countries.",
     scene_protest),
    ("HEALTH", (30, 122, 70), "CANCER PILL SHRINKS TUMOURS",
     "ERAS-0015 shrank tumours in 44% of pancreatic cancer patients — "
     "69% in the two commonest variants.",
     scene_health),
    ("CONFLICT", (194, 65, 12), "TANKER BURNS NEAR HORMUZ",
     "Iran claims a sea mine hit the tanker; US sanctioned 4 Iranian "
     "oil officials. Trump: in no rush on Iran.",
     scene_tanker),
    ("DIPLOMACY", (91, 58, 142), "DENMARK EXPELS RUSSIAN ATTACHÉ",
     "Moscow allegedly planned to kill rapper Kyivstoner; 3 arrested, "
     "2 charged. Attaché has 7 days to leave.",
     scene_diplomacy),
]

TICKER = ("ATP Finals semis: Alcaraz v Shelton, Zverev v Medvedev  •  "
          "YouTube to pay $3bn to US schools in principle deal  •  "
          "Trump wants Ukraine peace deal by January — FT")


def draw_masthead(d):
    d.rectangle([0, 0, W, MASTHEAD_H], fill=NAVY)
    d.rectangle([0, MASTHEAD_H - 4, W, MASTHEAD_H], fill=GOLD)
    d.text((W // 2, 28), "THE WORLD IN ONE DAY",
           font=font(44, bold=True), fill=WHITE, anchor="ma")
    d.text((W // 2, 80), "SATURDAY, 21 NOVEMBER 2026",
           font=font(21, bold=True), fill=GOLD, anchor="ma")


def draw_ticker(d):
    d.rectangle([0, H - TICKER_H, W, H], fill=NAVY)
    d.rectangle([0, H - TICKER_H, W, H - TICKER_H + 3], fill=GOLD)
    items = TICKER.split("  •  ")
    for size in (18, 17, 16, 15):
        fnt = font(size)
        lines, cur = [], ""
        for item in items:
            trial = item if not cur else f"{cur}  •  {item}"
            if d.textlength(trial, font=fnt) <= W - 2 * 18:
                cur = trial
            else:
                lines.append(cur)
                cur = item
        if cur:
            lines.append(cur)
        if len(lines) <= 2:
            break
    line_h = size + 7
    y0 = H - TICKER_H + (TICKER_H - len(lines) * line_h) // 2
    for i, line in enumerate(lines):
        d.text((18, y0 + i * line_h), line, font=fnt, fill=WHITE)


def draw_panel(d, px, py, pw, ph, section, tag_color, headline, sub, scene):
    d.rounded_rectangle([px, py, px + pw, py + ph], radius=10,
                        fill=PAPER, outline=PANEL_EDGE, width=1)
    tag_font = font(15, bold=True)
    chip_w = d.textlength(section, font=tag_font) + 20
    d.rounded_rectangle([px + 12, py + 10, px + 12 + chip_w, py + 36],
                        radius=8, fill=tag_color)
    d.text((px + 22, py + 23), section, font=tag_font, fill=WHITE, anchor="lm")
    scene(d, px + 12, py + 44, pw - 24, 106)
    head_font = font(27, bold=True)
    sub_font = font(16)
    head_lines = wrap(d, headline, head_font, pw - 24)
    sub_lines = wrap(d, sub, sub_font, pw - 24)
    block = len(head_lines) * 30 + 2 + len(sub_lines) * 20
    zone_top, zone_h = py + 156, ph - 156 - 6
    y = zone_top + max(0, (zone_h - block) // 2)
    for line in head_lines:
        d.text((px + 12, y), line, font=head_font, fill=INK)
        y += 30
    y += 2
    for line in sub_lines:
        d.text((px + 12, y), line, font=sub_font, fill=SUB_INK)
        y += 20


def build():
    img = Image.new("RGB", (W, H), BACKGROUND)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    draw_ticker(d)
    col_w = (W - 2 * MARGIN - GAP) // 2
    row_h = 261
    top = MASTHEAD_H + MARGIN
    for i, (section, color, headline, sub, scene) in enumerate(PANELS):
        col, row = i % 2, i // 2
        px = MARGIN + col * (col_w + GAP)
        py = top + row * (row_h + GAP)
        draw_panel(d, px, py, col_w, row_h, section, color, headline, sub, scene)
    return img


def main():
    img = build()
    img.save(OUT, format="PNG")
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()

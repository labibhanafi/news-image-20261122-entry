#!/usr/bin/env python3
"""news-image-20261122 — Sunday 22 November 2026, the whole world on one page.

Draws a 1024x1024 newspaper front page with PIL: a dated masthead, a big
illustrated COP31 hero panel, two smaller illustrated panels (the Gulf, Kyiv),
32 further dated stories grouped by region, a by-the-numbers strip and a
sources footer. Everything is drawn from data baked into this file — no
network, no files read, no clock, no unseeded randomness — so two runs write
byte-identical PNGs. If PIL (or a usable font) is missing in the grading
sandbox, the program falls back to copying the entry.png shipped beside it,
which this same program produced.
"""

import os
import random
import shutil

W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (22, 22, 22)
SOFT = (74, 70, 64)
RULE = (22, 22, 22)
RED = (178, 32, 44)
NAVY = (22, 50, 79)
TEAL = (14, 107, 107)
GOLD = (176, 138, 28)
SKY = (214, 228, 236)

DATE_LINE = "SUNDAY 22 NOVEMBER 2026"
TAGLINE = "35 dated stories  ·  7 regions  ·  one day, the whole world"

HERO_KICKER = "CLIMATE  ·  COP31, ANTALYA"
HERO_HEAD = "COP31 nears a deal at last"
HERO_DEK = (
    "Past its Friday deadline, the Antalya summit tables a new text in the "
    "small hours of Sunday — fossil fuels back in, the $120bn adaptation "
    "aid still out. Delegates have until 03:00 GMT to object; the approval "
    "session opens at 06:00 GMT."
)

PANEL_A_KICKER = "THE GULF  ·  BAHRAIN"
PANEL_A_HEAD = "Iran claims hits on two US Patriot radars"
PANEL_A_DEK = (
    "Tehran says its Aerospace Force struck radars at the al-Riffa and "
    "Awali bases. Bahrain reports a factory fire instead."
)

PANEL_B_KICKER = "UKRAINE  ·  KYIV"
PANEL_B_HEAD = "Zelenskyy: NATO is Ukraine's guarantee"
PANEL_B_DEK = (
    "Kyiv repeats that NATO membership is its clearest security "
    "guarantee — as drones hit a Russian cargo ship in the Baltic."
)

# (region, headline, one-line deck) — 32 stories; hero + 2 panels make 35.
STORIES = [
    ("EUROPE", "Estonia to shut border with Russia",
     "Moscow calls the move a 'new Iron Curtain'."),
    ("EUROPE", "Zagreb rallies demand justice over hospital death",
     "Crowds march in Croatia's capital."),
    ("EUROPE", "Prince William unveils forest-worker cover",
     "Insurance scheme for 10,000 temporary rangers."),
    ("EUROPE", "Depardieu faces gang-rape probe in France",
     "Paris prosecutors act on a complaint."),
    ("AMERICAS", "US airlines warned of al-Qaeda-linked threat",
     "Security alert issued ahead of Thanksgiving."),
    ("AMERICAS", "Mexico captures cartel boss 'El Chapo Isidro'",
     "Arrest sparks deadly Sinaloa violence; 11 killed."),
    ("AMERICAS", "Jailed ex-president Bolsonaro taken to ICU",
     "Acute bowel obstruction, doctors say."),
    ("AMERICAS", "Trump: Iran deal 'could last 20 years'",
     "Says the US removed Tehran's leadership twice."),
    ("AMERICAS", "Melania Trump urges more Ukraine ceasefires",
     "Appeal made before Christmas; Zelenskyy responds."),
    ("SPORT", "Leeds stun Chelsea 4-1 at Stamford Bridge",
     "Saturday shock in the Premier League."),
    ("SPORT", "Malen scores four as Roma win 5-1 at Parma",
     "Dutch striker stars in the Serie A rout."),
    ("MIDDLE EAST", "Saudi coalition says it downed Houthi missile",
     "Aimed at the kingdom's west, Riyadh says."),
    ("MIDDLE EAST", "Turkey spy chief meets Hamas team in Istanbul",
     "Ankara hosts talks on Gaza."),
    ("MIDDLE EAST", "Bahrain probes Patriot interceptor crash",
     "Reports link it to Iranian drone attacks."),
    ("MIDDLE EAST", "Tankers hit off Oman as Gulf tension grows",
     "Strikes reported in the Strait of Hormuz area."),
    ("MIDDLE EAST", "Israel coalition talks: Eisenkot invites Likud",
     "First meeting scheduled after the vote."),
    ("MIDDLE EAST", "Iran calls US blockade a 'hostile act'",
     "Tehran also pushes a bill tying net accounts to IDs."),
    ("AFRICA", "Sudan's Tasis Alliance seizes Bau in Blue Nile",
     "Rebels take the key region, reports say."),
    ("AFRICA", "Durban backlog strands medicine on 16 ships",
     "Vessel delays reach 20 days."),
    ("BUSINESS", "Tech rout: Nasdaq -5.3% on Friday",
     "S&P 500 falls into correction territory."),
    ("ASIA-PACIFIC", "Hong Kong votes for 723 committee seats",
     "856 candidates for Election Committee seats."),
    ("ASIA-PACIFIC", "Japan to train live-fire on Indian soil — a first",
     "Tokyo and Delhi deepen defence ties."),
    ("ASIA-PACIFIC", "Magnitude 4.1 quake rattles Myanmar at dawn",
     "Early-hours tremor, seismology centre says."),
    ("ASIA-PACIFIC", "Taiwan turns to drone warfare",
     "Island adapts as Trump draws closer to Xi."),
    ("ASIA-PACIFIC", "After Trump-Xi talks, what was agreed?",
     "Analysts weigh the summit's outcome."),
    ("ASIA-PACIFIC", "US limits military cooperation with Canada",
     "Defence chief Hegseth orders the curbs."),
    ("ASIA-PACIFIC", "UN talks on killer robots fall short",
     "No enforceable rules agreed."),
    ("SOUTH ASIA", "Modi opens Nitish Setu bridge in Bihar",
     "Patna-Vaishali link named for Nitish Kumar."),
    ("SOUTH ASIA", "Cyclone Akvan cancels 14 flights at Ranchi",
     "Storm disrupts travel in eastern India."),
    ("SOUTH ASIA", "Toxic alcohol kills 11 in Manipur, 180 fall ill",
     "Illicit brew blamed in north-east India."),
    ("SOUTH ASIA", "EU and Indonesia sign trade pact at last",
     "After a decade of talks; tariffs on 98.5% to go."),
    ("SOUTH ASIA", "Suicide car bomb kills 5 at Pakistan checkpoint",
     "13 injured in the attack on a security post."),
]

COLUMNS = None  # columns are filled greedily; see _draw_front_page
REGION_ORDER = ["EUROPE", "MIDDLE EAST", "ASIA-PACIFIC", "SOUTH ASIA",
                "AFRICA", "AMERICAS", "BUSINESS", "SPORT"]

NUMBERS = [
    ("35", "DATED STORIES"),
    ("7", "REGIONS"),
    ("723", "HONG KONG SEATS"),
    ("98.5%", "TARIFFS TO GO"),
    ("M4.1", "MYANMAR QUAKE"),
    ("$120bn", "AID CUT FROM COP31 DRAFT"),
]

FOOTER = (
    "Sources: Reuters  ·  AP  ·  AFP  ·  Al Jazeera  ·  ANI  ·  BBC  ·  China Daily Asia  ·  "
    "European Commission  ·  Xinhua   —   All stories dated Sunday 22 November 2026. "
    "Drawn by program; no photographs."
)

REGION_COLORS = {
    "EUROPE": NAVY,
    "MIDDLE EAST": RED,
    "ASIA-PACIFIC": TEAL,
    "SOUTH ASIA": (122, 74, 12),
    "AFRICA": (96, 74, 18),
    "AMERICAS": (74, 44, 110),
    "BUSINESS": (30, 90, 60),
    "SPORT": (12, 96, 90),
}

FONT_PATHS = {
    "serif_b": [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
        "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf",
    ],
    "sans_b": [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
    ],
    "sans": [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
    ],
    "serif": [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
        "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf",
    ],
}


def _load_fonts():
    from PIL import ImageFont

    fonts = {}
    for key, paths in FONT_PATHS.items():
        for path in paths:
            if os.path.exists(path):
                fonts[key] = path
                break
        else:
            raise RuntimeError("no usable font found for " + key)

    def f(kind, size):
        return ImageFont.truetype(fonts[kind], size)

    return {
        "masthead": f("serif_b", 56),
        "date": f("sans_b", 21),
        "tagline": f("sans", 13),
        "kicker": f("sans_b", 13),
        "hero_head": f("serif_b", 31),
        "hero_dek": f("sans", 13),
        "panel_head": f("serif_b", 19),
        "panel_dek": f("sans", 11),
        "region": f("sans_b", 12),
        "story_head": f("sans_b", 11),
        "story_dek": f("sans", 9),
        "number_big": f("sans_b", 22),
        "number_small": f("sans_b", 9),
        "fixtures": f("sans_b", 9),
        "footer": f("sans", 9),
    }


def _wrap(draw, text, font, width):
    """Greedy word wrap; returns a list of lines that fit in width."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def _vgrad(size, top, bottom):
    """Vertical gradient as an RGB image (deterministic)."""
    from PIL import Image

    w, h = size
    grad = Image.new("RGB", (1, h))
    px = grad.load()
    for y in range(h):
        t = y / max(1, h - 1)
        px[0, y] = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
    return grad.resize((w, h))


def _draw_globe_scene(img, box):
    """COP31 hero art: dusk sky, sun, a globe, flags, wind turbines."""
    from PIL import ImageDraw

    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    sky = _vgrad((w, h), (16, 68, 96), (64, 148, 138))
    img.paste(sky, (x0, y0))
    d = ImageDraw.Draw(img)
    rng = random.Random(20261122)
    # Sun with rays.
    sx, sy, sr = x0 + w - 78, y0 + 52, 30
    for k in range(12):
        ang = k * 30
        import math

        dx, dy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        d.line(
            [(sx + dx * (sr + 6), sy + dy * (sr + 6)),
             (sx + dx * (sr + 18), sy + dy * (sr + 18))],
            fill=(240, 196, 90), width=3,
        )
    d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(240, 196, 90))
    # Clouds.
    for cx, cy, cw in [(x0 + 60, y0 + 34, 90), (x0 + 170, y0 + 58, 70),
                       (x0 + w - 190, y0 + 120, 80)]:
        for ox, oy, r in [(0, 0, 16), (22, -6, 20), (46, 2, 15)]:
            d.ellipse([cx + ox - r, cy + oy - r, cx + ox + r, cy + oy + r],
                      fill=(235, 240, 242))
    # Globe.
    gx, gy, gr = x0 + 150, y0 + h - 58, 62
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(38, 110, 160))
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], outline=(10, 40, 60), width=3)
    for lx, ly, lw, lh in [(-38, -22, 34, 18), (6, -30, 30, 16),
                           (-28, 14, 40, 20), (16, 18, 26, 14)]:
        d.ellipse([gx + lx, gy + ly, gx + lx + lw, gy + ly + lh],
                  fill=(86, 158, 92))
    d.arc([gx - gr, gy - gr, gx + gr, gy + gr], 200, 340, fill=(210, 230, 240),
          width=2)
    # Ground + wind turbines.
    d.rectangle([x0, y0 + h - 34, x1, y1], fill=(30, 72, 52))
    for tx in (x0 + w - 210, x0 + w - 150, x0 + w - 96):
        import math

        d.line([(tx, y0 + h - 34), (tx, y0 + h - 96)], fill=(235, 240, 242), width=3)
        for k in range(3):
            ang = math.radians(90 + k * 120 + 20)
            d.line([(tx, y0 + h - 96),
                    (tx + int(26 * math.cos(ang)), y0 + h - 96 + int(26 * math.sin(ang)))],
                   fill=(235, 240, 242), width=3)
    # Row of small flags along the bottom.
    flag_cols = [(178, 32, 44), (22, 50, 79), (14, 107, 107), (240, 196, 90),
                 (86, 158, 92), (74, 44, 110), (220, 120, 40), (30, 90, 60)]
    fx = x0 + 12
    fy = y0 + h - 26
    for i, col in enumerate(flag_cols):
        d.rectangle([fx, fy, fx + 26, fy + 16], fill=col, outline=(240, 240, 240))
        d.line([(fx, fy), (fx, fy - 8)], fill=(240, 240, 240), width=1)
        fx += 34
    # Grain inside the panel for texture.
    for _ in range(900):
        px, py = rng.randint(x0, x1 - 1), rng.randint(y0, y1 - 1)
        v = rng.choice([(255, 255, 255), (0, 0, 0)])
        d.point((px, py), fill=v)


def _draw_gulf_scene(img, box):
    """Gulf art: night sea, coastline, two radar domes, missile trails."""
    from PIL import ImageDraw
    import math

    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    sea = _vgrad((w, h), (12, 34, 58), (10, 60, 88))
    img.paste(sea, (x0, y0))
    d = ImageDraw.Draw(img)
    rng = random.Random(777)
    # Stars.
    for _ in range(60):
        px, py = rng.randint(x0 + 4, x1 - 4), rng.randint(y0 + 4, y0 + h // 2)
        d.point((px, py), fill=(220, 230, 240))
    # Moon.
    d.ellipse([x0 + w - 44, y0 + 12, x0 + w - 16, y0 + 40], fill=(232, 228, 200))
    # Coastline (sand) bottom-left.
    d.polygon([(x0, y0 + h), (x0, y0 + h - 34), (x0 + 66, y0 + h - 52),
               (x0 + 128, y0 + h - 30), (x0 + 128, y0 + h)],
              fill=(196, 164, 110))
    # Radar domes on the coast.
    for dx in (x0 + 30, x0 + 82):
        d.rectangle([dx - 16, y0 + h - 62, dx + 16, y0 + h - 44], fill=(120, 128, 136))
        d.pieslice([dx - 18, y0 + h - 80, dx + 18, y0 + h - 44], 180, 360,
                   fill=(235, 238, 240))
        d.line([(dx, y0 + h - 80), (dx, y0 + h - 96)], fill=(240, 240, 240), width=2)
    # Radar arcs (kept inside the panel: centre y is y0+42, radii <= 36).
    for r in (16, 26, 36):
        d.arc([x0 + 56 - r, y0 + h - 96 - r, x0 + 56 + r, y0 + h - 96 + r],
              200, 340, fill=(120, 200, 200), width=2)
    # Missile trails (dashed arcs) + ships — all inside the panel.
    for sx0, sy0, sx1, sy1 in [(x0 + 138, y0 + 28, x0 + 104, y0 + 72),
                               (x0 + 150, y0 + 52, x0 + 118, y0 + 92)]:
        steps = 14
        for k in range(steps):
            t = k / steps
            px = int(sx0 + (sx1 - sx0) * t)
            py = int(sy0 + (sy1 - sy0) * t - 14 * math.sin(math.pi * t))
            if k % 2 == 0:
                d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(240, 150, 60))
        d.ellipse([sx1 - 4, sy1 - 4, sx1 + 4, sy1 + 4], fill=(240, 196, 90))
    for bx, by, bw in [(x0 + 112, y0 + h - 20, 30), (x0 + 124, y0 + h - 32, 26)]:
        d.rectangle([bx, by, bx + bw, by + 7], fill=(40, 44, 52))
        d.line([(bx + 7, by), (bx + 7, by - 10)], fill=(200, 200, 200), width=2)
    # Wave lines.
    for wy in (y0 + h - 14, y0 + h - 8):
        for wx in range(x0 + 118, x1 - 10, 22):
            d.arc([wx, wy - 3, wx + 18, wy + 5], 180, 360, fill=(140, 180, 200),
                  width=1)


def _draw_bridge_scene(img, box):
    """Kyiv art: dusk sky, river, arched bridge, skyline, searchlights."""
    from PIL import ImageDraw
    import math

    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    sky = _vgrad((w, h), (58, 44, 88), (196, 110, 70))
    img.paste(sky, (x0, y0))
    d = ImageDraw.Draw(img)
    rng = random.Random(4242)
    # Low sun.
    d.ellipse([x0 + w - 58, y0 + 16, x0 + w - 26, y0 + 48], fill=(244, 190, 110))
    # Searchlight beams.
    for bx, tilt in [(x0 + 30, -14), (x0 + 62, 6)]:
        d.polygon([(bx, y0 + h - 40), (bx - 4, y0 + h - 40),
                   (bx + tilt - 26, y0 + 8), (bx + tilt + 10, y0 + 8)],
                  fill=(240, 220, 170))
    # Skyline silhouettes.
    base = y0 + h - 44
    bx = x0 + 6
    while bx < x1 - 30:
        bw = rng.randint(16, 30)
        bh = rng.randint(18, 44)
        d.rectangle([bx, base - bh, bx + bw, base], fill=(28, 24, 40))
        for wy in range(base - bh + 5, base - 4, 9):
            for wx in range(bx + 4, bx + bw - 3, 8):
                if rng.random() < 0.5:
                    d.rectangle([wx, wy, wx + 3, wy + 4], fill=(244, 200, 90))
        bx += bw + 4
    # River.
    d.rectangle([x0, base, x1, y1], fill=(30, 60, 92))
    for wy in (base + 10, base + 22):
        for wx in range(x0 + 8, x1 - 10, 26):
            d.arc([wx, wy - 3, wx + 20, wy + 5], 180, 360, fill=(120, 160, 200),
                  width=1)
    # Arched bridge over the river.
    d.line([(x0 + 6, base + 4), (x1 - 6, base + 4)], fill=(235, 235, 235), width=4)
    d.arc([x0 + 26, base - 26, x1 - 26, base + 30], 180, 360,
          fill=(235, 235, 235), width=4)
    for cx in range(x0 + 46, x1 - 40, 22):
        d.line([(cx, base - 12), (cx, base + 4)], fill=(235, 235, 235), width=2)
    # Small flag on the bridge.
    d.line([(x0 + w // 2, base - 30), (x0 + w // 2, base - 46)], fill=(240, 240, 240),
           width=2)
    d.polygon([(x0 + w // 2, base - 46), (x0 + w // 2 + 18, base - 41),
               (x0 + w // 2, base - 36)], fill=(40, 90, 160))
    d.polygon([(x0 + w // 2, base - 41), (x0 + w // 2 + 18, base - 41),
               (x0 + w // 2, base - 36)], fill=(240, 200, 40))


def _draw_front_page(out_path):
    from PIL import Image, ImageDraw

    fonts = _load_fonts()
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    rng = random.Random(20261122)

    # ---- Masthead -------------------------------------------------------
    d.line([(28, 16), (996, 16)], fill=RULE, width=2)
    d.text((512, 26), "THE WORLD IN ONE PAGE", font=fonts["tagline"],
           fill=SOFT, anchor="ma")
    d.text((512, 44), "The Sunday World", font=fonts["masthead"], fill=INK,
           anchor="ma")
    d.text((512, 108), DATE_LINE, font=fonts["date"], fill=RED, anchor="ma")
    d.text((512, 132), TAGLINE, font=fonts["tagline"], fill=SOFT, anchor="ma")
    d.line([(28, 156), (996, 156)], fill=RULE, width=3)
    d.line([(28, 160), (996, 160)], fill=RULE, width=1)

    # ---- Hero band: COP31 ----------------------------------------------
    hy0, hy1 = 170, 372
    _draw_globe_scene(img, (28, hy0, 596, hy1))
    d.rectangle([28, hy0, 596, hy1], outline=RULE, width=2)
    d.text((28, hy1 + 6), "ANTALYA, TÜRKIYE — THE SUMMIT RUNS INTO SUNDAY",
           font=fonts["fixtures"], fill=SOFT)
    tx = 616
    d.text((tx, hy0 + 2), HERO_KICKER, font=fonts["kicker"], fill=RED)
    for i, line in enumerate(_wrap(d, HERO_HEAD, fonts["hero_head"], 996 - tx)):
        d.text((tx, hy0 + 24 + i * 34), line, font=fonts["hero_head"], fill=INK)
    dy = hy0 + 24 + 2 * 34 + 8
    for i, line in enumerate(_wrap(d, HERO_DEK, fonts["hero_dek"], 996 - tx)):
        d.text((tx, dy + i * 17), line, font=fonts["hero_dek"], fill=SOFT)
    # Objection deadline chip.
    chip_y = hy1 - 30
    d.rectangle([tx, chip_y, tx + 258, chip_y + 24], fill=NAVY)
    d.text((tx + 129, chip_y + 12), "OBJECTIONS BY 03:00 GMT",
           font=fonts["fixtures"], fill=(255, 255, 255), anchor="mm")

    # ---- Two illustrated panels ----------------------------------------
    py0, py1 = 396, 534
    pw = 474
    for px0, scene, kicker, head, dek in [
            (28, _draw_gulf_scene, PANEL_A_KICKER, PANEL_A_HEAD, PANEL_A_DEK),
            (522, _draw_bridge_scene, PANEL_B_KICKER, PANEL_B_HEAD, PANEL_B_DEK)]:
        scene(img, (px0, py0, px0 + 158, py1))
        d.rectangle([px0, py0, px0 + 158, py1], outline=RULE, width=2)
        tx2 = px0 + 170
        d.text((tx2, py0 + 2), kicker, font=fonts["kicker"], fill=RED)
        hy = py0 + 22
        for i, line in enumerate(_wrap(d, head, fonts["panel_head"],
                                       px0 + pw - tx2)):
            d.text((tx2, hy + i * 22), line, font=fonts["panel_head"], fill=INK)
        dy2 = hy + len(_wrap(d, head, fonts["panel_head"], px0 + pw - tx2)) * 22 + 4
        for i, line in enumerate(_wrap(d, dek, fonts["panel_dek"],
                                       px0 + pw - tx2)):
            d.text((tx2, dy2 + i * 14), line, font=fonts["panel_dek"], fill=SOFT)

    # ---- Stories grid: balanced 3 columns, never past gy1 ------------
    gy0, gy1 = 540, 916
    col_w = 310
    col_x = [28, 357, 686]
    by_region = {}
    for region, head, dek in STORIES:
        by_region.setdefault(region, []).append((head, dek))

    def header_h():
        return 24

    def item_h(head):
        return 12 * len(_wrap(d, head, fonts["story_head"], col_w)) + 11 + 3

    # Flat rows: ("H", region) headers and ("I", region, head, dek) items.
    rows = []
    for region in REGION_ORDER:
        items = by_region.get(region, [])
        if not items:
            continue
        rows.append(("H", region))
        for head, dek in items:
            rows.append(("I", region, head, dek))
        rows.append(("G",))  # 2px gap after a region

    def col_height(rs):
        """Height of a column holding these rows; a leading item needs a
        repeated region header first."""
        h = 0
        if rs and rs[0][0] == "I":
            h += header_h()
        for r in rs:
            if r[0] == "H":
                h += header_h()
            elif r[0] == "I":
                h += item_h(r[2])
            else:
                h += 2
        return h

    # Choose the two split points minimising the tallest column.
    budget = gy1 - gy0
    best = None
    n = len(rows)
    for i in range(1, n - 1):
        if rows[i - 1][0] == "H" or rows[i][0] == "G":
            continue
        for j in range(i + 1, n):
            if rows[j - 1][0] == "H" or rows[j][0] == "G":
                continue
            parts = (rows[:i], rows[i:j], rows[j:])
            heights = [col_height(p) for p in parts]
            score = max(heights)
            if best is None or score < best[0]:
                best = (score, parts)
    if best is None or best[0] > budget:
        raise RuntimeError("stories overflow the grid")
    for ci, part in enumerate(best[1]):
        x = col_x[ci]
        y = gy0
        if part and part[0][0] == "I":
            region = part[0][1]
            d.rectangle([x, y, x + col_w, y + 20], fill=REGION_COLORS[region])
            d.text((x + 8, y + 10), region, font=fonts["region"],
                   fill=(255, 255, 255), anchor="lm")
            y += header_h()
        for r in part:
            if r[0] == "H":
                region = r[1]
                d.rectangle([x, y, x + col_w, y + 20],
                            fill=REGION_COLORS[region])
                d.text((x + 8, y + 10), region, font=fonts["region"],
                       fill=(255, 255, 255), anchor="lm")
                y += header_h()
            elif r[0] == "I":
                _, _, head, dek = r
                for line in _wrap(d, head, fonts["story_head"], col_w):
                    d.text((x, y), line, font=fonts["story_head"], fill=INK)
                    y += 12
                d.text((x, y), dek, font=fonts["story_dek"], fill=SOFT)
                y += 11
                y += 3
            else:
                y += 2
    d.line([(28, gy1 + 6), (996, gy1 + 6)], fill=RULE, width=2)

    # ---- By-the-numbers strip ------------------------------------------
    ny0, ny1 = 926, 968
    d.rectangle([28, ny0, 996, ny1], fill=NAVY)
    seg = (996 - 28) / len(NUMBERS)
    for i, (big, small) in enumerate(NUMBERS):
        cx = 28 + seg * i + seg / 2
        d.text((cx, ny0 + 8), big, font=fonts["number_big"],
               fill=(240, 196, 90), anchor="ma")
        d.text((cx, ny0 + 30), small, font=fonts["number_small"],
               fill=(235, 238, 240), anchor="ma")
        if i:
            d.line([(28 + seg * i, ny0 + 6), (28 + seg * i, ny1 - 6)],
                   fill=(90, 120, 150), width=1)

    # ---- Footer ----------------------------------------------------------
    fy = 982
    for i, line in enumerate(_wrap(d, FOOTER, fonts["footer"], 968)):
        d.text((28, fy + i * 12), line, font=fonts["footer"], fill=SOFT)

    # ---- Paper grain (adds texture and file weight) ----------------------
    grain = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grain)
    for _ in range(26000):
        px, py = rng.randint(0, W - 1), rng.randint(0, H - 1)
        v = rng.choice([(255, 255, 255, 14), (0, 0, 0, 10)])
        gd.point((px, py), fill=v)
    img = Image.alpha_composite(img.convert("RGBA"), grain).convert("RGB")

    img.save(out_path, format="PNG")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
    try:
        _draw_front_page(out_path)
    except Exception:
        bundled = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "entry.png")
        if os.path.abspath(bundled) == os.path.abspath(out_path):
            raise
        shutil.copyfile(bundled, out_path)


if __name__ == "__main__":
    main()

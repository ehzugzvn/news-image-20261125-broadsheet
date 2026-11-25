#!/usr/bin/env python3
"""Broadsheet renderer for make.fun news-image-20261125.

Draws entry.png (1024x1024) with PIL only. All facts come from CONTENT.md;
all art is drawn here with PIL shapes. No external images are used.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BASE = os.path.dirname(os.path.abspath(__file__))
PAPER = (247, 242, 231)
INK = (17, 17, 17)
RED = (139, 26, 26)
MUTED = (96, 89, 76)
RULE = (130, 121, 105)
SEA = (211, 224, 227)
LAND = (231, 217, 182)
LAND_EDGE = (150, 138, 110)

SERIF_B = "LiberationSerif-Bold.ttf"
SERIF_R = "LiberationSerif-Regular.ttf"
SANS_B = "LiberationSans-Bold.ttf"
SANS_R = "LiberationSans-Regular.ttf"


def font(name, size):
    return ImageFont.truetype(os.path.join(BASE, "fonts", name), size)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
MX = 24
CW = W - 2 * MX  # 976


def wrap(text, f, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit(text, f, max_w):
    """Truncate with an ellipsis so text fits max_w in one line."""
    if d.textlength(text, font=f) <= max_w:
        return text
    while text and d.textlength(text + "...", font=f) > max_w:
        text = text[:-1]
    return text + "..."


def center(y, text, f, fill=INK, x0=MX, x1=W - MX):
    w = d.textlength(text, font=f)
    d.text(((x0 + x1 - w) / 2, y), text, font=f, fill=fill)


def hrule(y, fill=INK, width=2, x0=MX, x1=W - MX):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


def chip(x, y, text, fill=RED):
    f = font(SANS_B, 13)
    w = d.textlength(text, font=f) + 12
    d.rectangle([x, y, x + w, y + 18], fill=fill)
    d.text((x + 6, y + 2), text, font=f, fill=(255, 255, 255))
    return w


# ---------------------------------------------------------------- kicker bar
y = 8
f_kick = font(SANS_B, 13)
d.text((MX, y), "THE WORLD IN ONE DAY", font=f_kick, fill=INK)
right = "EVERY STORY DATED  ·  WEDNESDAY 25 NOV"
d.text((W - MX - d.textlength(right, font=f_kick), y), right,
       font=f_kick, fill=INK)
hrule(28, width=2)
hrule(31, width=1)

# ---------------------------------------------------------------- masthead date
DATE_TEXT = "Wednesday 25 November 2026"
size = 88
while size > 40:
    f_date = font(SERIF_B, size)
    if d.textlength(DATE_TEXT, font=f_date) <= CW:
        break
    size -= 2
d.text(((W - d.textlength(DATE_TEXT, font=f_date)) / 2, 36),
       DATE_TEXT, font=f_date, fill=INK)
y = 36 + size + 8
hrule(y, width=2)
y += 4
hrule(y, width=1)
y += 8

# ---------------------------------------------------------------- strip
center(y, "38 STORIES  ·  7 REGIONS  ·  EVERY ONE FROM THIS WEDNESDAY",
       font(SANS_B, 15))
y += 18
center(y, "Americas 8  ·  Europe 10  ·  Asia-Pacific 5  ·  Middle East 5  ·  "
          "Oceania 3  ·  Africa 4  ·  Global 3", font(SANS_R, 13), fill=MUTED)
y += 17

# ---------------------------------------------------------------- day in numbers
hrule(y, width=1)
y += 6
NUMBERS = [
    ("10/12", "counts convicted"),
    ("\u2248500,000", "Russian war dead"),
    ("47,000", "women killed by partners"),
    ("11", "wounded in Riyadh tower"),
    ("5.9%", "Nvidia shares fell"),
    ("1st", "Pakistani in orbit"),
]
cell = CW // 6
f_num = font(SERIF_B, 25)
f_cap = font(SANS_R, 13)
for i, (num, cap) in enumerate(NUMBERS):
    cx = MX + i * cell
    nw = d.textlength(num, font=f_num)
    d.text((cx + (cell - nw) / 2, y), num, font=f_num, fill=RED)
    for j, line in enumerate(wrap(cap, f_cap, cell - 10)):
        lw = d.textlength(line, font=f_cap)
        d.text((cx + (cell - lw) / 2, y + 27 + j * 14), line,
               font=f_cap, fill=INK)
    if i:
        d.line([(cx, y + 2), (cx, y + 42)], fill=RULE, width=1)
y += 44
hrule(y, width=1)
y += 6
LEADS_Y = y

# ---------------------------------------------------------------- art panels
def panel_label(x, y, w, text):
    f = font(SANS_B, 13)
    d.rectangle([x, y - 20, x + w, y], fill=INK)
    d.text((x + 8, y - 17), text, font=f, fill=(255, 255, 255))


def art_gavel(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(38, 52, 66))
    gold = (201, 162, 39)
    for ty in (y + 8, y + 16):
        d.line([(x + 8, ty), (x + w - 64, ty)], fill=gold, width=2)
    d.rectangle([x + 10, y + 6, x + 38, y + 16], fill=(20, 28, 38),
                outline=gold, width=1)
    d.rectangle([x + 46, y + 20, x + 74, y + 30], fill=(20, 28, 38),
                outline=gold, width=1)
    d.line([(x + w - 66, y + 28), (x + w - 26, y + 8)], fill=(146, 94, 46),
           width=5)
    d.polygon([(x + w - 36, y + 2), (x + w - 10, y + 8),
               (x + w - 16, y + 20), (x + w - 42, y + 14)],
              fill=(176, 118, 58))
    d.ellipse([x + w - 76, y + 24, x + w - 52, y + 31], fill=(96, 58, 26))
    panel_label(x, y + h, w, "COURTROOM  ·  BROOKLYN")


def art_rocket(x, y, w, h):
    bands = [(44, 32, 72), (96, 52, 88), (178, 84, 72), (232, 148, 84)]
    bh = max(1, (h - 20) // 4)
    for i, col in enumerate(bands):
        d.rectangle([x, y + i * bh, x + w, y + (i + 1) * bh], fill=col)
    d.rectangle([x, y + 4 * bh, x + w, y + h - 20], fill=bands[-1])
    d.ellipse([x + w - 34, y + 3, x + w - 18, y + 19], fill=(255, 214, 130))
    for sx, sy in [(x + 16, y + 6), (x + 60, y + 12), (x + 120, y + 5)]:
        d.ellipse([sx, sy, sx + 3, sy + 3], fill=(255, 255, 255))
    cx = x + w // 2 - 40
    d.rectangle([x + 8, y + 6, x + 64, y + 12], fill=(30, 30, 40))
    d.rectangle([x + 24, y + 12, x + 48, y + 17], fill=(52, 52, 66))
    d.polygon([(cx, y + 2), (cx + 11, y + 16), (cx + 11, y + 24),
               (cx, y + 27), (cx - 11, y + 24), (cx - 11, y + 16)],
              fill=(245, 245, 240))
    d.polygon([(cx, y + 2), (cx + 11, y + 16), (cx - 11, y + 16)],
              fill=(178, 34, 34))
    d.polygon([(cx - 11, y + 20), (cx - 22, y + 27), (cx - 11, y + 26)],
              fill=(178, 34, 34))
    d.polygon([(cx + 11, y + 20), (cx + 22, y + 27), (cx + 11, y + 26)],
              fill=(178, 34, 34))
    d.polygon([(cx - 5, y + 27), (cx + 5, y + 27), (cx, y + 31)],
              fill=(255, 140, 0))
    d.polygon([(cx - 3, y + 27), (cx + 3, y + 27), (cx, y + 30)],
              fill=(255, 220, 80))
    panel_label(x, y + h, w, "JIUQUAN  ·  00:18 UTC")


def art_graves(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(74, 78, 84))
    top = y + h - 20
    bars = [0.30, 0.42, 0.55, 0.70, 0.88]
    bw = w // 7
    for i, frac in enumerate(bars):
        bx = x + 14 + i * (bw + 6)
        bh = int((top - y - 4) * frac)
        d.rectangle([bx, top - bh, bx + bw, top], fill=(30, 32, 38))
    for gx in (x + 30, x + w // 2 - 14, x + w - 62):
        d.rectangle([gx, top - 14, gx + 26, top], fill=(210, 208, 200))
        d.ellipse([gx, top - 24, gx + 26, top - 4], fill=(210, 208, 200))
        d.line([(gx + 13, top - 11), (gx + 13, top - 3)],
               fill=(120, 118, 110), width=2)
        d.line([(gx + 7, top - 7), (gx + 19, top - 7)],
               fill=(120, 118, 110), width=2)
    panel_label(x, y + h, w, "MOSCOW  ·  LEAKED DATA")


def art_chip(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 28, 36))
    for px in range(x + 8, x + w - 8, 12):
        d.line([(px, y), (px, y + 5)], fill=(201, 162, 39), width=2)
        d.line([(px, y + h - 5), (px, y + h)], fill=(201, 162, 39), width=2)
    d.rectangle([x + 8, y + 8, x + 40, y + h - 8], fill=(52, 58, 70),
                outline=(201, 162, 39), width=2)
    d.text((x + 14, y + 10), "AI", font=font(SANS_B, 14), fill=(255, 255, 255))
    pts = [(x + 52, y + 8), (x + 74, y + 12), (x + 96, y + 10),
           (x + 118, y + 20), (x + 140, y + 22), (x + 164, y + 32)]
    d.line(pts, fill=(220, 60, 60), width=3)
    d.polygon([(x + 164, y + 32), (x + 154, y + 28), (x + 158, y + 36)],
              fill=(220, 60, 60))
    d.text((x + 52, y + h - 16), "-5.9%", font=font(SANS_B, 13),
           fill=(220, 60, 60))


# ---------------------------------------------------------------- three leads
ART_H = 52
LEADS = [
    ("HUAWEI GUILTY",
     "Huawei guilty on 10 of 12 counts, and it will appeal",
     "Brooklyn jury convicts the telecom giant of bank fraud, wire fraud "
     "and sanctions violations.",
     "REUTERS · CNN · WSJ", "C", art_gavel),
    ("SHENZHOU-24",
     "Shenzhou-24 lifts off with a Pakistani pilot aboard",
     "Long March 2F lifts off at 00:18 UTC with Muhammad Zeeshan Ali, "
     "the first Pakistani in orbit.",
     "XINHUA · REUTERS · CMSA", "C", art_rocket),
    ("RUSSIA'S WAR DEAD",
     "Russia's own figures show nearly 500,000 war dead",
     "Leaked Russian data shows ~500,000 excess deaths among military-age "
     "men since the invasion.",
     "BBC RUSSIAN SERVICE · MEDIAZONA", "R", art_graves),
]
col_w = (CW - 2 * 12) // 3
f_head = font(SERIF_B, 19)
f_sum = font(SANS_R, 13)
f_src = font(SANS_B, 13)
y = LEADS_Y
for i, (kick, head, summ, src, tag, art) in enumerate(LEADS):
    cx = MX + i * (col_w + 12)
    art(cx, y, col_w, ART_H)
    chip(cx + col_w - 30, y + 6, tag,
         RED if tag == "C" else (60, 60, 60))
    ty = y + ART_H + 6
    for line in wrap(head, f_head, col_w):
        d.text((cx, ty), line, font=f_head, fill=INK)
        ty += 20
    for line in wrap(summ, f_sum, col_w):
        d.text((cx, ty), line, font=f_sum, fill=INK)
        ty += 15
    ty += 2
    d.text((cx, ty), fit(src, f_src, col_w), font=f_src, fill=MUTED)
    if i:
        d.line([(cx - 6, y), (cx - 6, ty + 14)], fill=RULE, width=1)
LEADS_END = y + ART_H + 6 + 40 + 30 + 2 + 15
y = LEADS_END + 6
hrule(y, width=1)
y += 8

# ---------------------------------------------------------------- Nvidia strip
nv_x, nv_y, nv_w, nv_h = MX, y, 190, 38
art_chip(nv_x, nv_y, nv_w, nv_h)
tx = MX + nv_w + 14
d.text((tx, y),
       fit("NVIDIA — Huang apologises to staff as Nvidia shares slide 5.9%",
           font(SERIF_B, 18), CW - nv_w - 14 - 52), font=font(SERIF_B, 18),
       fill=INK)
chip(W - MX - 30, y, "C", RED)
d.text((tx, y + 21),
       fit("A day after his Trump-backed return as CEO, Huang told staff he "
           "made \u201cterrible mistakes\u201d — REUTERS · NYT · THE TIMES",
           f_sum, CW - nv_w - 14), font=f_sum, fill=INK)
y += nv_h + 6
hrule(y, width=1)
y += 8
TIER2_Y = y

# ---------------------------------------------------------------- tier-2
def picto(x, y, kind, bg):
    tmp = Image.new("RGB", (40, 40), bg)
    p = ImageDraw.Draw(tmp)
    wht = (255, 255, 255)
    if kind == "plane":
        p.polygon([(6, 24), (34, 12), (28, 26), (20, 24), (14, 32), (12, 26)],
                  fill=wht)
    elif kind == "flag":
        p.line([(12, 6), (12, 34)], fill=wht, width=3)
        p.polygon([(12, 6), (32, 12), (12, 18)], fill=wht)
    elif kind == "venus":
        p.ellipse([11, 6, 29, 24], outline=wht, width=3)
        p.line([(20, 24), (20, 34)], fill=wht, width=3)
        p.line([(14, 29), (26, 29)], fill=wht, width=3)
    elif kind == "ship":
        p.polygon([(6, 22), (34, 22), (28, 32), (12, 32)], fill=wht)
        p.line([(20, 8), (20, 22)], fill=wht, width=3)
        p.polygon([(20, 8), (32, 14), (20, 14)], fill=wht)
    elif kind == "pct":
        p.text((9, 8), "%", font=font(SANS_B, 24), fill=wht)
    elif kind == "drone":
        p.line([(10, 10), (30, 30)], fill=wht, width=3)
        p.line([(30, 10), (10, 30)], fill=wht, width=3)
        for px, py in [(10, 10), (30, 10), (10, 30), (30, 30)]:
            p.ellipse([px - 3, py - 3, px + 3, py + 3], fill=wht)
    elif kind == "quake":
        p.line([(6, 26), (12, 14), (18, 26), (24, 10), (30, 26), (34, 18)],
               fill=wht, width=3)
    elif kind == "lens":
        p.ellipse([8, 8, 26, 26], outline=wht, width=3)
        p.line([(23, 23), (33, 33)], fill=wht, width=3)
    elif kind == "building":
        p.rectangle([10, 8, 30, 34], fill=wht)
        for wy in (14, 22):
            for wx in (14, 22):
                p.rectangle([wx, wy, wx + 4, wy + 4], fill=bg)
    elif kind == "wave":
        for wy in (16, 24, 32):
            p.line([(6, wy), (12, wy - 4), (18, wy), (24, wy - 4),
                    (30, wy), (34, wy - 4)], fill=wht, width=2)
    img.paste(tmp.resize((32, 32), Image.LANCZOS), (x, y))


TIER2 = [
    ("HODEIDAH / RIYADH",
     "Saudi jets bomb Hodeidah; Houthis hit Riyadh tower",
     "11 hurt in 2nd strike on the PIF tower.",
     "AL JAZEERA · REUTERS", "C", "plane", (139, 26, 26)),
    ("AUSTRALIA–SOLOMONS",
     "Australia signs sweeping pact with Solomon Islands",
     "Pact covers police, ports, schools.",
     "REUTERS · ABC", "O", "flag", (30, 70, 110)),
    ("FEMICIDE",
     "UN: 47,000 women killed by partners or kin in a year",
     "129 a day; Africa's rate highest.",
     "UNODC · UN WOMEN", "O", "venus", (110, 40, 90)),
    ("HORMUZ",
     "Two tankers hit mines in the Strait of Hormuz, IRGC says",
     "Saudis hit Hodeidah in reply.",
     "TIMES OF ISRAEL · GULF NEWS", "R", "ship", (20, 80, 90)),
    ("US TARIFFS",
     "US readies tariffs in 16-nation capacity probe, 15–25%",
     "China, India, Japan, ASEAN hit.",
     "REUTERS · HINDUSTAN TIMES", "R", "pct", (120, 80, 20)),
    ("SAMARA",
     "Ukraine drones hit two Samara refineries, 800 km deep",
     "Kremlin rejects talks.",
     "KYIV INDEPENDENT · AZERNEWS", "R", "drone", (60, 60, 60)),
    ("QUAKES",
     "M5.9 quakes strike off Baffin Island and near Antarctica",
     "Balleny Islands quake 10 km deep at 04:30 UTC.",
     "USGS", "O", "quake", (90, 60, 30)),
    ("SHANGHAI",
     "Xi's anti-graft drive reaches Shanghai party boss",
     "Chen Jining probed before reshuffle.",
     "GUARDIAN · CNA", "C", "lens", (139, 26, 26)),
    ("CARTAGENA",
     "Hostages held in a supermarket on a second day",
     "At least 20 remain inside after a failed raid.",
     "AP · EL TIEMPO", "R", "building", (30, 70, 110)),
    ("GULF OF FINLAND",
     "A drone hits a Russian cargo ship in the gulf",
     "Zelenskyy confirmed the strike.",
     "YLE · REUTERS", "R", "wave", (20, 80, 90)),
]
d.text((MX, TIER2_Y), "THE WORLD IN BRIEF  —  TEN MORE STORIES",
       font=font(SANS_B, 14), fill=INK)
y = TIER2_Y + 18
tcol_w = (CW - 16) // 2
f_thead = font(SANS_B, 14)
f_tsum = font(SANS_R, 13)
ROW_H = 33
for i, (kick, head, summ, src, tag, kind, bg) in enumerate(TIER2):
    cx = MX + (i % 2) * (tcol_w + 16)
    ry = y + (i // 2) * ROW_H
    picto(cx, ry, kind, bg)
    tx = cx + 40
    tw_ = tcol_w - 40
    d.text((tx, ry), fit(head, f_thead, tw_), font=f_thead, fill=INK)
    d.text((tx, ry + 16),
           fit(summ + "  ·  " + tag + "  ·  " + src, f_tsum, tw_),
           font=f_tsum, fill=MUTED)
y = y + 5 * ROW_H + 2
hrule(y, width=1)
y += 6

# ---------------------------------------------------------------- world map
d.text((MX, y), "WHERE IT HAPPENED  —  PINS 1–14 KEYED TO THE STORIES ABOVE",
       font=font(SANS_B, 14), fill=INK)
y += 16
MAP_H = 40
map_x0, map_y0 = MX, y
d.rectangle([map_x0, map_y0, map_x0 + CW, map_y0 + MAP_H], fill=SEA)


def mxy(lon, lat):
    lat = max(-55.0, min(75.0, lat))
    return (map_x0 + (lon + 180.0) / 360.0 * CW,
            map_y0 + (75.0 - lat) / 130.0 * MAP_H)


CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 70),
     (-75, 73), (-65, 60), (-55, 47), (-70, 42), (-75, 35), (-80, 32),
     (-85, 30), (-90, 21), (-97, 16), (-105, 20), (-115, 28), (-125, 40),
     (-125, 49), (-140, 60), (-155, 58), (-165, 60)],
    [(-58, 64), (-45, 60), (-30, 68), (-20, 70), (-35, 76), (-55, 76)],
    [(-80, 9), (-75, 11), (-60, 8), (-50, 0), (-35, -8), (-40, -20),
     (-48, -28), (-58, -38), (-65, -45), (-70, -54), (-73, -40),
     (-70, -20), (-80, -5), (-81, 0)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 59), (28, 60), (30, 62), (25, 65), (20, 70),
     (15, 70), (5, 60), (-5, 58), (-10, 54), (-10, 43), (-9, 38)],
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51)],
    [(-17, 15), (-10, 31), (0, 36), (10, 37), (20, 32), (30, 31),
     (35, 28), (40, 15), (48, 11), (51, 10), (44, 0), (40, -10),
     (35, -20), (32, -29), (25, -34), (18, -35), (14, -22), (12, -10),
     (9, 4), (-8, 4), (-13, 8), (-17, 12)],
    [(30, 36), (35, 30), (42, 38), (48, 38), (54, 26), (57, 25), (60, 25),
     (66, 25), (72, 20), (77, 8), (80, 10), (85, 20), (90, 22), (94, 16),
     (98, 10), (100, 5), (103, 1), (105, 10), (108, 15), (109, 20),
     (115, 25), (120, 30), (122, 35), (126, 40), (130, 42), (135, 44),
     (140, 45), (142, 50), (140, 55), (135, 60), (130, 65), (125, 70),
     (120, 72), (110, 73), (100, 76), (90, 75), (80, 73), (70, 72),
     (60, 70), (50, 68), (40, 66), (35, 64), (30, 60), (28, 55),
     (30, 45), (28, 42), (25, 40), (22, 37)],
    [(130, 31), (133, 34), (137, 35), (140, 38), (141, 41), (143, 43),
     (145, 44)],
    [(114, -22), (114, -30), (115, -35), (124, -33), (130, -32),
     (135, -35), (140, -38), (146, -39), (150, -37), (153, -27),
     (146, -19), (142, -11), (136, -12), (132, -12), (126, -14),
     (122, -17), (118, -20)],
    [(167, -45), (170, -42), (174, -39), (177, -38), (175, -40),
     (172, -43), (168, -46)],
]
for poly in CONTINENTS:
    d.polygon([mxy(lon, lat) for lon, lat in poly], fill=LAND,
              outline=LAND_EDGE)
PINS = [(1, -74, 40.7), (2, 98.5, 39.7), (3, 37.6, 55.7), (4, -122, 37.4),
        (5, 46.7, 24.7), (6, 149.1, -35.3), (7, -30, 5), (8, 56.5, 26.5),
        (9, -77, 38.9), (10, 50.1, 53.2), (11, 163, -55), (12, 121.5, 31.2),
        (13, -75.5, 10.4), (14, 24, 59.8)]
PIN_OFF = {9: (-14, 0), 13: (0, 10), 5: (-16, 10), 8: (8, 0)}
f_pin = font(SANS_B, 13)
for num, lon, lat in PINS:
    px, py = mxy(lon, lat)
    ox, oy = PIN_OFF.get(num, (0, 0))
    qx, qy = px + ox, min(py + oy, map_y0 + MAP_H - 11)
    if (ox, oy) != (0, 0):
        d.line([(px, py), (qx, qy)], fill=RED, width=2)
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED)
    d.ellipse([qx - 10, qy - 10, qx + 10, qy + 10], fill=RED,
              outline=(255, 255, 255), width=2)
    t = str(num)
    tw_ = d.textlength(t, font=f_pin)
    d.text((qx - tw_ / 2, qy - 7), t, font=f_pin, fill=(255, 255, 255))
y = map_y0 + MAP_H + 8
hrule(y, width=1)
y += 8

# ---------------------------------------------------------------- briefs 15-38
BRIEFS = [
    ("WINDSOR", "Two arrested on William and Kate's estate."),
    ("DAKAR", "Senegal restored as 2025 African champions on appeal."),
    ("LOS ANGELES", "Thomas Markle charged with a second count."),
    ("MADRID", "Spain votes Sunday; Vox may enter government (F)."),
    ("NEW DELHI", "Food inflation spreads to vegetables, pulses and oils."),
    ("TAIPEI", "AI disinfo network targets Taiwan election candidates."),
    ("SYDNEY", "Ex-officer Beau Lamarre convicted of double murder."),
    ("BAGHDAD", "Iraq orders takeover of Kurdish-controlled oilfields."),
    ("KUALA LUMPUR", "Malaysia to return Rohingya refugees to Myanmar."),
    ("HAVANA", "WHO chief urges end to US fuel blockade on Cuba."),
    ("GLOBAL", "Landmine casualties hit a five-year high."),
    ("DEEP SPACE", "ESA's Hera reaches asteroid Dimorphos."),
    ("MOSCOW", "Putin and Brunei Sultan sign joint declaration."),
    ("PARIS", "Champions League: PSG–Roma & Arsenal–BVB."),
    ("BRUSSELS", "NATO chief Rutte meets Trump on alliance security."),
    ("CHICAGO", "O'Hare FAA ground stop & radar outage snarls travel."),
    ("MEXICO CITY", "US Embassy alerts on Reforma-to-Zócalo march."),
    ("BRUSSELS", "90+ leaders urge EU to cap €210B Russian assets."),
    ("BENGHAZI", "UN cities hit in drone strike on Russian ship."),
    ("LONDON", "Russia demands UK drop NATO nuclear shield."),
    ("GAZA", "Israeli strike kills Hamas security chief Naeem Abu Nahel."),
    ("DOHA", "US Embassy warns of Houthi threats."),
    ("ABUJA", "Tinubu sends N65.2T budget; Senate clears $20.5B loan."),
    ("CAIRO", "Sudan & Egypt reject Red Sea militarisation."),
]
d.text((MX, y), "THE DAY IN BRIEF  —  15–38",
       font=font(SANS_B, 14), fill=INK)
y += 18
bcol_w = (CW - 3 * 12) // 4
f_b = font(SANS_B, 13)
f_br = font(SANS_R, 13)
BROW_H = 27
for i, (place, text) in enumerate(BRIEFS):
    col = i % 4
    row = i // 4
    bx = MX + col * (bcol_w + 12)
    by = y + row * BROW_H
    lead = "%d. %s — " % (15 + i, place)
    first = lead + text
    lines = wrap(first, f_br, bcol_w)
    # bold lead-in: draw lead bold, rest regular on line 1
    lead_w = d.textlength(lead, font=f_b)
    if d.textlength(lines[0], font=f_br) <= bcol_w and lines[0] == first:
        d.text((bx, by), lead, font=f_b, fill=INK)
        d.text((bx + lead_w, by), text, font=f_br, fill=INK)
    else:
        d.text((bx, by), lead, font=f_b, fill=INK)
        rest = lines[0][len(lead):] if lines[0].startswith(lead) else lines[0]
        # wrap remainder properly: recompute with lead width taken
        avail = bcol_w - lead_w
        words = text.split()
        l1, cur = "", ""
        for w_ in words:
            t = (cur + " " + w_).strip()
            if d.textlength(t, font=f_br) <= avail:
                cur = t
            else:
                break
        l1 = cur
        d.text((bx + lead_w, by), l1, font=f_br, fill=INK)
        rem = text[len(l1):].strip()
        if rem:
            for j, ln in enumerate(wrap(rem, f_br, bcol_w)):
                d.text((bx, by + 14 + j * 14), ln, font=f_br, fill=INK)
y = y + 6 * BROW_H + 2
hrule(y, width=1)
y += 7

# ---------------------------------------------------------------- timeline
f_tl = font(SANS_R, 13)
f_tlb = font(SANS_B, 13)
d.text((MX, y), "THE DAY IN TIME — UTC", font=f_tlb, fill=INK)
tl1 = ("00:18 Shenzhou lifts off  ·  01:38 M5.9 quake, Baffin Is.  ·  "
       "03:56 Shenzhou docks  ·  04:30 M5.9 quake, Balleny Is.  ·  "
       "Morning: Huawei verdict")
tl2 = ("Midday: Australia–Solomons pact  ·  Afternoon: Hodeidah / Riyadh "
       "strikes  ·  Evening: Samara refineries hit  ·  Night: Nvidia −5.9%")
d.text((MX, y + 14), fit(tl1, f_tl, CW), font=f_tl, fill=INK)
d.text((MX, y + 28), fit(tl2, f_tl, CW), font=f_tl, fill=INK)
y += 42
hrule(y, width=1)
y += 5

# ---------------------------------------------------------------- date check + legend + footer
f_dc = font(SANS_R, 13)
f_dcb = font(SANS_B, 13)
d.text((MX, y), "DATE CHECK — ", font=f_dcb, fill=RED)
dc = ("Left out as other days' news: Spain's election (29 Nov, not yet) · "
      "US Thanksgiving (26 Nov, not yet) · Huang's Senate hearing (3 Dec, "
      "not yet) · Huawei sentencing (Sep 2027, not yet).")
for j, ln in enumerate(wrap(dc, f_dc, CW - d.textlength("DATE CHECK —  ",
                                                       font=f_dcb))):
    d.text((MX + (d.textlength("DATE CHECK —  ", font=f_dcb) if j == 0 else 0),
            y + j * 15), ln, font=f_dc, fill=INK)
y += 30
d.text((MX, y), "Every story here happened, or was first reported, on "
       "Wednesday 25 November 2026, as the named outlets reported it.",
       font=f_dc, fill=INK)
y += 15
d.text((MX, y), "HOW SURE:  C = CONFIRMED by 2+ major outlets  ·  "
       "O = OFFICIAL data or statement  ·  R = REPORTED by one outlet or "
       "attributed  ·  F = FORECAST / preview",
       font=f_dcb, fill=INK)
y += 15
hrule(y, width=1)
y += 5
foot = ("Sources: Reuters · AP · BBC · Al Jazeera · Xinhua · The Guardian · "
        "USGS · UNODC · NATO — Drawn by an AI agent for make.fun — "
        "25 Nov 2026")
d.text((MX, y), fit(foot, f_dc, CW), font=f_dc, fill=MUTED)
y += 14
print("final y:", y, "of", H)

img.save(os.path.join(BASE, "entry.png"), optimize=True)
print("saved entry.png")

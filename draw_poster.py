#!/usr/bin/env python3
"""Draw the news-image-20261117 poster: a one-page newspaper front page
summing up Tuesday 17 November 2026 in 35 stories across 6 continents.

Variant 1 (default): light paper front page, red + navy accents.
Variant 2: dark navy hero band, white hero text.
Run:  python3 draw_poster.py [1|2] [output-path]
Uses Pillow + DejaVu fonts (local build tool only; main.py is stdlib-only
and just copies the finished entry.png).
"""
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (17, 17, 17)
RED = (178, 24, 24)
NAVY = (24, 54, 96)
GOLD = (176, 132, 24)
GREY = (90, 88, 82)
LIGHT_LINE = (205, 198, 184)
SECTION_COLORS = {
    "CONFLICT & MIDDLE EAST": (140, 28, 28),
    "EUROPE & DIPLOMACY": (24, 54, 96),
    "ECONOMY & TECH": (18, 92, 66),
    "HEALTH, CLIMATE & AFRICA": (122, 74, 12),
    "SPORT & CULTURE": (94, 42, 110),
    "CULTURE & OBITUARIES": (94, 42, 110),
}

FDIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FDIR + name, size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_I = lambda s: font("DejaVuSans-Oblique.ttf", s) if False else font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_w, fill, leading=None):
    lines = wrap(draw, text, fnt, max_w)
    lh = leading or int(fnt.size * 1.22)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


HERO = [
    ("U.S. STRIKES IRAN", "Missiles answer drones",
     "US jets hit a missile site on Qeshm Island after Iran fired drones at a US radar base in Bahrain.",
     "strike"),
    ("KERCH BRIDGE HIT AGAIN", "Span falls into the strait",
     "Ukraine's drones strike the Crimea bridge a second day running; traffic is halted.",
     "bridge"),
    ("SHENZHEN SUMMIT SET", "Xi, Trump & Putin to meet",
     "The three leaders are confirmed for Thursday at APEC, for nuclear talks and Ukraine.",
     "summit"),
]

COLUMNS = [
    [("CONFLICT & MIDDLE EAST", [
        ("Tankers hit by mines", "Several tankers struck near Hormuz."),
        ("Third US carrier arrives", "Another carrier group in the region."),
        ("Dirty-bomb report denied", "Trump 'looking into' it; Tehran denies."),
        ("Sudan: 1,390 civilians killed", "UN counts the dead in H1 2026."),
        ("Western Sahara pull-out", "First MINURSO troops leave Laayoune."),
     ]),
     ("EUROPE & DIPLOMACY", [
        ("Estonia shuts Russia border", "Crossings close 1 Dec over sabotage."),
        ("Five states plan Rwanda hub", "Joint returns centre outlined."),
        ("Japan scrambles jets", "Tokyo protests to Moscow."),
        ("Slovenia grows 3.7%", "Q3 GDP up on spending, exports."),
        ("Trump in Manila", "At ASEAN before flying to China."),
     ])],
    [("ECONOMY & TECH", [
        ("Nvidia tops $115bn", "Record revenue; Huang will not return."),
        ("Markets slide", "S&P -1.03%, Euro Stoxx -2.15%."),
        ("Singapore wants AI chips", "Seeks trusted access under US curbs."),
        ("Microsoft explains outage", "Latent defect knocked out servers."),
        ("Japan banks raise forecasts", "MUFG, SMFG, Mizuho lift outlooks."),
        ("Anthropic IPO priced", "Shares proposed at $70-$78."),
     ]),
     ("HEALTH, CLIMATE & AFRICA", [
        ("Ebola passes 11,000 cases", "DR Congo: 5,400 deaths, UN says."),
        ("US measles at 1991 high", "Highest since 1991; 13 babies born ill."),
        ("Nepal presses for climate cash", "At COP31 after August's floods."),
        ("AfDB signs \u00a586.6bn loan", "Largest ever for its development fund."),
        ("Barrick pulls Congo staff", "Mine furloughs workers over Ebola."),
     ])],
    [("SPORT & CULTURE", [
        ("Argentina 7-0 Costa Rica", "No Messi; Paz, Alvarez, Mastantuono."),
        ("Haaland sends Norway through", "Penalty seals 3-2 win over Denmark."),
        ("Portugal top the group", "3-2 win in Wales, Nations League."),
        ("N. Ireland promoted", "1-1 in Hungary lifts them to League A."),
        ("Morocco & Senegal qualify", "Both book AFCON 2027 places."),
        ("Zverev into ATP knockouts", "India beat Pakistan 2-1, win SAFF."),
        ("Japan v Paraguay", "Friendly at Singapore National Stadium."),
     ]),
     ("CULTURE & OBITUARIES", [
        ("Dhoni retires from Chennai", "Ends his IPL playing career."),
        ("Peter Storey dies at 81", "Arsenal Double winner of 1971."),
        ("Yutaka Enatsu dies at 78", "Japanese strikeout great."),
     ])],
]

ALSO = ("England FA eye the 2027 Nations League finals  \u2022  "
        "FC Cincinnati near deal for Racing Louisville  \u2022  Al-Ahli lose two for Al-Nassr")

MARKETS = ("MARKETS  \u2014  S&P 500  7,341  \u25bc1.03%    FTSE 100  10,690  \u25bc1.76%    "
           "EURO STOXX  \u25bc2.15%    BRENT  $93.21    NIKKEI  \u25b21.13%")


def story_count():
    n = len(HERO)
    for col in COLUMNS:
        for _, items in col:
            n += len(items)
    return n  # 30 main stories; +5 in ALSO = 35


def draw_icon_strike(d, x, y, s=64):
    # red burst behind a navy jet climbing up-right
    cx, cy = x + s / 2, y + s / 2
    for ang in range(0, 360, 30):
        import math
        r1, r2 = 26, 15
        a = math.radians(ang)
        d.line([cx + r2 * math.cos(a), cy + r2 * math.sin(a),
                cx + r1 * math.cos(a), cy + r1 * math.sin(a)], fill=(178, 24, 24), width=4)
    d.polygon([(x + 12, y + 44), (x + 40, y + 16), (x + 46, y + 26),
               (x + 52, y + 22), (x + 30, y + 52), (x + 22, y + 46)],
              fill=(24, 54, 96))
    d.polygon([(x + 14, y + 48), (x + 8, y + 56), (x + 20, y + 52)], fill=(178, 24, 24))


def draw_icon_bridge(d, x, y, s=64):
    # deck in two segments with a gap knocked out in the middle
    d.rectangle([x + 4, y + s * 0.55, x + s * 0.42, y + s * 0.62], fill=(24, 54, 96))
    d.rectangle([x + s * 0.58, y + s * 0.55, x + s - 4, y + s * 0.62], fill=(24, 54, 96))
    d.rectangle([x + 10, y + 10, x + 16, y + s * 0.60], fill=(24, 54, 96))
    d.rectangle([x + s - 16, y + 10, x + s - 10, y + s * 0.60], fill=(24, 54, 96))
    # the fallen span, tilted, dropping into the water
    d.line([x + s * 0.44, y + s * 0.58, x + s * 0.56, y + s * 0.82], fill=(178, 24, 24), width=5)
    d.ellipse([x + s * 0.46, y + s * 0.80, x + s * 0.64, y + s * 0.90], fill=(90, 140, 200))
    d.line([x + 12, y + 10, x + s * 0.30, y + s * 0.55], fill=(120, 120, 120), width=2)
    d.line([x + s - 12, y + 10, x + s * 0.70, y + s * 0.55], fill=(120, 120, 120), width=2)


def draw_icon_summit(d, x, y, s=64):
    w = 18
    # US: stripes + canton
    for i in range(5):
        d.rectangle([x, y + i * 6, x + w, y + i * 6 + 3], fill=(178, 24, 24) if i % 2 == 0 else (255, 255, 255))
    d.rectangle([x, y, x + 9, y + 15], fill=(24, 54, 96))
    # China: red + stars
    d.rectangle([x + w + 3, y, x + 2 * w + 3, y + 30], fill=(178, 24, 24))
    d.ellipse([x + w + 6, y + 3, x + w + 12, y + 9], fill=(255, 220, 60))
    # Russia: white / blue / red
    d.rectangle([x + 2 * w + 6, y, x + 3 * w + 6, y + 10], fill=(255, 255, 255))
    d.rectangle([x + 2 * w + 6, y + 10, x + 3 * w + 6, y + 20], fill=(24, 84, 180))
    d.rectangle([x + 2 * w + 6, y + 20, x + 3 * w + 6, y + 30], fill=(178, 24, 24))


ICONS = {"strike": draw_icon_strike, "bridge": draw_icon_bridge, "summit": draw_icon_summit}


def build(variant=1, out_path="entry.png"):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    dark_hero = (variant == 2)

    # --- top strip ---
    d.rectangle([0, 0, W, 30], fill=INK)
    d.text((22, 7), "TUESDAY 17 NOVEMBER 2026", font=SANS_B(15), fill=(255, 255, 255))
    right = "37 STORIES  \u2022  6 CONTINENTS  \u2022  ONE DAY"
    d.text((W - 22 - d.textlength(right, font=SANS_B(15)), 7), right, font=SANS_B(15), fill=(255, 200, 60))

    # --- masthead ---
    title = "THE WORLD IN ONE DAY"
    tf = SERIF_B(56)
    d.text(((W - d.textlength(title, font=tf)) / 2, 40), title, font=tf, fill=INK)
    date = "TUESDAY, 17 NOVEMBER 2026"
    df = SANS_B(30)
    d.text(((W - d.textlength(date, font=df)) / 2, 104), date, font=df, fill=RED)
    d.text((22, 140), "The day's world news, in one image", font=SANS(15), fill=GREY)
    d.text((W - 22 - d.textlength("All events of 17 November 2026", font=SANS(15)), 140),
           "All events of 17 November 2026", font=SANS(15), fill=GREY)
    d.rectangle([22, 164, W - 22, 168], fill=INK)
    d.rectangle([22, 171, W - 22, 174], fill=RED)

    # --- hero: 3 lead stories ---
    hx, hy, hw, hg = 22, 182, 316, 168
    gap = 16
    hero_bg = NAVY if dark_hero else (255, 255, 255)
    hero_kick = (255, 200, 60) if dark_hero else RED
    hero_head = (255, 255, 255) if dark_hero else INK
    hero_deck = (220, 225, 235) if dark_hero else (60, 58, 52)
    for i, (kick, head, deck, kind) in enumerate(HERO):
        x = hx + i * (hw + gap)
        d.rectangle([x, hy, x + hw, hy + hg], fill=hero_bg, outline=INK, width=2)
        d.rectangle([x, hy, x + hw, hy + 26], fill=RED if not dark_hero else (140, 20, 20))
        d.text((x + 10, hy + 5), kick, font=SANS_B(13), fill=(255, 255, 255))
        y = hy + 34
        # icon top-right
        ICONS[kind](d, x + hw - 74, y, 64)
        y = draw_wrapped(d, x + 10, y, head, SANS_B(21), hw - 88, hero_head, leading=24)
        y += 4
        draw_wrapped(d, x + 10, y, deck, SANS(14), hw - 20, hero_deck, leading=18)

    # --- section header ---
    sy = 362
    d.rectangle([22, sy, W - 22, sy + 26], fill=INK)
    d.text((30, sy + 5), "THE DAY IN BRIEF  \u2014  BY REGION", font=SANS_B(14), fill=(255, 255, 255))
    d.text((W - 22 - d.textlength("34 stories below  \u2022  3 more in brief at the foot", font=SANS(13)), sy + 6),
           "34 stories below  \u2022  3 more in brief at the foot", font=SANS(13), fill=(200, 200, 200))

    # --- columns ---
    col_w = 316
    col_x = [22, 22 + col_w + gap, 22 + 2 * (col_w + gap)]
    y = sy + 26 + 12
    bottom = y
    for ci, col in enumerate(COLUMNS):
        cy = y
        for sec_title, items in col:
            color = SECTION_COLORS[sec_title]
            d.rectangle([col_x[ci], cy, col_x[ci] + col_w, cy + 26], fill=color)
            d.text((col_x[ci] + 8, cy + 5), sec_title, font=SANS_B(13), fill=(255, 255, 255))
            cy += 26 + 8
            for lead, deck in items:
                cy = draw_wrapped(d, col_x[ci] + 2, cy, lead, SANS_B(15), col_w - 4, INK, leading=18)
                cy = draw_wrapped(d, col_x[ci] + 2, cy, deck, SANS(13), col_w - 4, (70, 68, 62), leading=16)
                cy += 5
            cy += 4
        bottom = max(bottom, cy)

    # --- also in brief + markets ---
    fy = 934
    d.rectangle([22, fy - 8, W - 22, fy - 6], fill=LIGHT_LINE)
    d.text((22, fy), "ALSO IN BRIEF:", font=SANS_B(12), fill=RED)
    yy = draw_wrapped(d, 22, fy + 17, ALSO, SANS(12), W - 44, (70, 68, 62), leading=15)
    my = 976
    d.rectangle([0, my, W, my + 28], fill=INK)
    d.text(((W - d.textlength(MARKETS, font=SANS_B(12))) / 2, my + 8), MARKETS, font=SANS_B(12), fill=(255, 255, 255))
    d.text((22, 1006), "Sources: wire reports first published on Tuesday 17 November 2026.",
           font=SANS(11), fill=GREY)
    d.text((W - 22 - d.textlength("THE WORLD IN ONE DAY", font=SANS_B(11)), 1006),
           "THE WORLD IN ONE DAY", font=SANS_B(11), fill=GREY)

    img.save(out_path, format="PNG")
    print(f"variant {variant}: wrote {out_path}  bottom-of-columns y={bottom}  also-block ends y={yy}")
    return out_path


if __name__ == "__main__":
    variant = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    out = sys.argv[2] if len(sys.argv) > 2 else "entry.png"
    build(variant, out)

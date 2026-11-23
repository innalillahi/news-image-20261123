#!/usr/bin/env python3
"""Generate entry.png: one image summing up world news, Monday 23 November 2026.

Pure PIL, no network, deterministic output (fixed palette, fixed layout,
PNG saved with fixed settings). Run: python3 draw.py
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"

BG = (11, 24, 48)          # deep navy
HEADER_BG = (11, 24, 48)
GOLD = (245, 184, 0)
WHITE = (255, 255, 255)
INK = (18, 28, 46)
CARD = (255, 255, 255)
SUB = (70, 82, 100)
TICKER_BG = (16, 36, 66)
TICKER_FG = (214, 224, 238)


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


F_TITLE = font("DejaVuSans-Bold.ttf", 76)
F_DATE = font("DejaVuSans-Bold.ttf", 58)
F_SUB = font("DejaVuSans-Bold.ttf", 22)
F_TAG = font("DejaVuSans-Bold.ttf", 19)
F_HEAD = font("DejaVuSans-Bold.ttf", 28)
F_BODY = font("DejaVuSans.ttf", 20)
F_TICK = font("DejaVuSans.ttf", 17)
F_TICK_B = font("DejaVuSans-Bold.ttf", 20)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap to pixel width."""
    lines = []
    for para in text.split("\n"):
        words, line = para.split(), ""
        for w in words:
            trial = (line + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= max_w:
                line = trial
            else:
                if line:
                    lines.append(line)
                line = w
        if line:
            lines.append(line)
    return lines


# (tag, accent colour, headline, subline) — bodies kept to ~80 chars (2 lines)
STORIES = [
    ("CLIMATE", (198, 40, 40),
     "COP31 ends with no deal",
     "Longest UN climate summit ever. EU and Pacific islands reject the draft."),
    ("MIDDLE EAST", (176, 92, 0),
     "Iran strikes Bahrain",
     "IRGC missiles and drones hit US positions; 2 hurt. Air defences stop most."),
    ("IRAN TALKS", (122, 63, 160),
     "Trump: Iran wants a deal",
     "Not one that is \u201cacceptable\u201d, Trump says. He wants a real deal, not a fake one."),
    ("UKRAINE", (0, 90, 158),
     "Russia hits Kryvyi Rih",
     "Overnight strike kills a child and a young woman; 11 victims. 25 blocks hit."),
    ("NATO", (0, 120, 90),
     "NATO: \u201cevery inch\u201d of Poland",
     "Rutte vows to defend Poland after Russia violates its airspace with 3 objects."),
    ("GAZA", (176, 92, 0),
     "Gaza truck strike kills 3",
     "Israeli strike on a truck carrying food. WCK: no affiliation with the truck."),
]

# Terse ticker items; joined with bullet separators and wrapped as one paragraph.
TICKER_ITEMS = [
    "Dymer drone strike near Kyiv: 14 missing, 11 victims",
    "Ukraine hits Russian ships in the Baltic and Libya",
    "US: Democrats' biggest House majority in three decades",
    "Hubbard beats Foxx by 330 votes in North Carolina",
    "Alcaraz wins first ATP Finals title in Turin",
    "Denmark expels Russian attache over Kyivstoner plot",
    "Zelenskyy calls Putin a \u201cmurderer\u201d",
    "Eisenkot: settler arson is \u201cJewish terrorism\u201d",
    "Bangladesh to jail Hasina if she returns from India",
    "South Korea: first woman to head the NIS",
    "France: police beating of Zecler ruled racist",
    "Thailand upholds lese-majeste verdict, 3 years",
    "Thailand halts Cambodia ceasefire after mine blast",
    "\u201cChapo Isidro\u201d arrested in Mexico",
    "ICE detains father and daughter at Seattle airport",
    "Trump to block US data centres abroad",
    "SEC probes Nvidia accounting",
    "Oregon and Virginia sue SpaceX over Grok",
    "South Korea education minister quits over AI-cheating row",
    "NATO intel: Russia plans nuclear-armed satellite",
    "EU open to closest ties with UK",
    "Molly Meldrum dies aged 83",
    "Lebanese villagers return home",
    "SoftBank to invest $2bn in Intel",
    "US to detonate bomb chemicals in Iowa",
]


def draw_card(d, x, y, w, h, tag, accent, head, body):
    d.rounded_rectangle([x, y, x + w, y + h], radius=12, fill=CARD)
    d.rectangle([x, y, x + 10, y + h], fill=accent)
    tx, ty = x + 24, y + 12
    d.text((tx, ty), tag, font=F_TAG, fill=accent)
    ty += 26
    for ln in wrap(d, head, F_HEAD, w - 48):
        d.text((tx, ty), ln, font=F_HEAD, fill=INK)
        ty += 34
    ty += 2
    for ln in wrap(d, body, F_BODY, w - 48)[:2]:
        d.text((tx, ty), ln, font=F_BODY, fill=SUB)
        ty += 26


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # Header
    d.text((32, 18), "MONDAY", font=F_TITLE, fill=WHITE)
    d.text((32, 92), "23 NOVEMBER 2026", font=F_DATE, fill=GOLD)
    d.text((740, 40), "THE WORLD", font=F_SUB, fill=(160, 180, 205))
    d.text((740, 68), "IN ONE IMAGE", font=F_SUB, fill=(160, 180, 205))
    d.text((740, 96), "30 STORIES", font=F_SUB, fill=GOLD)
    d.rectangle([32, 170, 992, 174], fill=GOLD)

    # 2 x 3 grid of big stories
    gx, gy = 24, 186
    cw, ch, gap = 476, 168, 12
    for i, (tag, accent, head, body) in enumerate(STORIES):
        x = gx + (i % 2) * (cw + gap)
        y = gy + (i // 2) * (ch + gap)
        draw_card(d, x, y, cw, ch, tag, accent, head, body)

    # Ticker: the rest of the day
    ty0 = gy + 3 * ch + 2 * gap + 12  # 726
    d.rounded_rectangle([24, ty0, 1000, H - 20], radius=12, fill=TICKER_BG)
    d.text((44, ty0 + 8), "ALSO TODAY", font=F_TICK_B, fill=GOLD)
    ticker_text = "  \u2022  ".join(TICKER_ITEMS)
    lines = wrap(d, ticker_text, F_TICK, 932)
    ly = ty0 + 36
    for ln in lines:
        if ly + 20 > H - 24:
            break
        d.text((44, ly), ln, font=F_TICK, fill=TICKER_FG)
        ly += 20
    assert ly <= H - 20, "ticker overflowed: %d lines" % len(lines)

    img.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    main()

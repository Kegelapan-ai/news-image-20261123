#!/usr/bin/env python3
"""Draw the 23 November 2026 front page: one 1024x1024 PNG.

Everything here is local and fixed: system DejaVu fonts, no clock,
no random numbers, no network. Running this twice writes the same bytes.
"""

import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "image.png")

W, H = 1024, 1024
PAPER = (251, 247, 236)
INK = (26, 26, 26)
RULE = (26, 26, 26)
ACCENT = (178, 38, 30)
CARD_BG = (255, 255, 255)
LEAD_BG = (245, 238, 221)
FOOT_BG = (239, 233, 216)
MUTED = (90, 84, 70)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_MAST = font("DejaVuSerif-Bold.ttf", 56)
F_DATE = font("DejaVuSans-Bold.ttf", 20)
F_SUB = font("DejaVuSans.ttf", 15)
F_KICK = font("DejaVuSans-Bold.ttf", 13)
F_HEAD = font("DejaVuSerif-Bold.ttf", 21)
F_HEAD_LEAD = font("DejaVuSerif-Bold.ttf", 29)
F_HEAD_STRIP = font("DejaVuSerif-Bold.ttf", 22)
F_BODY = font("DejaVuSans.ttf", 15)
F_BODY_LEAD = font("DejaVuSans.ttf", 16)
F_FOOT = font("DejaVuSans.ttf", 12)
F_FOOT_B = font("DejaVuSans-Bold.ttf", 12)
F_SRC = font("DejaVuSans.ttf", 11)


def wrap(draw, text, fnt, width):
    """Greedy word wrap on pixel width; returns a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_lines(draw, text, fnt, width, max_lines):
    """Wrap text and clip to max_lines, adding an ellipsis if cut."""
    lines = wrap(draw, text, fnt, width)
    if len(lines) <= max_lines:
        return lines
    print("WARNING: text clipped to %d lines: %r" % (max_lines, text[:60]),
          file=sys.stderr)
    cut = lines[:max_lines]
    while cut and draw.textlength(cut[-1] + " ...", font=fnt) > width:
        cut[-1] = cut[-1].rsplit(" ", 1)[0] if " " in cut[-1] else ""
    cut[-1] = (cut[-1] + " ...").strip()
    return cut


# ---------------------------------------------------------------- icons
# Each icon draws simple shapes inside a square box (x, y, size).


def icon_shield(d, x, y, s):
    pts = [(x + s // 2, y + 2), (x + s - 6, y + 12), (x + s - 6, y + s // 2),
           (x + s // 2, y + s - 4), (x + 6, y + s // 2), (x + 6, y + 12)]
    d.polygon(pts, outline=INK, width=3)
    cx, cy, r = x + s // 2, y + s // 2 - 2, 11
    star = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        star.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(star, fill=ACCENT)


def icon_warship(d, x, y, s):
    # hull
    d.polygon([(x + 6, y + s - 24), (x + s - 6, y + s - 24),
               (x + s - 14, y + s - 10), (x + 14, y + s - 10)],
              outline=INK, width=2)
    # superstructure + mast
    d.rectangle([x + 22, y + s - 42, x + 40, y + s - 24], outline=INK, width=2)
    d.line([x + 31, y + s - 42, x + 31, y + s - 52], fill=INK, width=2)
    d.polygon([(x + 27, y + s - 52), (x + 35, y + s - 52), (x + 31, y + s - 58)],
              fill=ACCENT)
    # listing / sinking tilt: waves over the bow
    d.arc([x + 6, y + s - 10, x + 26, y + s + 4], 180, 360, fill=INK, width=2)
    d.arc([x + s - 28, y + s - 10, x + s - 8, y + s + 4], 180, 360,
          fill=INK, width=2)
    # small drone overhead
    d.line([x + 44, y + 4, x + s - 4, y + 4], fill=INK, width=2)
    d.ellipse([x + s - 12, y + 2, x + s - 6, y + 8], outline=INK, width=2)


def icon_flats(d, x, y, s):
    d.rectangle([x + 8, y + 18, x + 30, y + s - 6], outline=INK, width=2)
    d.rectangle([x + 34, y + 10, x + s - 8, y + s - 6], outline=INK, width=2)
    for wx in (x + 13, x + 21):
        for wy in (y + 24, y + 34, y + 44):
            d.rectangle([wx, wy, wx + 5, wy + 5], fill=INK)
    for wx in (x + 40, x + 48):
        for wy in (y + 16, y + 26, y + 36, y + 46):
            d.rectangle([wx, wy, wx + 5, wy + 5], fill=INK)
    # crack down the taller block
    d.line([x + 44, y + 10, x + 40, y + 30, x + 48, y + 48], fill=ACCENT, width=2)
    # tiny drone overhead
    d.line([x + 44, y + 2, x + s - 4, y + 2], fill=INK, width=2)
    d.ellipse([x + s - 12, y, x + s - 6, y + 6], outline=INK, width=2)


def icon_factory(d, x, y, s):
    d.rectangle([x + 8, y + 26, x + s - 8, y + s - 6], outline=INK, width=2)
    d.line([x + 8, y + 26, x + 18, y + 16, x + 28, y + 26, x + 38, y + 16,
            x + 48, y + 26], fill=INK, width=2)
    d.rectangle([x + s - 16, y + 8, x + s - 10, y + 26], fill=INK)
    d.polygon([(x + s - 19, y + 2), (x + s - 13, y - 6), (x + s - 7, y + 2)],
              fill=ACCENT)
    for wx in (x + 13, x + 25, x + 37):
        d.rectangle([wx, y + 34, wx + 7, y + 41], fill=INK)
    d.polygon([(x + 16, y + s - 6), (x + 26, y + s - 20), (x + 36, y + s - 6)],
              fill=ACCENT)


def icon_tanker(d, x, y, s):
    # tanker hull with deck tanks
    d.polygon([(x + 4, y + s - 24), (x + s - 4, y + s - 24),
               (x + s - 12, y + s - 8), (x + 12, y + s - 8)],
              outline=INK, width=2)
    for cx in (x + 14, x + 28, x + 42):
        d.ellipse([cx, y + s - 40, cx + 11, y + s - 29], outline=INK, width=2)
    d.rectangle([x + s - 12, y + s - 40, x + s - 6, y + s - 24], fill=INK)
    # flame above the middle tank
    d.polygon([(x + 28, y + s - 44), (x + 33, y + s - 56),
               (x + 38, y + s - 44)], fill=ACCENT)
    d.line([x + 4, y + s - 2, x + s - 4, y + s - 2], fill=INK, width=2)
    d.arc([x + 8, y + s - 10, x + 26, y + s + 4], 180, 360, fill=INK, width=2)
    d.arc([x + s - 28, y + s - 10, x + s - 10, y + s + 4], 180, 360,
          fill=INK, width=2)


def icon_route(d, x, y, s):
    # winding road through mountains, with a flag at the far end
    d.polygon([(x + 6, y + s - 14), (x + 22, y + 22), (x + 34, y + s - 14)],
              outline=INK, width=2)
    d.polygon([(x + 26, y + s - 14), (x + 44, y + 30), (x + 58, y + s - 14)],
              outline=INK, width=2)
    d.line([x + 8, y + s - 8, x + s - 8, y + s - 8], fill=INK, width=3)
    for i in range(4):
        px = x + 14 + i * 12
        d.line([px, y + s - 8, px + 6, y + s - 8], fill=PAPER, width=3)
    d.line([x + s - 12, y + 6, x + s - 12, y + 26], fill=INK, width=2)
    d.polygon([(x + s - 12, y + 6), (x + s - 2, y + 11), (x + s - 12, y + 16)],
              fill=ACCENT)


# ---------------------------------------------------------------- cards

def story_card(d, x, y, w, h, kicker, headline, body, icon, bg=CARD_BG):
    d.rectangle([x, y, x + w, y + h], fill=bg, outline=RULE, width=2)
    ix, iy, isize = x + 12, y + 40, 64
    icon(d, ix, iy, isize)
    tx = x + 92
    tw = w - 92 - 14
    d.text((tx, y + 10), kicker, font=F_KICK, fill=ACCENT)
    head = fit_lines(d, headline, F_HEAD, tw, 2)
    hy = y + 32
    for line in head:
        d.text((tx, hy), line, font=F_HEAD, fill=INK)
        hy += 26
    body_lines = fit_lines(d, body, F_BODY, tw, 4)
    by = hy + 6
    for line in body_lines:
        d.text((tx, by), line, font=F_BODY, fill=INK)
        by += 19
    # safety: nothing may run past the card's inner bottom edge
    assert by - 19 <= y + h - 10, "card text overflow: %s" % kicker


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([14, 14, W - 15, H - 15], outline=RULE, width=2)

    # ---- top strip
    d.text((30, 26), "THE WORLD  •  ONE DAY  •  ONE PAGE", font=F_KICK,
           fill=MUTED)
    right = "No. 327  •  2026"
    d.text((W - 30 - d.textlength(right, font=F_KICK), 26), right,
           font=F_KICK, fill=MUTED)

    # ---- masthead
    title = "THE DAY IN THE WORLD"
    d.text(((W - d.textlength(title, font=F_MAST)) // 2, 52), title,
           font=F_MAST, fill=INK)
    d.line([30, 128, W - 30, 128], fill=ACCENT, width=4)
    date = "MONDAY  23  NOVEMBER  2026"
    d.text(((W - d.textlength(date, font=F_DATE)) // 2, 138), date,
           font=F_DATE, fill=ACCENT)
    sub = "Six stories that summed up the day — from Brussels to Benghazi, Cikande to Yerevan."
    d.text(((W - d.textlength(sub, font=F_SUB)) // 2, 166), sub,
           font=F_SUB, fill=MUTED)

    # ---- lead story: NATO / Poland, full width
    lx, ly, lw, lh = 30, 196, W - 60, 148
    d.rectangle([lx, ly, lx + lw, ly + lh], fill=LEAD_BG, outline=RULE,
                width=2)
    icon_shield(d, lx + 14, ly + 42, 66)
    tx = lx + 100
    tw = lw - 100 - 16
    d.text((tx, ly + 10), "NATO  •  LEAD STORY", font=F_KICK, fill=ACCENT)
    lead_head = "NATO MEETS AFTER MISSILES LAND IN POLAND"
    assert d.textlength(lead_head, font=F_HEAD_LEAD) <= tw, "lead head too wide"
    d.text((tx, ly + 32), lead_head, font=F_HEAD_LEAD, fill=INK)
    lead_body = (
        "NATO ambassadors meet in Brussels on Monday after three Russian "
        "Kh-101 cruise missiles flew into Polish airspace on Friday and "
        "crashed in the south-east. NATO chief Mark Rutte said the alliance "
        "will defend “every inch” of Polish territory."
    )
    lines = fit_lines(d, lead_body, F_BODY_LEAD, tw, 3)
    by = ly + 74
    for line in lines:
        d.text((tx, by), line, font=F_BODY_LEAD, fill=INK)
        by += 21
    assert by - 21 <= ly + lh - 10, "lead text overflow"

    # ---- four-card grid
    gx, gy = 30, 356
    cw, ch, gap = 477, 200, 10
    cards = [
        ("LIBYA  •  UKRAINE",
         "Ukraine says sea drones sank a Russian warship",
         "President Zelenskyy said on Monday that seven Ukrainian naval "
         "drones sank the Russian corvette Merkury off Libya. The cargo "
         "ship MV Angara was also hit.",
         icon_warship),
        ("UKRAINE",
         "Dymer toll rises to 11 after drone hits flats",
         "The death toll rose to 11 on Monday after rescuers pulled another "
         "body from a block of flats in Dymer, near Kyiv, hit by a Russian "
         "drone on Sunday. Nine people were rescued.",
         icon_flats),
        ("INDONESIA",
         "Factory fire kills 24; about 30 still missing",
         "Indonesia confirmed on Monday that 24 people died in a fire that "
         "tore through a candy factory in Cikande, Banten, on Saturday "
         "evening. Rescuers were still searching the burned-out building.",
         icon_factory),
        ("THE GULF  •  IRAN",
         "Iran vows to fight US blockade “with all tools”",
         "Iran said on Monday it will use all available means to confront "
         "the US naval blockade of its ports. President Trump had said on "
         "Sunday that US forces would sink ships trying to break it.",
         icon_tanker),
    ]
    for i, (kick, head, body, icon) in enumerate(cards):
        cx = gx + (i % 2) * (cw + gap)
        cy = gy + (i // 2) * (ch + gap)
        story_card(d, cx, cy, cw, ch, kick, head, body, icon)

    # ---- TRIPP strip, full width
    sx, sy, sw, sh = 30, 778, W - 60, 100
    d.rectangle([sx, sy, sx + sw, sy + sh], fill=CARD_BG, outline=RULE,
                width=2)
    icon_route(d, sx + 12, sy + 14, 62)
    tx = sx + 92
    d.text((tx, sy + 8), "CAUCASUS  •  ARMENIA", font=F_KICK, fill=ACCENT)
    d.text((tx, sy + 28), "“Trump Route” breaks ground in Armenia",
           font=F_HEAD_STRIP, fill=INK)
    strip_body = (
        "Armenia launched the US-backed Trump Route for International Peace "
        "and Prosperity on Monday, linking mainland Azerbaijan with its "
        "Nakhchivan exclave through Armenian territory."
    )
    lines = fit_lines(d, strip_body, F_BODY, sw - 92 - 14, 2)
    by = sy + 56
    for line in lines:
        d.text((tx, by), line, font=F_BODY, fill=INK)
        by += 19
    assert by - 19 <= sy + sh - 8, "strip text overflow"

    # ---- footer: also today (weekend stories, dated), 2 x 2
    fx, fy, fw, fh = 30, 890, W - 60, 92
    d.rectangle([fx, fy, fx + fw, fy + fh], fill=FOOT_BG, outline=RULE,
                width=2)
    d.text((fx + 12, fy + 6), "ALSO — FROM THE WEEKEND", font=F_KICK, fill=ACCENT)
    foot_items = [
        ("USA — ", "Democrats won at least 258 House seats on Sunday, their "
         "biggest majority since 1992, AP and Reuters reported."),
        ("USA — ", "More than 1,600 Delta flights were delayed on Sunday "
         "after a weight-and-balance system failure, days before "
         "Thanksgiving."),
        ("CLIMATE — ", "The COP31 summit in Türkiye ended on Sunday with no "
         "deal — the longest climate talks ever, after two days of overtime."),
        ("GAZA — ", "Israeli forces hit a truck in Gaza on Saturday and "
         "three people were killed, Gaza’s Health Ministry said."),
    ]
    cell_w, cell_h = (fw - 24) // 2, 30
    for i, (lead, rest) in enumerate(foot_items):
        cell_x = fx + 12 + (i % 2) * cell_w
        cell_y = fy + 26 + (i // 2) * cell_h
        full = lead + rest
        lines = fit_lines(d, full, F_FOOT, cell_w - 8, 2)
        ly2 = cell_y
        for line in lines:
            # bold the lead-in on the first line only
            if line is lines[0] and line.startswith(lead):
                d.text((cell_x, ly2), lead, font=F_FOOT_B, fill=INK)
                d.text((cell_x + d.textlength(lead, font=F_FOOT_B), ly2),
                       line[len(lead):], font=F_FOOT, fill=INK)
            else:
                d.text((cell_x, ly2), line, font=F_FOOT, fill=INK)
            ly2 += 15
        assert ly2 - 16 <= cell_y + cell_h - 2, "footer overflow"

    # ---- sources line
    src = ("Sources: Reuters  •  AP  •  Just Security  •  RIA Novosti — figures as "
           "reported on 23 Nov 2026.")
    d.text(((W - d.textlength(src, font=F_SRC)) // 2, 992), src,
           font=F_SRC, fill=MUTED)

    img.save(OUT, format="PNG")
    print("wrote", OUT)


if __name__ == "__main__":
    build()

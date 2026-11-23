#!/usr/bin/env python3
"""Paint the 23 November 2026 front page and save it as image.png.

Everything here is drawn with Pillow from fixed coordinates, so the
result is the same on every run: no clock, no random numbers, no
network, no input files other than the fonts already on the system.
Run it from the repository root; it writes ./image.png next to itself.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- palette
PAPER = (250, 244, 232)      # warm cream, like old newsprint
PAPER_SOFT = (243, 236, 220) # slightly deeper cream for the lead box
INK = (18, 18, 18)           # near-black for rules and body copy
GREY = (88, 82, 74)          # small print and the subtitle
FLAG_RED = (178, 34, 28)     # the one accent colour, used sparingly
WHITE = (255, 255, 255)

SIDE = 1024
HERE = Path(__file__).resolve().parent
OUT_PATH = HERE / "image.png"

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")


def pick_font(name: str, size: int) -> ImageFont.FreeTypeFont:
    """Load a DejaVu face; fall back to Pillow's built-in font if missing."""
    try:
        return ImageFont.truetype(str(FONT_DIR / name), size)
    except OSError:
        return ImageFont.load_default()


# ------------------------------------------------------------ text helper
def flow_words(draw: ImageDraw.ImageDraw, words: str, font, limit: int):
    """Split *words* into lines no wider than *limit* pixels.

    Returns a list of strings.  A single over-long word is left whole
    rather than chopped in half, so nothing ever comes out hyphenated
    in a surprising place.
    """
    lines, current = [], ""
    for piece in words.split():
        trial = f"{current} {piece}".strip()
        if draw.textlength(trial, font=font) <= limit or not current:
            current = trial
        else:
            lines.append(current)
            current = piece
    if current:
        lines.append(current)
    return lines


def put_lines(draw, lines, x, y, font, colour=INK, gap=4):
    """Draw *lines* top to bottom starting at (x, y); return the y below."""
    for line in lines:
        draw.text((x, y), line, font=font, fill=colour)
        y += font.size + gap
    return y


# -------------------------------------------------------------- tiny icons
# Each icon lives in a small box anchored at (x, y).  They are all drawn
# from straight lines and simple shapes, in ink with one red accent.

def icon_shield(draw, x, y):
    import math
    pts = [(x + 28, y), (x + 56, y + 10), (x + 56, y + 34),
           (x + 28, y + 56), (x, y + 34), (x, y + 10)]
    draw.polygon(pts, outline=INK, width=3)
    cx, cy, r = x + 28, y + 28, 11
    star = []
    for i in range(10):
        ang = -90 + i * 36
        rad = r if i % 2 == 0 else r * 0.45
        star.append((cx + rad * math.cos(math.radians(ang)),
                     cy + rad * math.sin(math.radians(ang))))
    draw.polygon(star, fill=FLAG_RED)


def icon_boat(draw, x, y):
    draw.line([(x + 10, y + 44), (x + 52, y + 44)], fill=INK, width=3)
    draw.line([(x + 6, y + 50), (x + 56, y + 50)], fill=INK, width=2)
    draw.polygon([(x + 12, y + 28), (x + 50, y + 28), (x + 44, y + 44),
                  (x + 18, y + 44)], outline=INK, width=3)
    draw.rectangle([x + 24, y + 12, x + 38, y + 28], outline=INK, width=3)
    draw.line([(x + 31, y + 12), (x + 31, y + 2)], fill=INK, width=2)
    draw.polygon([(x + 31, y + 2), (x + 31, y + 10), (x + 38, y + 6)],
                 fill=FLAG_RED)
    draw.line([(x + 52, y + 18), (x + 62, y + 18)], fill=INK, width=2)
    draw.polygon([(x + 62, y + 18), (x + 56, y + 14), (x + 56, y + 22)],
                 fill=INK)


def icon_blocks(draw, x, y):
    draw.rectangle([x + 2, y + 16, x + 26, y + 56], outline=INK, width=3)
    draw.rectangle([x + 32, y + 4, x + 56, y + 56], outline=INK, width=3)
    for wx in (8, 16):
        for wy in (24, 34, 44):
            draw.rectangle([x + wx, y + wy, x + wx + 5, y + wy + 5],
                           outline=INK, width=1)
    for wx in (38, 46):
        for wy in (12, 22, 32, 42):
            draw.rectangle([x + wx, y + wy, x + wx + 5, y + wy + 5],
                           outline=INK, width=1)
    draw.line([(x + 44, y + 4), (x + 38, y + 22), (x + 46, y + 34),
               (x + 40, y + 56)], fill=FLAG_RED, width=3)


def icon_works(draw, x, y):
    draw.polygon([(x + 2, y + 26), (x + 22, y + 12), (x + 42, y + 26)],
                 outline=INK, width=3)
    draw.rectangle([x + 2, y + 26, x + 42, y + 56], outline=INK, width=3)
    draw.rectangle([x + 44, y + 6, x + 52, y + 56], outline=INK, width=3)
    draw.polygon([(x + 44, y + 6), (x + 52, y + 6), (x + 50, y - 4),
                  (x + 46, y - 4)], fill=FLAG_RED)
    for fx in (10, 22, 34):
        draw.rectangle([x + fx, y + 38, x + fx + 6, y + 44], fill=INK)
    draw.polygon([(x + 24, y + 56), (x + 32, y + 40), (x + 40, y + 56)],
                 fill=FLAG_RED)


def icon_tanker(draw, x, y):
    draw.line([(x + 31, y), (x + 31, y + 10)], fill=INK, width=2)
    draw.polygon([(x + 31, y), (x + 31, y + 8), (x + 38, y + 4)],
                 fill=FLAG_RED)
    for cx in (14, 31, 48):
        draw.ellipse([x + cx - 8, y + 12, x + cx + 8, y + 28],
                     outline=INK, width=3)
    draw.polygon([(x + 4, y + 32), (x + 58, y + 32), (x + 52, y + 48),
                  (x + 10, y + 48)], outline=INK, width=3)
    draw.line([(x + 8, y + 54), (x + 54, y + 54)], fill=INK, width=2)


def icon_peaks(draw, x, y):
    draw.polygon([(x, y + 48), (x + 22, y + 14), (x + 44, y + 48)],
                 outline=INK, width=3)
    draw.polygon([(x + 26, y + 48), (x + 46, y + 20), (x + 62, y + 48)],
                 outline=INK, width=3)
    for dx in range(0, 58, 10):
        draw.line([(x + dx, y + 54), (x + dx + 5, y + 54)], fill=INK, width=3)
    draw.line([(x + 52, y + 20), (x + 52, y + 2)], fill=INK, width=2)
    draw.polygon([(x + 52, y + 2), (x + 52, y + 10), (x + 60, y + 6)],
                 fill=FLAG_RED)


ICONS = {
    "shield": icon_shield,
    "boat": icon_boat,
    "blocks": icon_blocks,
    "works": icon_works,
    "tanker": icon_tanker,
    "peaks": icon_peaks,
}

# ------------------------------------------------------------------- copy
# Every sentence below was checked against live reporting for 23 Nov 2026.
# Anything that stayed unconfirmed was left out (see README).

LEAD = {
    "kicker": "NATO  •  LEAD STORY",
    "icon": "shield",
    "headline": "NATO MEETS AFTER MISSILES LAND IN POLAND",
    "body": ("NATO ambassadors meet in Brussels on Monday after three Russian "
             "Kh-101 cruise missiles flew into Polish airspace on Friday and "
             "crashed in the south-east. NATO chief Mark Rutte said the "
             "alliance will defend \u201cevery inch\u201d of Polish territory."),
}

GRID = [
    {
        "kicker": "LIBYA  •  UKRAINE",
        "icon": "boat",
        "headline": "Ukraine says sea drones sank a Russian warship",
        "body": ("President Zelenskyy said on Monday that seven Ukrainian naval "
                 "drones sank the Russian corvette Merkury off Libya. The cargo "
                 "ship MV Angara was also hit."),
    },
    {
        "kicker": "UKRAINE",
        "icon": "blocks",
        "headline": "Dymer toll rises to 11 after drone hits flats",
        "body": ("The death toll rose to 11 on Monday after rescuers pulled "
                 "another body from a block of flats in Dymer, near Kyiv, hit "
                 "by a Russian drone on Sunday. Nine people were rescued."),
    },
    {
        "kicker": "INDONESIA",
        "icon": "works",
        "headline": "Factory fire kills 24; about 30 still missing",
        "body": ("Indonesia confirmed on Monday that 24 people died in a fire "
                 "that tore through a candy factory in Cikande, Banten, on "
                 "Saturday evening. Rescuers were still searching the "
                 "burned-out building."),
    },
    {
        "kicker": "THE GULF  •  IRAN",
        "icon": "tanker",
        "headline": "Iran vows to fight US blockade \u201cwith all tools\u201d",
        "body": ("Iran said on Monday it will use all available means to "
                 "confront the US naval blockade of its ports. President Trump "
                 "had said on Sunday that US forces would sink ships trying "
                 "to break it."),
    },
]

WIDE = {
    "kicker": "CAUCASUS  •  ARMENIA",
    "icon": "peaks",
    "headline": "\u201cTrump Route\u201d breaks ground in Armenia",
    "body": ("Armenia launched the US-backed Trump Route for International Peace "
             "and Prosperity on Monday, linking mainland Azerbaijan with its "
             "Nakhchivan exclave through Armenian territory."),
}

ALSO = [
    ("USA", "Democrats won at least 258 House seats on Sunday, their biggest "
            "majority since 1992, AP and Reuters reported."),
    ("CLIMATE", "The COP31 summit in T\u00fcrkiye ended on Sunday with no deal "
                "\u2014 the longest climate talks ever, after two days of overtime."),
    ("USA", "More than 1,600 Delta flights were delayed on Sunday after a "
            "weight-and-balance system failure, days before Thanksgiving."),
    ("GAZA", "Israeli forces hit a truck in Gaza on Saturday and three people "
             "were killed, Gaza\u2019s Health Ministry said."),
]

SOURCES_LINE = ("Sources: Reuters  •  AP  •  Just Security  •  RIA Novosti "
                "\u2014 figures as reported on 23 Nov 2026.")

# ------------------------------------------------------------------ layout
def paint_page() -> Image.Image:
    """Draw the whole front page and return the finished image."""
    canvas = Image.new("RGB", (SIDE, SIDE), PAPER)
    draw = ImageDraw.Draw(canvas)

    serif_big = pick_font("DejaVuSerif-Bold.ttf", 58)
    serif_head = pick_font("DejaVuSerif-Bold.ttf", 29)
    serif_card = pick_font("DejaVuSerif-Bold.ttf", 24)
    serif_wide = pick_font("DejaVuSerif-Bold.ttf", 26)
    sans_bold = pick_font("DejaVuSans-Bold.ttf", 15)
    sans_bold_sm = pick_font("DejaVuSans-Bold.ttf", 13)
    sans = pick_font("DejaVuSans.ttf", 17)
    sans_body = pick_font("DejaVuSans.ttf", 16)
    sans_small = pick_font("DejaVuSans.ttf", 13)

    # Double rule framing the page.
    draw.rectangle([10, 10, SIDE - 11, SIDE - 11], outline=INK, width=2)
    draw.rectangle([16, 16, SIDE - 17, SIDE - 17], outline=INK, width=1)

    # --- top strip ------------------------------------------------------
    draw.text((28, 26), "THE WORLD  •  ONE DAY  •  ONE PAGE",
              font=sans_bold_sm, fill=GREY)
    right = "No. 327  •  2026"
    draw.text((SIDE - 28 - draw.textlength(right, font=sans_bold_sm), 26),
              right, font=sans_bold_sm, fill=GREY)

    # --- masthead -------------------------------------------------------
    title = "THE DAY IN THE WORLD"
    draw.text(((SIDE - draw.textlength(title, font=serif_big)) / 2, 46),
              title, font=serif_big, fill=INK)
    draw.rectangle([28, 126, SIDE - 28, 130], fill=FLAG_RED)

    date_line = "MONDAY  23  NOVEMBER  2026"
    date_font = pick_font("DejaVuSans-Bold.ttf", 22)
    draw.text(((SIDE - draw.textlength(date_line, font=date_font)) / 2, 138),
              date_line, font=date_font, fill=FLAG_RED)
    sub = ("Six stories that summed up the day \u2014 from Brussels to "
           "Benghazi, Cikande to Yerevan.")
    draw.text(((SIDE - draw.textlength(sub, font=sans)) / 2, 168),
              sub, font=sans, fill=GREY)

    # --- lead story -----------------------------------------------------
    lx, ly, lw, lh = 28, 196, SIDE - 56, 136
    draw.rectangle([lx, ly, lx + lw, ly + lh], fill=PAPER_SOFT,
                   outline=INK, width=2)
    ICONS[LEAD["icon"]](draw, lx + 14, ly + 42)
    tx = lx + 92
    draw.text((tx, ly + 10), LEAD["kicker"], font=sans_bold, fill=FLAG_RED)
    draw.text((tx, ly + 32), LEAD["headline"], font=serif_head, fill=INK)
    body_lines = flow_words(draw, LEAD["body"], sans_body, lw - 110)
    put_lines(draw, body_lines, tx, ly + 70, sans_body, gap=3)

    # --- the 2 x 2 grid --------------------------------------------------
    gx, gy = 28, 342
    cw, ch, gap = 472, 208, 16
    for idx, story in enumerate(GRID):
        cx = gx + (idx % 2) * (cw + gap)
        cy = gy + (idx // 2) * (ch + gap)
        draw.rectangle([cx, cy, cx + cw, cy + ch], fill=WHITE,
                       outline=INK, width=2)
        ICONS[story["icon"]](draw, cx + 16, cy + 40)
        kx = cx + 92
        draw.text((kx, cy + 12), story["kicker"], font=sans_bold,
                  fill=FLAG_RED)
        head_lines = flow_words(draw, story["headline"], serif_card, cw - 110)
        put_lines(draw, head_lines, kx, cy + 34, serif_card, gap=1)
        body = flow_words(draw, story["body"], sans_body, cw - 34)
        put_lines(draw, body, cx + 17, cy + 118, sans_body, gap=3)

    # --- wide strip: the Caucasus ---------------------------------------
    # Taller than a first draft, so the two-line body sits inside the box.
    wx, wy, ww, wh = 28, 784, SIDE - 56, 92
    draw.rectangle([wx, wy, wx + ww, wy + wh], fill=WHITE,
                   outline=INK, width=2)
    ICONS[WIDE["icon"]](draw, wx + 14, wy + 12)
    tx = wx + 92
    draw.text((tx, wy + 8), WIDE["kicker"], font=sans_bold, fill=FLAG_RED)
    draw.text((tx, wy + 28), WIDE["headline"], font=serif_wide, fill=INK)
    wide_body = flow_words(draw, WIDE["body"], sans_small, ww - 110)
    put_lines(draw, wide_body, tx, wy + 58, sans_small, gap=1)

    # --- also, from the weekend -----------------------------------------
    # Each item takes two lines, so rows are spaced 30 apart, not 26.
    # The first line shares its row with the label, so it is wrapped
    # narrow; the rest gets the full column width, so nothing is cut.
    ax, ay, aw, ah = 28, 886, SIDE - 56, 96
    draw.rectangle([ax, ay, ax + aw, ay + ah], fill=PAPER_SOFT,
                   outline=INK, width=2)
    draw.text((ax + 12, ay + 7), "ALSO \u2014 FROM THE WEEKEND",
              font=sans_bold, fill=FLAG_RED)
    col_w = (aw - 36) // 2
    for i, (tag, text) in enumerate(ALSO):
        col_x = ax + 12 + (i % 2) * (col_w + 12)
        row_y = ay + 28 + (i // 2) * 30
        label = f"{tag} \u2014 "
        label_w = draw.textlength(label, font=sans_bold_sm)
        draw.text((col_x, row_y), label, font=sans_bold_sm, fill=INK)
        first_pass = flow_words(draw, text, sans_small, col_w - label_w)
        draw.text((col_x + label_w, row_y), first_pass[0], font=sans_small,
                  fill=INK)
        leftover = " ".join(first_pass[1:])
        if leftover:
            second_pass = flow_words(draw, leftover, sans_small, col_w)
            draw.text((col_x, row_y + 13), second_pass[0], font=sans_small,
                      fill=INK)

    # --- sources ---------------------------------------------------------
    draw.text(((SIDE - draw.textlength(SOURCES_LINE, font=sans_small)) / 2,
               990), SOURCES_LINE, font=sans_small, fill=GREY)

    return canvas


def main() -> None:
    page = paint_page()
    page.save(OUT_PATH, format="PNG", optimize=True)
    print(f"wrote {OUT_PATH} ({page.size[0]}x{page.size[1]})")


if __name__ == "__main__":
    main()

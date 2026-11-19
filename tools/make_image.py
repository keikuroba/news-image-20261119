#!/usr/bin/env python3
"""Build the 19 November 2026 front page (1024x1024 PNG).

Build-time only: the grader never runs this file. It draws the artwork
that main.py later copies, from the stories first reported on Thursday
19 November 2026. Everything is fixed — text, geometry, palette — so the
bytes are the same on every run. Pillow is the only dependency.
"""

import os

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.normpath(os.path.join(ROOT, "..", "assets", "entry.png"))

PAGE_W, PAGE_H = 1024, 1024
MARGIN = 40
GUTTER = 40

PAPER = (246, 241, 231)
INK = (22, 22, 22)
BODY_INK = (52, 52, 52)
NAVY = (18, 34, 62)
SCARLET = (178, 34, 26)
FAINT = (90, 86, 78)
HAIRLINE = (196, 188, 172)
TICKER_GOLD = (255, 214, 90)
TICKER_TEXT = (238, 238, 238)
WHITE = (255, 255, 255)

FONT_DIRS = ("/usr/share/fonts/truetype/dejavu", "/usr/share/fonts/dejavu")


def load_font(points, heavy=False):
    """A DejaVu face at the given size, or Pillow's built-in fallback."""
    wanted = "DejaVuSans-Bold.ttf" if heavy else "DejaVuSans.ttf"
    for folder in FONT_DIRS:
        candidate = os.path.join(folder, wanted)
        if os.path.isfile(candidate):
            return ImageFont.truetype(candidate, points)
    return ImageFont.load_default()


def fit_lines(canvas, text, face, max_width):
    """Split text into lines that fit max_width pixels (greedy)."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = (current + " " + word).strip()
        if not current or canvas.textlength(trial, font=face) <= max_width:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_rule(canvas, x0, x1, y, weight=2, colour=None):
    canvas.line([(x0, y), (x1, y)], fill=colour or HAIRLINE, width=weight)


class Story:
    """One news block: kicker, headline, body, and its drawn height."""

    def __init__(self, kicker, headline, body):
        self.kicker = kicker
        self.headline = headline
        self.body = body

    def paint(self, canvas, x, y, width, head_points=29, body_points=20):
        kicker_face = load_font(24, heavy=True)
        canvas.text((x, y), self.kicker, font=kicker_face, fill=SCARLET)
        y += 34
        head_face = load_font(head_points, heavy=True)
        for line in fit_lines(canvas, self.headline, head_face, width):
            canvas.text((x, y), line, font=head_face, fill=INK)
            y += head_points + 6
        y += 4
        body_face = load_font(body_points)
        for line in fit_lines(canvas, self.body, body_face, width):
            canvas.text((x, y), line, font=body_face, fill=BODY_INK)
            y += body_points + 7
        return y


def masthead(canvas):
    """Title bar, date badge and double rule."""
    canvas.rectangle([0, 0, PAGE_W, 8], fill=NAVY)
    title_face = load_font(50, heavy=True)
    canvas.text((MARGIN, 34), "THE WORLD IN ONE IMAGE",
                font=title_face, fill=NAVY)
    badge_r = 46
    bx0 = PAGE_W - MARGIN - 2 * badge_r
    canvas.ellipse([bx0, 26, bx0 + 2 * badge_r, 26 + 2 * badge_r],
                   fill=SCARLET)
    day_face = load_font(46, heavy=True)
    canvas.text((bx0 + 26, 44), "19", font=day_face, fill=WHITE)
    date_face = load_font(30, heavy=True)
    canvas.text((MARGIN, 100), "THURSDAY  \u00b7  19 NOVEMBER 2026",
                font=date_face, fill=SCARLET)
    draw_rule(canvas, MARGIN, PAGE_W - MARGIN, 146, weight=4, colour=NAVY)
    draw_rule(canvas, MARGIN, PAGE_W - MARGIN, 154, weight=1, colour=NAVY)


def ticker(canvas, y, items):
    """Dark band with the rest of the day's news, two lines at most."""
    band_h = 100
    canvas.rectangle([0, y, PAGE_W, y + band_h], fill=NAVY)
    label_face = load_font(24, heavy=True)
    canvas.text((MARGIN, y + 12), "ALSO TODAY",
                font=label_face, fill=TICKER_GOLD)
    joined = "  \u00b7  ".join(items)
    text_face = load_font(21)
    ty = y + 46
    lines = fit_lines(canvas, joined, text_face, PAGE_W - 2 * MARGIN)
    assert len(lines) <= 2, "ticker needs more than two lines"
    for line in lines:
        canvas.text((MARGIN, ty), line, font=text_face, fill=TICKER_TEXT)
        ty += 26
    return y + band_h


def build():
    sheet = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    canvas = ImageDraw.Draw(sheet)
    content_w = PAGE_W - 2 * MARGIN
    half_w = (content_w - GUTTER) // 2

    masthead(canvas)

    lead = Story(
        "SUMMIT IN SHENZHEN",
        "Trump, Xi and Putin shake hands \u2014 the first trilateral "
        "summit of the three leaders",
        "Xi Jinping hugged Donald Trump on the tarmac as he arrived in "
        "Shenzhen for the APEC summit. The three presidents hold their "
        "trilateral meeting on Thursday.")
    y = lead.paint(canvas, MARGIN, 176, content_w,
                   head_points=36, body_points=22)
    draw_rule(canvas, MARGIN, PAGE_W - MARGIN, y + 10)
    y += 22

    gulf = Story(
        "GULF ESCALATION",
        "U.S. and Iran trade fire again as Tehran widens its Gulf attacks",
        "U.S. jets hit a missile site on Qeshm Island after Iran struck a "
        "U.S. radar base in Bahrain; Iran then fired on U.S. bases in "
        "Kuwait and Bahrain again.")
    bridge = Story(
        "CRIMEAN BRIDGE HIT AGAIN",
        "Attack closes the Crimea link; damage is being assessed",
        "Russian officials say the bridge was attacked again and traffic "
        "was shut while engineers check the damage.")
    left_end = gulf.paint(canvas, MARGIN, y, half_w)
    right_end = bridge.paint(canvas, MARGIN + half_w + GUTTER, y, half_w)
    y = max(left_end, right_end)
    draw_rule(canvas, MARGIN, PAGE_W - MARGIN, y + 10)
    y += 22

    speaker = Story(
        "FIRST BLACK SPEAKER",
        "Democrats nominate Hakeem Jeffries to lead the House",
        "Jeffries is set to become the first African-American Speaker of "
        "the U.S. House of Representatives.")
    ipo = Story(
        "ANTHROPIC\u2019S RECORD IPO",
        "$81.3bn raised \u2014 the biggest IPO of all time",
        "The Claude maker raised $81.3bn in the largest flotation ever, "
        "poised for a stock-market debut worth over $1.4tn.")
    left_end = speaker.paint(canvas, MARGIN, y, half_w)
    right_end = ipo.paint(canvas, MARGIN + half_w + GUTTER, y, half_w)
    y = max(left_end, right_end)

    band_end = ticker(canvas, y + 16, [
        "ICJ Rohingya verdict",
        "Nvidia halts H-chips to China",
        "Cyclone Akvan nears India",
        "Gaza ground operation",
        "Voyager 1 one light-day out",
    ])

    foot_face = load_font(19)
    canvas.text((MARGIN, band_end + 10),
                "Every story first reported on 19 November 2026  \u00b7  "
                "made for make.fun", font=foot_face, fill=FAINT)
    assert band_end + 10 + 19 <= PAGE_H, "footer runs off the page"

    sheet.save(TARGET, format="PNG", optimize=True)
    size = os.path.getsize(TARGET)
    assert size <= 1024 * 1024, "image over 1 MiB: %d bytes" % size
    print("wrote %s (%d bytes)" % (TARGET, size))


if __name__ == "__main__":
    build()

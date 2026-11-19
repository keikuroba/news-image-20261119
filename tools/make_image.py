#!/usr/bin/env python3
"""Draw the 19 November 2026 world-news infographic (1024x1024 PNG).

Run once, locally, at build time. The entry program (main.py) only copies
the finished image; this script is never run by the grader. Output is
deterministic: fixed text, fixed layout, fixed colours, no clock, no
network, no randomness. Pillow is the only dependency.

Layout (newspaper front page, 1024x1024):
  masthead  -> THE WORLD IN ONE IMAGE / THURSDAY 19 NOVEMBER 2026
  lead      -> Trump-Xi-Putin summit in Shenzhen (full width)
  row 2     -> Gulf escalation | Crimean Bridge (two columns)
  row 3     -> Jeffries Speaker | Anthropic IPO (two columns)
  ticker    -> the rest of the day, one dark band
"""

import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "assets", "entry.png")

W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (22, 22, 22)
NAVY = (18, 34, 62)
RED = (178, 34, 26)
MUTED = (90, 86, 78)
RULE = (18, 34, 62)
LIGHT_LINE = (196, 188, 172)


def find_font(bold=False):
    """DejaVu ships with most Linux Pillow installs; fall back to default."""
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    for base in ("/usr/share/fonts/truetype/dejavu",
                 "/usr/share/fonts/dejavu"):
        path = os.path.join(base, name)
        if os.path.exists(path):
            return path
    return None


def font(size, bold=False):
    path = find_font(bold)
    if path:
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def wrap(draw, text, fnt, width):
    """Greedy word wrap by pixel width; returns list of lines."""
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_story(draw, x, y, w, label, headline, body, head_size=34,
               body_size=23, label_size=24):
    """Draw one story block; returns the y just below it."""
    lab_f = font(label_size, bold=True)
    draw.text((x, y), label, font=lab_f, fill=RED)
    y += label_size + 10
    head_f = font(head_size, bold=True)
    for line in wrap(draw, headline, head_f, w):
        draw.text((x, y), line, font=head_f, fill=INK)
        y += head_size + 6
    y += 4
    body_f = font(body_size)
    for line in wrap(draw, body, body_f, w):
        draw.text((x, y), line, font=body_f, fill=(52, 52, 52))
        y += body_size + 7
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 40  # side margin

    # ---- masthead ----
    d.rectangle([0, 0, W, 8], fill=NAVY)
    title_f = font(50, bold=True)
    d.text((mx, 34), "THE WORLD IN ONE IMAGE", font=title_f, fill=NAVY)
    # date badge: red disc with the day number
    d.ellipse([W - mx - 92, 26, W - mx, 118], fill=RED)
    num_f = font(46, bold=True)
    d.text((W - mx - 66, 44), "19", font=num_f, fill=(255, 255, 255))
    date_f = font(30, bold=True)
    d.text((mx, 100), "THURSDAY  \u00b7  19 NOVEMBER 2026",
           font=date_f, fill=RED)
    d.line([(mx, 146), (W - mx, 146)], fill=RULE, width=4)
    d.line([(mx, 154), (W - mx, 154)], fill=RULE, width=1)

    # ---- lead story: Trump-Xi-Putin summit ----
    y = draw_story(
        d, mx, 176, W - 2 * mx,
        "SUMMIT IN SHENZHEN",
        "Trump, Xi and Putin shake hands \u2014 the first trilateral "
        "summit of the three leaders",
        "Xi Jinping hugged Donald Trump on the tarmac as he arrived in "
        "Shenzhen for the APEC summit. The three presidents hold their "
        "trilateral meeting on Thursday.",
        head_size=36, body_size=22)
    d.line([(mx, y + 10), (W - mx, y + 10)], fill=LIGHT_LINE, width=2)
    y += 22

    # ---- row 2: two columns ----
    col_w = (W - 2 * mx - 40) // 2
    left_y = draw_story(
        d, mx, y, col_w,
        "GULF ESCALATION",
        "U.S. and Iran trade fire again as Tehran widens its Gulf attacks",
        "U.S. jets hit a missile site on Qeshm Island after Iran struck a "
        "U.S. radar base in Bahrain; Iran then fired on U.S. bases in "
        "Kuwait and Bahrain again.",
        head_size=29, body_size=20)
    right_y = draw_story(
        d, mx + col_w + 40, y, col_w,
        "CRIMEAN BRIDGE HIT AGAIN",
        "Attack closes the Crimea link; damage is being assessed",
        "Russian officials say the bridge was attacked again and traffic "
        "was shut while engineers check the damage.",
        head_size=29, body_size=20)
    y = max(left_y, right_y)
    d.line([(mx, y + 10), (W - mx, y + 10)], fill=LIGHT_LINE, width=2)
    y += 22

    # ---- row 3: two columns ----
    left_y = draw_story(
        d, mx, y, col_w,
        "FIRST BLACK SPEAKER",
        "Democrats nominate Hakeem Jeffries to lead the House",
        "Jeffries is set to become the first African-American Speaker of "
        "the U.S. House of Representatives.",
        head_size=29, body_size=20)
    right_y = draw_story(
        d, mx + col_w + 40, y, col_w,
        "ANTHROPIC\u2019S RECORD IPO",
        "$81.3bn raised \u2014 the biggest IPO of all time",
        "The Claude maker raised $81.3bn in the largest flotation ever, "
        "poised for a stock-market debut worth over $1.4tn.",
        head_size=29, body_size=20)
    y = max(left_y, right_y)

    # ---- ticker: the rest of the day (band placed after row 3) ----
    band_y = y + 16
    band_h = 100
    d.rectangle([0, band_y, W, band_y + band_h], fill=NAVY)
    tick_f = font(24, bold=True)
    d.text((mx, band_y + 12), "ALSO TODAY", font=tick_f, fill=(255, 214, 90))
    tick = ("ICJ Rohingya verdict  \u00b7  "
            "Nvidia halts H-chips to China  \u00b7  "
            "Cyclone Akvan nears India  \u00b7  "
            "Gaza ground operation  \u00b7  "
            "Voyager 1 one light-day out")
    tick_f2 = font(21)
    ty = band_y + 46
    for line in wrap(d, tick, tick_f2, W - 2 * mx):
        d.text((mx, ty), line, font=tick_f2, fill=(238, 238, 238))
        ty += 26
    assert ty - 26 + 21 <= band_y + band_h, "ticker overflows its band"

    # ---- footer ----
    foot_f = font(19)
    foot_y = band_y + band_h + 10
    d.text((mx, foot_y), "Every story first reported on 19 November 2026  \u00b7  "
           "made for make.fun", font=foot_f, fill=MUTED)
    assert foot_y + 19 <= H, "footer overflows the page"

    img.save(OUT, format="PNG", optimize=True)
    size = os.path.getsize(OUT)
    assert size <= 1048576, "image over 1 MiB: %d" % size
    print("wrote", OUT, size, "bytes")


if __name__ == "__main__":
    main()

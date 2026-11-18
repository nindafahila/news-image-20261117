#!/usr/bin/env python3
"""Draw entry.png: a one-page newspaper front page summing up the world news
of Tuesday 17 November 2026. Pure Pillow, no network, fully deterministic:
same input, same bytes every run. Regenerates entry.png beside this file.

Stories (all happened / first reported 17 Nov 2026, per AP, Reuters,
Al Jazeera, NYT, The Guardian):
  1. Third US carrier (USS Theodore Roosevelt) reaches the Middle East as
     tankers are hit by mines near the Strait of Hormuz.
  2. Russian missiles hit two Kyiv bridges; Ukraine strikes the Crimean
     (Kerch) Bridge again, a day after the first strike.
  3. Trump heads to Asia for APEC in Shenzhen; China confirms the first
     Xi-Trump-Putin three-way meeting, set for Thursday 19 Nov.
  4. Five EU states announce a joint migrant return hub in Rwanda.
  5. Pentagon fails its financial audit for the 9th year running.
  6. JPMorgan tech glitch disrupts online banking and Zelle.
  7. WHO validates Eritrea's elimination of trachoma.
"""

import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (18, 24, 32)
NAVY = (16, 35, 63)
RED = (178, 34, 34)
GOLD = (212, 175, 55)
GREY = (90, 90, 88)
BLUE = (38, 84, 124)
SEA = (46, 111, 152)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, color, max_w, leading):
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def rule(draw, x0, x1, y, color=INK, width=2):
    draw.line([(x0, y), (x1, y)], fill=color, width=width)


def burst(draw, cx, cy, r, color):
    """Starburst explosion: 12 spikes + filled core."""
    pts = []
    for i in range(24):
        ang = math.pi * i / 12
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=color)
    draw.ellipse([cx - r * 0.35, cy - r * 0.35, cx + r * 0.35, cy + r * 0.35],
                 fill=(255, 214, 90))


def draw_carrier(draw, x, y, w, h):
    """Aircraft carrier on the sea with a mine blast behind it."""
    draw.rectangle([x, y, x + w, y + h], fill=(214, 232, 240))
    # sky sun
    draw.ellipse([x + w - 52, y + 8, x + w - 16, y + 44], fill=(255, 205, 80))
    # sea
    draw.rectangle([x, y + h * 0.62, x + w, y + h], fill=SEA)
    for wx in range(0, w, 46):
        draw.arc([x + wx, y + h * 0.66, x + wx + 40, y + h * 0.86],
                 200, 340, fill=(255, 255, 255), width=3)
    # carrier hull + deck + island
    hx, hy = x + 30, y + h * 0.52
    draw.polygon([(hx, hy), (hx + w - 70, hy), (hx + w - 92, hy + 26),
                  (hx + 12, hy + 26)], fill=(52, 62, 72))
    draw.rectangle([hx + 8, hy - 8, hx + w - 78, hy + 2], fill=(70, 80, 92))
    draw.rectangle([hx + w - 150, hy - 34, hx + w - 118, hy - 8],
                   fill=(70, 80, 92))
    draw.line([(hx + w - 134, hy - 34), (hx + w - 134, hy - 52)],
              fill=(70, 80, 92), width=4)
    # mine blast at the stern
    burst(draw, x + 40, y + h * 0.35, 20, (232, 90, 30))
    draw.text((x + 8, y + h - 24), "USS THEODORE ROOSEVELT  •  STRAIT OF HORMUZ",
              font=font(SANS_B, 13), fill=(255, 255, 255))


def draw_bridge(draw, x, y, w, h):
    """A river bridge hit by a strike: towers, cables, blast."""
    draw.rectangle([x, y, x + w, y + h], fill=(226, 232, 238))
    draw.rectangle([x, y + h * 0.72, x + w, y + h], fill=(120, 150, 180))
    # deck
    draw.rectangle([x + 6, y + h * 0.58, x + w - 6, y + h * 0.64],
                   fill=(70, 76, 84))
    # towers + cables
    for tx in (x + w * 0.28, x + w * 0.68):
        draw.rectangle([tx - 5, y + 14, tx + 5, y + h * 0.60],
                       fill=(90, 96, 104))
        draw.line([(tx, y + 16), (x + 10, y + h * 0.58)], fill=(120, 126, 134),
                  width=2)
        draw.line([(tx, y + 16), (x + w - 10, y + h * 0.58)],
                  fill=(120, 126, 134), width=2)
    # collapsed span + blast
    draw.line([(x + w * 0.44, y + h * 0.60), (x + w * 0.50, y + h * 0.72)],
              fill=(70, 76, 84), width=5)
    burst(draw, x + w * 0.78, y + h * 0.35, 18, (232, 90, 30))
    draw.text((x + 8, y + h - 24), "KYIV  •  CRIMEA BRIDGE",
              font=font(SANS_B, 13), fill=(255, 255, 255))


def draw_globe(draw, cx, cy, r):
    """Simple globe with three small flags beneath it."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(178, 214, 235),
                 outline=BLUE, width=3)
    for k in range(1, 4):
        yy = cy - r + k * (2 * r / 4)
        half = math.sqrt(max(r * r - (yy - cy) ** 2, 0))
        draw.line([(cx - half, yy), (cx + half, yy)], fill=BLUE, width=2)
    draw.ellipse([cx - r * 0.45, cy - r * 0.55, cx - r * 0.05, cy - r * 0.15],
                 fill=(96, 160, 90))
    draw.ellipse([cx + r * 0.05, cy + r * 0.10, cx + r * 0.50, cy + r * 0.55],
                 fill=(96, 160, 90))
    draw.arc([cx - r * 0.55, cy - r, cx + r * 0.55, cy + r], 300, 60,
             fill=BLUE, width=2)
    draw.arc([cx - r * 0.55, cy - r, cx + r * 0.55, cy + r], 120, 240,
             fill=BLUE, width=2)
    # three flags: US, China, Russia
    flags = [
        ([(205, 40, 40), (255, 255, 255), (205, 40, 40), (255, 255, 255)],
         (16, 35, 63)),
        ([(222, 41, 16)], None),
        ([(255, 255, 255), (0, 57, 166), (213, 0, 50)], None),
    ]
    fx = cx - 78
    for stripes, canton in flags:
        fy = cy + r + 14
        fw, fh = 44, 28
        for i, col in enumerate(stripes):
            draw.rectangle([fx, fy + i * fh // len(stripes),
                            fx + fw, fy + (i + 1) * fh // len(stripes)],
                           fill=col)
        draw.rectangle([fx, fy, fx + fw, fy + fh], outline=INK, width=2)
        if canton:
            draw.rectangle([fx, fy, fx + 18, fy + 14], fill=canton)
        else:
            # one small star on the plain red flag
            draw.ellipse([fx + 6, fy + 5, fx + 14, fy + 13], fill=(255, 222, 0))
        fx += 56


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    d.rectangle([0, 0, W, 116], fill=NAVY)
    d.text((W // 2, 14), "THE WORLD IN ONE PICTURE",
           font=font(SERIF, 52), fill=(255, 255, 255), anchor="ma")
    d.text((W // 2, 76), "T U E S D A Y  •  1 7  N O V E M B E R  2 0 2 6",
           font=font(SANS_B, 26), fill=GOLD, anchor="ma")
    rule(d, 0, W, 118, RED, 6)

    # ---- Dateline strip ----
    d.text((36, 134), "WORLD NEWS  —  THE DAY IN ONE IMAGE",
           font=font(SANS_B, 18), fill=RED)
    d.text((988, 134), "No. 321  •  ONE PAGE, THE WHOLE DAY",
           font=font(SANS_B, 16), fill=GREY, anchor="ra")

    # ---- Lead story (left), fixed box 168-520 ----
    lx, lw = 36, 584
    d.text((lx, 168), "MIDDLE EAST  •  STRAIT OF HORMUZ",
           font=font(SANS_B, 20), fill=RED)
    para(d, lx, 196,
         "THIRD U.S. CARRIER ARRIVES AS TANKERS HIT BY MINES",
         font(SERIF, 38), INK, lw, 44)
    para(d, lx, 332,
         "The USS Theodore Roosevelt joins two other American carriers "
         "in the region — the first three-carrier concentration since "
         "April — as tankers strike mines near Hormuz and catch fire.",
         font(SANS, 19), INK, lw, 25)
    draw_carrier(d, lx, 436, lw, 80)

    # ---- Ukraine (right), fixed box 168-520 ----
    rx, rw = 648, 340
    d.text((rx, 168), "UKRAINE  •  WAR", font=font(SANS_B, 20), fill=RED)
    para(d, rx, 196,
         "KYIV BRIDGES HIT; UKRAINE STRIKES CRIMEA BRIDGE AGAIN",
         font(SERIF, 30), INK, rw, 36)
    para(d, rx, 344,
         "Russian missiles hit two bridges over the Dnipro, cutting "
         "heat, water and power. Ukraine hits the Kerch Bridge for a "
         "second day running.",
         font(SANS, 18), INK, rw, 24)
    draw_bridge(d, rx, 456, rw, 60)

    # ---- Divider + APEC band, fixed box 532-712 ----
    rule(d, 36, 988, 528, INK, 2)
    d.text((36, 542), "DIPLOMACY  •  APEC, SHENZHEN",
           font=font(SANS_B, 20), fill=RED)
    para(d, 36, 570,
         "TRUMP HEADS TO ASIA FOR TALKS WITH XI AND PUTIN",
         font(SERIF, 32), INK, 620, 38)
    para(d, 36, 656,
         "China confirms the first three-way Xi–Trump–Putin meeting, "
         "set for Thursday in Shenzhen on the APEC sidelines.",
         font(SANS, 19), INK, 620, 25)
    draw_globe(d, 830, 606, 50)

    # ---- Bottom grid: four more stories ----
    rule(d, 36, 988, 716, INK, 2)
    cols = [
        ("EUROPE", "FIVE EU STATES PLAN RWANDA RETURN HUB",
         "Germany, Denmark, Austria, Greece and the Netherlands will send "
         "rejected asylum seekers to a joint facility in Rwanda."),
        ("WASHINGTON", "PENTAGON FAILS AUDIT, 9TH YEAR RUNNING",
         "Auditors again cannot verify books covering more than $4.8 "
         "trillion in assets — a disclaimer of opinion."),
        ("MARKETS", "JPMORGAN GLITCH HITS ZELLE & ONLINE BANKING",
         "A technical fault disrupts accounts at several major U.S. banks "
         "and the money-transfer service Zelle."),
        ("HEALTH", "ERITREA BEATS TRACHOMA, WHO CONFIRMS",
         "The blinding eye disease is eliminated in Eritrea. Also: Japan "
         "protests Russian jets near its airspace."),
    ]
    cw, gap = 224, 16
    for i, (kick, head, body) in enumerate(cols):
        x = 36 + i * (cw + gap)
        y = 732
        d.text((x, y), kick, font=font(SANS_B, 16), fill=RED)
        y = para(d, x, y + 24, head, font(SERIF, 22), INK, cw, 27)
        para(d, x, y + 4, body, font(SANS, 15), INK, cw, 21)
        if i < 3:
            d.line([(x + cw + 8, 732), (x + cw + 8, 948)], fill=(200, 195, 180),
                   width=1)

    # ---- Footer ----
    rule(d, 36, 988, 966, INK, 2)
    d.text((512, 978),
           "Every story happened, or was first reported, on Tuesday 17 November 2026",
           font=font(SANS_B, 16), fill=INK, anchor="ma")
    d.text((512, 1000),
           "Sources: AP  •  Reuters  •  Al Jazeera  •  NYT  •  The Guardian",
           font=font(SANS, 14), fill=GREY, anchor="ma")

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()

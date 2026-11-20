#!/usr/bin/env python3
"""Render the 20 November 2026 world-news front page (1024x1024 PNG).

Stories (all verified against real sources dated 20 Nov 2026):
 1. Cyclone Akvan landfall, India east coast - India Meteorological Dept
    (landfall by noon 20 Nov near Gopalpur; winds 90-100 km/h, gusts 110;
    100,000+ people evacuated to shelters)
 2. Tanker fire after mine strike, Strait of Hormuz - Al Jazeera, 20 Nov
    (Iran's navy says a liquefied gas carrier hit naval mines and caught fire)
 3. Russian strikes damage Austrian and Dutch embassies, Kyiv - Euronews/AFP
    (strikes 19 Nov, reported 20 Nov; staff unharmed; EU to summon envoy)
 4. South Korea's exports pass $1 trillion, first time - Seoul Economic Daily
    (milestone crossed 19 Nov; fourth country after US, Germany, China)
 5. Shenzhen summit nuclear pledge weighed - CNN analysis, 20 Nov
    (joint vow "a nuclear war cannot be won" echoes Reagan-Gorbachev)
 6. Malaysia PM flags air force officers in drug probe - Media Selangor, 20 Nov
    (Anwar Ibrahim: officers incl. pilots suspected; 100+ detained)

Deterministic: fixed text, fixed fonts, no time, no randomness.
Run: python3 render.py  -> writes news.png next to this file.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))

W, H = 1024, 1024
PAPER = (246, 241, 229)
INK = (26, 26, 26)
RED = (163, 18, 18)
BLUE = (38, 68, 104)
GREY = (96, 96, 92)
RULE = (26, 26, 26)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
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


def draw_spiral(draw, cx, cy, turns=2.6, color=BLUE):
    """A simple cyclone swirl: an Archimedean spiral plus rain streaks."""
    pts = []
    steps = 220
    for i in range(steps + 1):
        t = i / steps
        ang = t * turns * 2 * math.pi
        r = 8 + t * 104
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang) * 0.92))
    for a, b in zip(pts, pts[1:]):
        draw.line([a, b], fill=color, width=4)
    # rain streaks around the swirl, kept clear of the spiral edge
    for k in range(10):
        ang = k * math.pi / 5 + 0.35
        x0 = cx + 132 * math.cos(ang)
        y0 = cy + 122 * math.sin(ang)
        draw.line([(x0, y0), (x0 - 8, y0 + 26)], fill=(120, 140, 165), width=3)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # outer frame
    d.rectangle([10, 10, W - 11, H - 11], outline=INK, width=3)
    d.rectangle([18, 18, W - 19, H - 19], outline=INK, width=1)

    # ---- masthead ----
    f_mast = font(SERIF_B, 62)
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=f_mast)
    d.text(((W - tw) / 2, 30), title, font=f_mast, fill=INK)
    d.line([(40, 108), (W - 40, 108)], fill=INK, width=2)
    f_date = font(SANS_B, 25)
    date = "F R I D A Y   2 0   N O V E M B E R   2 0 2 6"
    dw = d.textlength(date, font=f_date)
    d.text(((W - dw) / 2, 120), date, font=f_date, fill=RED)
    d.line([(40, 158), (W - 40, 158)], fill=INK, width=3)
    d.line([(40, 164), (W - 40, 164)], fill=INK, width=1)

    # ---- lead story ----
    f_kick = font(SANS_B, 19)
    d.text((40, 182), "LEAD  —  INDIA", font=f_kick, fill=RED)
    f_lead = font(SERIF_B, 46)
    lead_head = ["Cyclone Akvan slams", "into India's east coast"]
    y = 208
    for line in lead_head:
        d.text((40, y), line, font=f_lead, fill=INK)
        y += 54
    f_body = font(SANS, 20)
    lead_sum = ("The severe storm is due ashore near Gopalpur around noon, "
                "with winds of 90–100 km/h. More than 100,000 people have "
                "been moved to shelters as Odisha and Andhra Pradesh brace "
                "for heavy rain.")
    y = 322
    for line in wrap(d, lead_sum, f_body, 620):
        d.text((40, y), line, font=f_body, fill=INK)
        y += 27
    f_fact = font(SANS_B, 18)
    d.text((40, y + 8), "Winds 90–100 km/h, gusts to 110  •  Red alert, 11 districts",
           font=f_fact, fill=BLUE)

    # lead graphic: cyclone swirl panel
    d.rectangle([700, 182, 984, 452], outline=INK, width=2)
    d.rectangle([706, 188, 978, 446], outline=GREY, width=1)
    draw_spiral(d, 842, 300)
    f_cap = font(SANS_B, 16)
    cap = "AKVAN — BAY OF BENGAL"
    cw = d.textlength(cap, font=f_cap)
    d.text((842 - cw / 2, 412), cap, font=f_cap, fill=INK)

    # ---- divider ----
    d.line([(40, 478), (W - 40, 478)], fill=INK, width=2)

    # ---- five more stories ----
    stories = [
        ("HORMUZ", "Tanker catches fire after hitting a mine",
         "Iran's navy says a tanker hit naval mines in the Strait of "
         "Hormuz and caught fire. The claims are unverified; shipping in "
         "the vital oil waterway stays on edge."),
        ("UKRAINE", "Russian strikes damage two EU embassies in Kyiv",
         "Blasts hit the Austrian and Dutch missions; staff escaped "
         "unharmed and one person was killed in the wider attack. The EU "
         "said it will summon Russia's ambassador."),
        ("SOUTH KOREA", "Exports pass $1 trillion for the first time",
         "Driven by an AI chip boom, Korea becomes only the fourth "
         "country to reach the mark, after the US, Germany and China."),
        ("SUMMIT", "A day after Shenzhen, the nuclear pledge is weighed",
         "Trump, Xi and Putin's joint vow that \u201ca nuclear war cannot "
         "be won\u201d echoes the Reagan–Gorbachev principle, analysts say."),
        ("MALAYSIA", "PM flags air force officers in drug-smuggling probe",
         "Anwar Ibrahim says officers, including pilots, are suspected in "
         "a major case. More than 100 people have been detained in a wider "
         "crackdown on trafficking and illicit finance."),
    ]
    f_skick = font(SANS_B, 16)
    f_shead = font(SERIF_B, 24)
    f_ssum = font(SANS, 17)
    col_x = [40, 532]
    col_w = 452
    row_y = [498, 668, 838]
    for i, (kick, head, summ) in enumerate(stories):
        if i < 4:
            x = col_x[i % 2]
            y = row_y[i // 2]
        else:
            x = 40
            y = row_y[2]
            col_w = 944
        d.text((x, y), kick, font=f_skick, fill=RED)
        y += 24
        for line in wrap(d, head, f_shead, col_w)[:2]:
            d.text((x, y), line, font=f_shead, fill=INK)
            y += 30
        for line in wrap(d, summ, f_ssum, col_w)[:3]:
            d.text((x, y), line, font=f_ssum, fill=INK)
            y += 23
        if i < 4:
            col_w = 452

    # ---- footer ----
    d.line([(40, 962), (W - 40, 962)], fill=INK, width=1)
    f_foot = font(SANS, 13)
    foot = ("Sources: India Meteorological Dept · Al Jazeera · Euronews · Seoul Economic Daily · "
            "CNN · Media Selangor  —  20 November 2026")
    fw = d.textlength(foot, font=f_foot)
    d.text(((W - fw) / 2, 972), foot, font=f_foot, fill=GREY)

    out = os.path.join(HERE, "news.png")
    img.save(out, format="PNG")
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""og.png 1200x630 — Mylar Bar — "mylar & streamers" poster.
Midnight plum, mylar pink, chrome silver, electric blue. Balloons flank the centered
stack OUTSIDE the text column; the script asserts no balloon/string box overlaps any
text box before saving (the buoy-collision lesson, salty-jax 2026-11-24)."""
from PIL import Image, ImageDraw, ImageFont
import os, sys

W, H = 1200, 630
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public", "og.png")

INK = (20, 16, 33); INK2 = (29, 23, 49); PINK = (255, 77, 143); PINK_HI = (255, 122, 176)
BLUE = (127, 160, 255); SILVER = (207, 211, 230); CREAM = (242, 238, 252); DIM = (141, 134, 171)

def font(paths, size):
    bases = ["/System/Library/Fonts/Supplemental/", "/System/Library/Fonts/"]
    for b in bases:
        for n in paths:
            p = b + n
            if os.path.exists(p):
                try: return ImageFont.truetype(p, size)
                except Exception: pass
    return ImageFont.load_default()

serif = lambda s: font(["Iowan Old Style.ttc", "Palatino.ttc", "Georgia.ttf", "Times New Roman.ttf"], s)
sans = lambda s: font(["Futura.ttc", "HelveticaNeue.ttc", "HelveticaNeue.ttc", "Arial.ttf"], s)

img = Image.new("RGB", (W, H), INK)
d = ImageDraw.Draw(img)

# darker band lower third — the room past midnight
d.rectangle([0, 470, W, H], fill=INK2)
# pink streamer rules top and bottom
d.rectangle([0, 0, W, 6], fill=PINK)
d.rectangle([0, H-6, W, H], fill=PINK)

boxes = []   # (kind, x0, y0, x1, y1)

def text_h(f, probe="Ag"):
    bb = d.textbbox((0,0), probe, font=f)
    return bb[3]-bb[1]

def center(text, f, y, fill, tracking=0):
    if tracking:
        widths = [d.textbbox((0,0), ch, font=f)[2]-d.textbbox((0,0), ch, font=f)[0] for ch in text]
        tw = sum(widths) + tracking*(len(text)-1)
        x0 = (W-tw)/2
        x = x0
        for ch,w in zip(text,widths):
            bb = d.textbbox((0,0), ch, font=f)
            d.text((x - bb[0], y), ch, font=f, fill=fill)
            x += w + tracking
    else:
        bb = d.textbbox((0,0), text, font=f)
        tw = bb[2]-bb[0]
        x0 = (W-tw)/2
        d.text((x0 - bb[0], y), text, font=f, fill=fill)
    boxes.append(('text', x0, y, x0+tw, y + text_h(f)))
    return (tw, x0)

def balloon(cx, cy, rx, ry, color, hi):
    d.ellipse([cx-rx, cy-ry, cx+rx, cy+ry], fill=color)
    d.ellipse([cx-rx*0.55, cy-ry*0.55, cx-rx*0.15, cy-ry*0.1], fill=hi)   # highlight
    d.polygon([(cx-7, cy+ry), (cx+7, cy+ry), (cx, cy+ry+12)], fill=color) # knot
    sx = cx; sy = cy+ry+12
    d.line([(sx, sy), (sx, sy+70)], fill=SILVER, width=2)
    boxes.append(('balloon', cx-rx, cy-ry, cx+rx, sy+70))

# balloons — clusters flanking the center column, in the header zone
balloon(140, 100, 55, 66, PINK, PINK_HI)      # left big pink
balloon(248, 62, 42, 52, BLUE, (180, 205, 255))  # left small blue
balloon(1060, 100, 55, 66, PINK, PINK_HI)     # right big pink
balloon(952, 62, 42, 52, SILVER, (245, 247, 252)) # right small silver

# kicker
center("SOUTH PHILLY  ·  NINTH & MORRIS", sans(24), 196, PINK_HI, tracking=6)
# brand
center("MYLAR BAR", serif(120), 244, CREAM)
# double streamer rule
d.rectangle([W/2-140, 386, W/2+140, 389], fill=PINK)
d.rectangle([W/2-140, 393, W/2+140, 396], fill=PINK)
# line
center("Martinis. Punches. Late-night plates.", serif(46), 410, CREAM)
center("Open every day \u2014 5 pm to 2 am.", serif(46), 470, PINK)
# bottom strips on the midnight band
center("The old Dino\u2019s Party Center building \u2014 named for balloon film", sans(23), 522, SILVER)
center("1638 S. Ninth St \u00b7 Philadelphia, PA 19148", sans(21), 562, DIM)

# ---- overlap assertions: balloons/strings vs text ----
def rects_overlap(a, b):
    return not (a[3] <= b[1] or b[3] <= a[1] or a[2] <= b[0] or b[2] <= a[0])

baloons = [b[1:] for b in boxes if b[0] == 'balloon']
texts = [b[1:] for b in boxes if b[0] == 'text']
clash = []
for bl in baloons:
    for tx in texts:
        if rects_overlap(bl, tx):
            clash.append((bl[1:], tx[1:]))
if clash:
    print("OVERLAP FAIL:", clash)
    sys.exit(1)

img.save(OUT, "PNG", optimize=True)
print("wrote", OUT, os.path.getsize(OUT), "bytes; overlap check PASS")

#!/usr/bin/env python3
"""Generate VibeLeading PWA icons, apple-touch icon, and OG image.

Pure-python rasterizer (no external deps) that mirrors assets/icons design
from /favicon.svg: dark (rounded) canvas + cyan->pink gradient mark.

Usage: python3 scripts/gen_icons.py
"""

import struct
import zlib
import math
import os

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "assets", "icons")

PATH = [(10, 46), (28, 18), (38, 30), (50, 14), (56, 32)]
CIRCLE = (47, 42, 4.5)
STROKE = 5.0

BG = (0x05, 0x06, 0x0A)
CYAN = (0x00, 0xD4, 0xFF)
PINK = (0xFF, 0x2D, 0x95)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def seg_lengths():
    lens = []
    for i in range(len(PATH) - 1):
        x1, y1 = PATH[i]
        x2, y2 = PATH[i + 1]
        lens.append(math.hypot(x2 - x1, y2 - y1))
    return lens


SEG_LENS = seg_lengths()
SEG_START = [sum(SEG_LENS[:i]) for i in range(len(SEG_LENS))]
TOTAL_LEN = sum(SEG_LENS)


def arc_color(t):
    return lerp(CYAN, PINK, t)


def render(w, h, out, rounded=True, pad_scale=1.0, center_goto=None, bg=None, bg_grad=None):
    """Render the mark. pad_scale scales the design; bg_grad=(c1,c2) for og."""
    buf = bytearray(w * h * 4)
    scale = min(w, h) * 0.9 / 64.0 * pad_scale
    if center_goto:
        cx = (10 + 56) / 2.0 * scale
        cy = (14 + 46) / 2.0 * scale
        ox = center_goto[0] - cx
        oy = center_goto[1] - cy
    else:
        ox = oy = 0.0

    def px(u, v):
        return u * scale + ox, v * scale + oy

    pts = [px(*p) for p in PATH]
    ccx, ccy = px(CIRCLE[0], CIRCLE[1])
    cr = CIRCLE[2] * scale

    half_w = STROKE / 2.0 * scale
    aa = 1.0

    cx_, cy_ = w / 2.0, h / 2.0
    radius = min(w, h) * 0.22 if rounded else 0.0
    half = min(w, h) / 2.0

    for y in range(h):
        row = y * w * 4
        for x in range(w):
            i = row + x * 4

            bgc = BG
            bg_a = 0.0
            if bg_grad:
                t = (x / (w - 1) + y / (h - 1)) / 2.0
                bgc = lerp(bg_grad[0], bg_grad[1], t)
                bg_a = 1.0
            elif rounded:
                d = math.hypot(max(abs(x - cx_) - (half - radius), 0.0),
                               max(abs(y - cy_) - (half - radius), 0.0)) - radius
                bg_a = 1.0 - min(max(d + 0.5, 0.0), 1.0)
            else:
                bg_a = 1.0

            r, g, b = bgc
            a = bg_a

            path_r = path_g = path_b = 0.0
            cov_sum = 0.0

            # path capsules
            for si in range(len(pts) - 1):
                x1, y1 = pts[si]
                x2, y2 = pts[si + 1]
                dx, dy = x2 - x1, y2 - y1
                L2 = dx * dx + dy * dy
                t = 0.0 if L2 == 0 else ((x - x1) * dx + (y - y1) * dy) / L2
                t = 0.0 if t < 0.0 else (1.0 if t > 1.0 else t)
                qx, qy = x1 + t * dx, y1 + t * dy
                dist = math.hypot(x - qx, y - qy)
                if dist <= half_w + aa:
                    cov = min(max(half_w - dist + 0.5, 0.0), 1.0)
                    ta = (SEG_START[si] + t * SEG_LENS[si]) / TOTAL_LEN
                    cr_, cg_, cb_ = arc_color(ta)
                    cov_sum += cov
                    path_r += cr_ * cov
                    path_g += cg_ * cov
                    path_b += cb_ * cov

            # endpoint dot
            dot_dist = math.hypot(x - ccx, y - ccy)
            if dot_dist <= cr + aa:
                cov = min(max(cr - dot_dist + 0.5, 0.0), 1.0)
                tu = (x - ccx + cr) / (2 * cr)
                tv = (y - ccy + cr) / (2 * cr)
                cr_, cg_, cb_ = arc_color(max(0.0, min(1.0, (tu + tv) / 2)))
                cov_sum += cov
                path_r += cr_ * cov
                path_g += cg_ * cov
                path_b += cb_ * cov

            if cov_sum > 0:
                pf = min(cov_sum, 1.0)
                pr_, pg_, pb_ = path_r / cov_sum, path_g / cov_sum, path_b / cov_sum
                pa = a * (1 - pf) + pf
                if pa > 0:
                    r = (r * a * (1 - pf) + pr_ * pf) / pa
                    g = (g * a * (1 - pf) + pg_ * pf) / pa
                    b = (b * a * (1 - pf) + pb_ * pf) / pa
                a = pa

            buf[i] = int(r)
            buf[i + 1] = int(g)
            buf[i + 2] = int(b)
            buf[i + 3] = int(round(a * 255))

    write_png(out, w, h, buf)


def write_png(path, w, h, rgba):
    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    raw = bytearray()
    for y in range(h):
        raw.append(0)
        raw += rgba[y * w * 4:(y + 1) * w * 4]
    data = (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
            + chunk(b"IEND", b""))
    with open(path, "wb") as f:
        f.write(data)


def main():
    os.makedirs(OUT, exist_ok=True)
    render(192, 192, os.path.join(OUT, "icon-192.png"), rounded=True)
    render(512, 512, os.path.join(OUT, "icon-512.png"), rounded=True)
    render(512, 512, os.path.join(OUT, "maskable-512.png"), rounded=False, pad_scale=0.78,
           center_goto=(256.0, 256.0))
    render(180, 180, os.path.join(OUT, "apple-touch-icon.png"), rounded=False)
    render(1200, 630, os.path.join(ROOT, "assets", "og-cover.png"), rounded=False, pad_scale=0.85,
           center_goto=(600.0, 315.0),
           bg_grad=((0x0A, 0x10, 0x1E), (0x05, 0x06, 0x0A)))
    print("icons written to", os.path.abspath(OUT))


if __name__ == "__main__":
    main()
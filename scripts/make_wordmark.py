#!/usr/bin/env python3
"""
make_wordmark.py — renders WORDMARK as ASCII block letters that print
row-by-row, left to right, with a cursor riding the wipe edge.

Two decisions worth knowing:

1. Every character is placed at its own exact x with text-anchor="middle".
   Relying on a monospace advance width breaks the grid on any machine whose
   fallback font has different metrics — and SVG fonts resolve against the
   *viewer's* system, not yours.

2. The wipe is SMIL (<animate fill="freeze">) inside the SVG file. GitHub
   strips <script> and inline CSS from READMEs but renders SVG referenced by
   <img> and plays its animations — so all motion has to live in here.

Static art. Regenerate only when the wordmark or tagline changes.
    python scripts/make_wordmark.py           # animated (this is what you commit)
    STATIC=1 python scripts/make_wordmark.py  # frozen final frame, for previewing
"""
import os
from config import (WORDMARK, TAGLINE, USERNAME, BONE, MUTED,
                    ULTRA, ULTRA_LT, GOLD, RULE, MONO)
from svgkit import esc, header, base_css, bg

STATIC = os.environ.get("STATIC") == "1"

# 7x7 block glyphs. Add entries here to use letters not listed.
FONT = {
    "H": ["##   ##", "##   ##", "##   ##", "#######", "##   ##", "##   ##", "##   ##"],
    "E": ["#######", "##     ", "##     ", "#####  ", "##     ", "##     ", "#######"],
    "T": ["#######", "  ###  ", "  ###  ", "  ###  ", "  ###  ", "  ###  ", "  ###  "],
    "A": ["  ###  ", " ## ## ", "##   ##", "##   ##", "#######", "##   ##", "##   ##"],
    "N": ["##   ##", "###  ##", "#### ##", "## ####", "##  ###", "##   ##", "##   ##"],
    "S": [" ######", "##     ", "##     ", " ##### ", "     ##", "     ##", "###### "],
    "D": ["#####  ", "##  ## ", "##   ##", "##   ##", "##   ##", "##  ## ", "#####  "],
    "O": [" ##### ", "##   ##", "##   ##", "##   ##", "##   ##", "##   ##", " ##### "],
    "I": ["#######", "  ###  ", "  ###  ", "  ###  ", "  ###  ", "  ###  ", "#######"],
    "Z": ["#######", "    ## ", "   ##  ", "  ##   ", " ##    ", "##     ", "#######"],
    "Y": ["##   ##", "##   ##", " ## ## ", "  ###  ", "  ###  ", "  ###  ", "  ###  "],
    "R": ["#####  ", "##  ## ", "##  ## ", "#####  ", "## ##  ", "##  ## ", "##   ##"],
    "W": ["##   ##", "##   ##", "##   ##", "## # ##", "#######", "### ###", "##   ##"],
    "L": ["##     ", "##     ", "##     ", "##     ", "##     ", "##     ", "#######"],
    "U": ["##   ##", "##   ##", "##   ##", "##   ##", "##   ##", "##   ##", " ##### "],
    " ": ["       "] * 7,
}
MISSING = ["#######", "#     #", "#     #", "#     #", "#     #", "#     #", "#######"]
ROWS = 7


def lay_out(word: str):
    grid = [""] * ROWS
    chars = list(word.upper())
    for i, ch in enumerate(chars):
        g = FONT.get(ch)
        if g is None:
            print(f"  ! no glyph for {ch!r} — placeholder used; add it to FONT")
            g = MISSING
        for r in range(ROWS):
            grid[r] += g[r] + (" " if i < len(chars) - 1 else "")
    return grid


def build() -> str:
    grid = lay_out(WORDMARK)
    cols = len(grid[0])

    W, PAD = 880, 36
    art_w = W - PAD * 2
    cell = art_w / cols
    line_h = cell * 1.20
    fs = cell * 1.28   # < cell so glyphs stay discrete instead of merging into a blob

    y_eyebrow = 30
    y_top = 54
    art_h = line_h * ROWS
    y_rule = y_top + art_h + 26
    y_tag = y_rule + 30
    H = int(y_tag + 24)

    row_dur, stagger, lead = 0.5, 0.085, 0.25
    rule_delay = lead + ROWS * stagger + row_dur * 0.55
    tag_delay = rule_delay + 0.4

    def css(anim):
        return "opacity:1" if STATIC else f"animation:{anim}"

    out = [header(W, H, f"{WORDMARK} — {TAGLINE}"), bg(W, H), base_css()]

    # faint blueprint grid — the drafting table under the plate
    g = [f'<path d="M{x} 0V{H}"/>' for x in range(0, W, 40)]
    g += [f'<path d="M0 {y}H{W}"/>' for y in range(0, H, 40)]
    out.append(f'<g stroke="{RULE}" stroke-width="1" opacity=".45">{"".join(g)}</g>')

    # corner registration ticks — same drafting mark as the other plates,
    # but without a frame, so the banner stays full-bleed
    L, I = 12, 8
    ticks = "".join(
        f'<path d="M{cx + dx * L} {cy} H{cx} V{cy + dy * L}"/>'
        for cx, cy, dx, dy in ((I, I, 1, 1), (W - I, I, -1, 1),
                               (I, H - I, 1, -1), (W - I, H - I, -1, -1)))
    out.append(f'<g fill="none" stroke="{ULTRA}" stroke-width="1.4" opacity=".85" '
               f'class="fx" style="{css("fade .5s .05s forwards")}">{ticks}</g>')

    out.append(f'<text x="{PAD}" y="{y_eyebrow}" font-family="{MONO}" font-size="12.5" '
               f'letter-spacing="2.4" fill="{MUTED}" class="fx" '
               f'style="{css("fade .5s .05s forwards")}">github.com/{esc(USERNAME)}</text>')
    out.append(f'<text x="{W - PAD}" y="{y_eyebrow}" text-anchor="end" font-family="{MONO}" '
               f'font-size="12.5" letter-spacing="2.4" fill="{ULTRA}" class="fx" '
               f'style="{css("fade .5s .05s forwards")}">PLATE 01 — IDENT</text>')

    clips, art = [], []
    for r, line in enumerate(grid):
        begin = lead + r * stagger
        top = y_top + line_h * r
        base = top + line_h * 0.82
        cid = f"w{r}"

        w0 = art_w if STATIC else 0
        anim = "" if STATIC else (
            f'<animate attributeName="width" from="0" to="{art_w:.1f}" dur="{row_dur}s" '
            f'begin="{begin:.2f}s" fill="freeze" calcMode="spline" '
            f'keySplines="0.25 0.9 0.3 1" keyTimes="0;1"/>')
        clips.append(f'<clipPath id="{cid}"><rect x="{PAD}" y="{top - 2:.1f}" '
                     f'width="{w0}" height="{line_h + 4:.1f}">{anim}</rect></clipPath>')

        chars = "".join(
            f'<text x="{PAD + cell * (c + 0.5):.2f}" y="{base:.2f}">{ch}</text>'
            for c, ch in enumerate(line) if ch != " ")
        art.append(f'<g clip-path="url(#{cid})" font-family="{MONO}" font-size="{fs:.2f}" '
                   f'text-anchor="middle" fill="{BONE}">{chars}</g>')

        if not STATIC:
            art.append(
                f'<rect x="{PAD}" y="{top:.1f}" width="{cell:.2f}" '
                f'height="{line_h * 0.86:.2f}" fill="{ULTRA_LT}" opacity="0">'
                f'<animate attributeName="x" from="{PAD}" to="{PAD + art_w - cell:.1f}" '
                f'dur="{row_dur}s" begin="{begin:.2f}s" fill="freeze" calcMode="spline" '
                f'keySplines="0.25 0.9 0.3 1" keyTimes="0;1"/>'
                f'<animate attributeName="opacity" values="0;.9;.9;0" keyTimes="0;.05;.88;1" '
                f'dur="{row_dur}s" begin="{begin:.2f}s" fill="freeze"/></rect>')

    out.append("<defs>" + "".join(clips) + "</defs>")
    out.extend(art)

    x2 = W - PAD if STATIC else PAD
    out.append(f'<line x1="{PAD}" y1="{y_rule:.1f}" x2="{x2}" y2="{y_rule:.1f}" '
               f'stroke="{GOLD}" stroke-width="1.6" opacity=".9">'
               + ("" if STATIC else
                  f'<animate attributeName="x2" from="{PAD}" to="{W - PAD}" dur="0.65s" '
                  f'begin="{rule_delay:.2f}s" fill="freeze"/>')
               + "</line>")

    tw = art_w if STATIC else 0
    out.append(f'<defs><clipPath id="tagw"><rect x="{PAD}" y="{y_tag - 18:.1f}" '
               f'width="{tw}" height="26">'
               + ("" if STATIC else
                  f'<animate attributeName="width" from="0" to="{art_w}" dur="0.95s" '
                  f'begin="{tag_delay:.2f}s" fill="freeze"/>')
               + "</rect></clipPath></defs>")
    out.append(f'<g clip-path="url(#tagw)"><text x="{PAD}" y="{y_tag:.1f}" '
               f'font-family="{MONO}" font-size="15" letter-spacing="1.1" fill="{MUTED}">'
               f'<tspan fill="{ULTRA_LT}">$ </tspan>{esc(TAGLINE)}</text></g>')

    out.append("</svg>")
    return "\n".join(out)


if __name__ == "__main__":
    with open("art/wordmark.svg", "w", encoding="utf-8") as f:
        f.write(build())
    print("wrote art/wordmark.svg")

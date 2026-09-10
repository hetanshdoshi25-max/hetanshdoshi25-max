#!/usr/bin/env python3
"""
make_dossier.py, the neofetch-style identity card (left column, 520px).

Content lives in config.py so this file stays layout-only. Keep GitHub stats
OUT of here; the heatmap already covers those. This card is for the things a
contribution count can't say.

Height is computed from len(DOSSIER_ROWS), not hardcoded, so adding a row
here never breaks the layout the way a fixed H used to. make_projects.py
reads DOSSIER_H from here to stay in sync.

Static art. Regenerate when your details change.
    python scripts/make_dossier.py
    STATIC=1 python scripts/make_dossier.py   # frozen frame for previewing
"""
import os
from config import (DOSSIER_TITLE, DOSSIER_ROWS, LINKS, BONE, MUTED,
                    ULTRA, ULTRA_LT, GOLD, RULE, MONO)
from svgkit import esc, header, base_css, bg, plate

STATIC = os.environ.get("STATIC") == "1"

W = 520
PAD = 20
LABEL_X = PAD + 4
VALUE_X = PAD + 86

ROW_TOP = 68       # y of the first row's baseline
ROW_PITCH = 24.5
FOOTER_H = 64       # rule + link line + bottom margin below the last row

DOSSIER_H = int(ROW_TOP + len(DOSSIER_ROWS) * ROW_PITCH + FOOTER_H)


def build() -> str:
    H = DOSSIER_H

    def css(anim):
        return "opacity:1" if STATIC else f"animation:{anim}"

    out = [header(W, H, f"{DOSSIER_TITLE}, profile card"), bg(W, H), base_css()]
    out.append(plate(6, 6, W - 12, H - 12))

    out.append(f'<text x="{LABEL_X}" y="30" font-family="{MONO}" font-size="13" '
               f'fill="{BONE}" class="fx" style="{css("fade .45s .05s forwards")}">'
               f'<tspan fill="{ULTRA_LT}">$ </tspan>{esc(DOSSIER_TITLE)}</text>')
    out.append(f'<text x="{W - PAD}" y="30" text-anchor="end" font-family="{MONO}" '
               f'font-size="10.5" letter-spacing="2" fill="{MUTED}" class="fx" '
               f'style="{css("fade .45s .05s forwards")}">DOSSIER</text>')
    out.append(f'<line x1="{PAD}" y1="42" x2="{W - PAD}" y2="42" stroke="{RULE}" '
               f'stroke-width="1" class="fx" style="{css("fade .4s .12s forwards")}"/>')

    y = ROW_TOP
    for i, (label, value) in enumerate(DOSSIER_ROWS):
        d = 0.2 + i * 0.06
        style = css(f"slide .42s {d:.2f}s forwards")
        out.append(f'<g class="fx" style="{style}">'
                   f'<text x="{LABEL_X}" y="{y:.1f}" font-family="{MONO}" font-size="11.5" '
                   f'fill="{ULTRA}">{esc(label)}</text>'
                   f'<text x="{VALUE_X}" y="{y:.1f}" font-family="{MONO}" font-size="11.5" '
                   f'fill="{BONE}">{esc(value)}</text></g>')
        y += ROW_PITCH

    fy = H - 42
    out.append(f'<line x1="{PAD}" y1="{fy}" x2="{W - PAD}" y2="{fy}" stroke="{GOLD}" '
               f'stroke-width="1.2" opacity=".75" class="fx" '
               f'style="{css("fade .5s .85s forwards")}"/>')
    out.append(f'<text x="{LABEL_X}" y="{fy + 22}" font-family="{MONO}" font-size="11.5" '
               f'letter-spacing="0.6" fill="{ULTRA_LT}" class="fx" '
               f'style="{css("fade .5s .95s forwards")}">{esc(LINKS)}</text>')

    out.append("</svg>")
    return "\n".join(out)


if __name__ == "__main__":
    with open("art/dossier.svg", "w", encoding="utf-8") as f:
        f.write(build())
    print(f"wrote art/dossier.svg (H={DOSSIER_H}, {len(DOSSIER_ROWS)} rows)")

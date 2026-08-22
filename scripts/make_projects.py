#!/usr/bin/env python3
"""
make_projects.py , the "selected work" column (right column, 360px).

Height is pinned to the dossier card's 348px so the two <td>s in the README
table have flush bottom edges. If you change one, change both.

The 01/02/03 numbering earns its place here: it's a stated order of
importance, not decoration.

Static art.
    python scripts/make_projects.py
    STATIC=1 python scripts/make_projects.py
"""
import os
from config import PROJECTS, BONE, MUTED, ULTRA, ULTRA_LT, RULE, PANEL, MONO
from svgkit import esc, header, base_css, bg, plate

STATIC = os.environ.get("STATIC") == "1"

W, H = 360, 412          # H must match make_dossier.H
PAD = 18
CARD_H, GAP = 79, 8


def build() -> str:
    def css(anim):
        return "opacity:1" if STATIC else f"animation:{anim}"

    out = [header(W, H, "Selected work"), bg(W, H), base_css()]
    out.append(plate(6, 6, W - 12, H - 12))

    out.append(f'<text x="{PAD + 4}" y="30" font-family="{MONO}" font-size="11" '
               f'letter-spacing="2.4" fill="{MUTED}" class="fx" '
               f'style="{css("fade .45s .05s forwards")}">SELECTED WORK</text>')
    out.append(f'<line x1="{PAD}" y1="42" x2="{W - PAD}" y2="42" stroke="{RULE}" '
               f'stroke-width="1" class="fx" style="{css("fade .4s .12s forwards")}"/>')

    y = 54
    for i, (num, title, body) in enumerate(PROJECTS):
        d = 0.3 + i * 0.13
        out.append(f'<g class="fx" style="{css(f"rise .5s {d:.2f}s forwards")}">')
        out.append(f'<rect x="{PAD}" y="{y}" width="{W - PAD * 2}" height="{CARD_H}" '
                   f'rx="2" fill="{PANEL}" stroke="{RULE}" stroke-width="1"/>')
        # left spine , the accent that marks a card as an entry
        out.append(f'<rect x="{PAD}" y="{y}" width="2.5" height="{CARD_H}" fill="{ULTRA}"/>')
        out.append(f'<text x="{PAD + 14}" y="{y + 22}" font-family="{MONO}" font-size="10.5" '
                   f'letter-spacing="1.5" fill="{ULTRA_LT}">{esc(num)}</text>')
        out.append(f'<text x="{PAD + 44}" y="{y + 22}" font-family="{MONO}" font-size="12.5" '
                   f'letter-spacing="0.4" fill="{BONE}">{esc(title)}</text>')
        for j, line in enumerate(body.split("\n")):
            out.append(f'<text x="{PAD + 14}" y="{y + 46 + j * 15}" font-family="{MONO}" '
                       f'font-size="10.5" fill="{MUTED}">{esc(line)}</text>')
        out.append("</g>")
        y += CARD_H + GAP

    out.append("</svg>")
    return "\n".join(out)


if __name__ == "__main__":
    with open("art/projects.svg", "w", encoding="utf-8") as f:
        f.write(build())
    print("wrote art/projects.svg")

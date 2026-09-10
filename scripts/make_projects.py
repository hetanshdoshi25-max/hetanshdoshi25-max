#!/usr/bin/env python3
"""
make_projects.py, the "selected work" column (right column, 360px).

Height is imported from make_dossier.DOSSIER_H, not hardcoded, so the two
<td>s in the README table always have flush bottom edges no matter how many
rows or cards either side has. Card height is then derived to fill that space
evenly, so adding a project here never requires hand-tuning CARD_H.

The 01/02/03... numbering is a stated order of importance, not decoration.

Static art.
    python scripts/make_projects.py
    STATIC=1 python scripts/make_projects.py
"""
import os
from config import PROJECTS, BONE, MUTED, ULTRA, ULTRA_LT, RULE, PANEL, MONO
from svgkit import esc, header, base_css, bg, plate
from make_dossier import DOSSIER_H

STATIC = os.environ.get("STATIC") == "1"

W, H = 360, DOSSIER_H
PAD = 18
TOP = 54
GAP = 8
BOTTOM_MARGIN = 16

N = len(PROJECTS)
CARD_H = (H - TOP - BOTTOM_MARGIN - (N - 1) * GAP) / N


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

    y = TOP
    for i, (num, title, body) in enumerate(PROJECTS):
        d = 0.3 + i * 0.11
        out.append(f'<g class="fx" style="{css(f"rise .5s {d:.2f}s forwards")}">')
        out.append(f'<rect x="{PAD}" y="{y:.1f}" width="{W - PAD * 2}" height="{CARD_H:.1f}" '
                   f'rx="2" fill="{PANEL}" stroke="{RULE}" stroke-width="1"/>')
        out.append(f'<rect x="{PAD}" y="{y:.1f}" width="2.5" height="{CARD_H:.1f}" fill="{ULTRA}"/>')
        out.append(f'<text x="{PAD + 14}" y="{y + 22:.1f}" font-family="{MONO}" font-size="10.5" '
                   f'letter-spacing="1.5" fill="{ULTRA_LT}">{esc(num)}</text>')
        out.append(f'<text x="{PAD + 44}" y="{y + 22:.1f}" font-family="{MONO}" font-size="12.5" '
                   f'letter-spacing="0.4" fill="{BONE}">{esc(title)}</text>')
        for j, line in enumerate(body.split("\n")):
            out.append(f'<text x="{PAD + 14}" y="{y + 46 + j * 15:.1f}" font-family="{MONO}" '
                       f'font-size="10.5" fill="{MUTED}">{esc(line)}</text>')
        out.append("</g>")
        y += CARD_H + GAP

    out.append("</svg>")
    return "\n".join(out)


if __name__ == "__main__":
    with open("art/projects.svg", "w", encoding="utf-8") as f:
        f.write(build())
    print(f"wrote art/projects.svg (H={H}, {N} cards, card_h={CARD_H:.1f})")

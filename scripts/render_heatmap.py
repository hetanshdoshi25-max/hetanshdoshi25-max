#!/usr/bin/env python3
"""
render_heatmap.py — data/contributions.json -> art/heatmap.svg

The 53x7 calendar drops in on a diagonal sweep (delay scales with column+row),
then freezes. CSS keyframes with animation-fill-mode: forwards; nothing loops.

Palette is a deliberate departure from GitHub green: an exposure ramp from
unexposed ink through ultramarine to a pale gold at the top level, so your
heaviest days read as burnt into the plate. The single busiest day gets a gold
ring — the second and last use of gold in the whole profile.

Dynamic art. The Actions workflow re-runs this every day.
    python scripts/render_heatmap.py
    STATIC=1 python scripts/render_heatmap.py   # frozen frame for previewing
"""
import json
import os
from datetime import date

from config import RAMP, BONE, MUTED, ULTRA, ULTRA_LT, GOLD, RULE, MONO
from svgkit import esc, header, base_css, bg, plate

STATIC = os.environ.get("STATIC") == "1"

W = 880
PAD = 22
GRID_X = 62          # room for the weekday gutter
GRID_Y = 74
PITCH = 15.2
CELL = 12.2
WEEKS = 53
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def build(data) -> str:
    def css(anim):
        return "opacity:1" if STATIC else f"animation:{anim}"

    days = data["days"]
    # normalise week index so the oldest visible week is column 0
    base_week = min(d["week"] for d in days)
    peak_date = data["best_day"]["date"]

    grid_h = PITCH * 7
    y_rule = GRID_Y + grid_h + 20
    y_stats = y_rule + 26
    H = int(y_stats + 34)

    out = [header(W, H, f"{data['total']} contributions in the last year"),
           bg(W, H), base_css()]
    out.append(plate(6, 6, W - 12, H - 12))

    # ---- header line -------------------------------------------------
    out.append(f'<text x="{PAD + 12}" y="34" font-family="{MONO}" font-size="13" '
               f'fill="{BONE}" class="fx" style="{css("fade .45s .05s forwards")}">'
               f'<tspan fill="{ULTRA_LT}">$ </tspan>contributions --last-year</text>')
    out.append(f'<text x="{W - PAD - 12}" y="34" text-anchor="end" font-family="{MONO}" '
               f'font-size="10.5" letter-spacing="2" fill="{MUTED}" class="fx" '
               f'style="{css("fade .45s .05s forwards")}">'
               f'UPDATED {esc(data["generated_at"][:10])}</text>')
    out.append(f'<line x1="{PAD + 8}" y1="46" x2="{W - PAD - 8}" y2="46" stroke="{RULE}" '
               f'stroke-width="1" class="fx" style="{css("fade .4s .12s forwards")}"/>')

    # ---- month labels ------------------------------------------------
    seen = set()
    labels = []
    for d in days:
        col = d["week"] - base_week
        month = int(d["date"][5:7])
        if month not in seen and int(d["date"][8:10]) <= 7:
            seen.add(month)
            labels.append((col, MONTHS[month - 1]))
    for col, name in labels:
        x = GRID_X + col * PITCH
        if x > W - PAD - 30:
            continue
        out.append(f'<text x="{x:.1f}" y="{GRID_Y - 10}" font-family="{MONO}" '
                   f'font-size="10" fill="{MUTED}" class="fx" '
                   f'style="{css("fade .4s .2s forwards")}">{name}</text>')

    # ---- weekday gutter (Mon/Wed/Fri, the GitHub convention) ----------
    for row, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        out.append(f'<text x="{GRID_X - 10}" y="{GRID_Y + row * PITCH + CELL - 2:.1f}" '
                   f'text-anchor="end" font-family="{MONO}" font-size="10" fill="{MUTED}" '
                   f'class="fx" style="{css("fade .4s .2s forwards")}">{name}</text>')

    # ---- the grid: diagonal sweep -------------------------------------
    cells = []
    for d in days:
        col = d["week"] - base_week
        row = date.fromisoformat(d["date"]).isoweekday() % 7   # Sunday = 0
        x = GRID_X + col * PITCH
        y = GRID_Y + row * PITCH
        fill = RAMP[min(d["level"], len(RAMP) - 1)]
        delay = 0.30 + (col + row) * 0.011
        style = "opacity:1" if STATIC else f"animation:drop .34s {delay:.2f}s forwards"
        cells.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{CELL}" height="{CELL}" rx="2.5" '
            f'fill="{fill}" class="fx" style="{style};transform-origin:'
            f'{x + CELL / 2:.1f}px {y + CELL / 2:.1f}px">'
            f'<title>{esc(d["date"])}: {d["count"]}</title></rect>')
        if d["date"] == peak_date and d["count"] > 0:
            ring_delay = delay + 0.5
            rstyle = "opacity:1" if STATIC else f"animation:fade .5s {ring_delay:.2f}s forwards"
            cells.append(
                f'<rect x="{x - 2.4:.1f}" y="{y - 2.4:.1f}" width="{CELL + 4.8}" '
                f'height="{CELL + 4.8}" rx="4" fill="none" stroke="{GOLD}" '
                f'stroke-width="1.4" class="fx" style="{rstyle}"/>')
    out.extend(cells)

    out.append(f'<line x1="{PAD + 8}" y1="{y_rule:.1f}" x2="{W - PAD - 8}" y2="{y_rule:.1f}" '
               f'stroke="{RULE}" stroke-width="1" class="fx" '
               f'style="{css("fade .5s 1.1s forwards")}"/>')

    # ---- stats row ----------------------------------------------------
    stats = [
        ("contributions", f'{data["total"]:,}'),
        ("current streak", f'{data["current_streak"]} d'),
        ("longest streak", f'{data["longest_streak"]} d'),
        ("best day", f'{data["best_day"]["count"]} on {data["best_day"]["date"][5:]}'),
    ]
    x = PAD + 12
    for i, (label, value) in enumerate(stats):
        d = 1.2 + i * 0.08
        out.append(f'<g class="fx" style="{css(f"rise .45s {d:.2f}s forwards")}">'
                   f'<text x="{x}" y="{y_stats:.1f}" font-family="{MONO}" font-size="10" '
                   f'letter-spacing="1.6" fill="{MUTED}">{esc(label.upper())}</text>'
                   f'<text x="{x}" y="{y_stats + 19:.1f}" font-family="{MONO}" '
                   f'font-size="14" fill="{BONE}">{esc(value)}</text></g>')
        x += 178

    # ---- legend -------------------------------------------------------
    lx = W - PAD - 12 - (len(RAMP) * 15 + 66)
    ly = y_stats + 8
    out.append(f'<g class="fx" style="{css("fade .5s 1.5s forwards")}">')
    out.append(f'<text x="{lx}" y="{ly + 9}" font-family="{MONO}" font-size="10" '
               f'fill="{MUTED}">less</text>')
    for i, c in enumerate(RAMP):
        out.append(f'<rect x="{lx + 34 + i * 15}" y="{ly}" width="11" height="11" rx="2.5" '
                   f'fill="{c}"/>')
    out.append(f'<text x="{lx + 34 + len(RAMP) * 15 + 6}" y="{ly + 9}" font-family="{MONO}" '
               f'font-size="10" fill="{MUTED}">more</text>')
    out.append("</g>")

    out.append("</svg>")
    return "\n".join(out)


if __name__ == "__main__":
    with open("data/contributions.json", encoding="utf-8") as f:
        data = json.load(f)
    os.makedirs("art", exist_ok=True)
    with open("art/heatmap.svg", "w", encoding="utf-8") as f:
        f.write(build(data))
    print(f"wrote art/heatmap.svg ({data['total']} contributions)")

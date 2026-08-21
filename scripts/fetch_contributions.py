#!/usr/bin/env python3
"""
fetch_contributions.py — pulls a year of real contribution data and writes
data/contributions.json.

No GraphQL, no personal access token, no secret to rotate: GitHub serves the
contribution calendar as public HTML at

    https://github.com/users/<username>/contributions

which is the same fragment the profile page itself loads. We parse the day
cells out of it.

That endpoint is unversioned and can change without notice, so this script
fails loudly rather than quietly writing an empty grid — a red X in the
Actions tab is much easier to notice than a blank image on your profile.

    python scripts/fetch_contributions.py
"""
import json
import os
import re
import sys
from collections import defaultdict
from datetime import date, datetime, timezone

import requests
from bs4 import BeautifulSoup

from config import USERNAME

URL = f"https://github.com/users/{USERNAME}/contributions"
OUT = "data/contributions.json"
MIN_DAYS = 300          # a real year is 365-371; anything less means the parse broke
UA = "Mozilla/5.0 (compatible; profile-art/1.0; +https://github.com/%s)" % USERNAME


def scrape():
    r = requests.get(URL, headers={"User-Agent": UA,
                                   "Accept": "text/html",
                                   "X-Requested-With": "XMLHttpRequest"}, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    # counts live in sibling <tool-tip for="cell-id"> nodes in current markup
    tips = {}
    for tip in soup.find_all("tool-tip"):
        target = tip.get("for")
        if not target:
            continue
        m = re.match(r"^\s*(No|\d[\d,]*)\s+contribution", tip.get_text(strip=True))
        if m:
            tips[target] = 0 if m.group(1) == "No" else int(m.group(1).replace(",", ""))

    days = []
    for td in soup.select("td.ContributionCalendar-day"):
        d = td.get("data-date")
        if not d:
            continue
        count = tips.get(td.get("id"))
        if count is None:                       # older markup exposed it directly
            raw = td.get("data-count")
            count = int(raw) if raw is not None else 0
        days.append({
            "date": d,
            "count": count,
            "level": int(td.get("data-level") or 0),
            "week": int(td.get("data-ix") or 0),
        })

    days.sort(key=lambda x: x["date"])
    add_top_tier(days)
    return days


def add_top_tier(days):
    """
    GitHub only ever emits data-level 0-4. The renderer's ramp has a sixth,
    brightest step, so promote the top decile of active days to level 5 —
    the brightest tier has to be earned rather than handed out.
    """
    active = sorted(d["count"] for d in days if d["count"] > 0)
    if len(active) < 20:
        return
    cutoff = active[int(len(active) * 0.9)]
    for d in days:
        if d["level"] >= 4 and d["count"] >= cutoff:
            d["level"] = 5


def streaks(days):
    """Current streak allows an empty today — the day isn't over yet."""
    counts = [d["count"] for d in days]

    cur = 0
    idx = len(counts) - 1
    if idx >= 0 and counts[idx] == 0:
        idx -= 1
    while idx >= 0 and counts[idx] > 0:
        cur += 1
        idx -= 1

    best = run = 0
    best_end = run_start = None
    best_start = None
    for d in days:
        if d["count"] > 0:
            run = run + 1 if run else 1
            run_start = run_start or d["date"]
            if run > best:
                best, best_start, best_end = run, run_start, d["date"]
        else:
            run, run_start = 0, None
    return cur, best, best_start, best_end


def main():
    days = scrape()
    if len(days) < MIN_DAYS:
        sys.exit(f"FAIL: parsed {len(days)} day cells (expected >= {MIN_DAYS}). "
                 "GitHub's calendar markup probably changed — fix the selector "
                 "in fetch_contributions.py before this ships a blank heatmap.")

    total = sum(d["count"] for d in days)
    cur, best, best_start, best_end = streaks(days)
    peak = max(days, key=lambda d: d["count"])

    monthly = defaultdict(int)
    for d in days:
        monthly[d["date"][:7]] += d["count"]

    payload = {
        "username": USERNAME,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "range": {"from": days[0]["date"], "to": days[-1]["date"]},
        "total": total,
        "current_streak": cur,
        "longest_streak": best,
        "longest_streak_range": [best_start, best_end],
        "best_day": {"date": peak["date"], "count": peak["count"]},
        "monthly": dict(sorted(monthly.items())),
        "days": days,
    }

    os.makedirs("data", exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=1)
        f.write("\n")
    print(f"wrote {OUT}: {len(days)} days, {total} contributions, "
          f"streak {cur}, longest {best}")


if __name__ == "__main__":
    main()

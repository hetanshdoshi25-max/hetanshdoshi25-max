# Profile art pipeline

Everything on the profile is an animated SVG committed to this repo. Nothing is
fetched from a third-party widget service at render time, so nothing can
rate-limit you or show a broken-image icon on your profile.

## How it fits together

```
scripts/config.py          palette + all copy — the only file you normally edit
      │
      ├─ make_wordmark.py  ──> art/wordmark.svg    static
      ├─ make_dossier.py   ──> art/dossier.svg     static
      ├─ make_projects.py  ──> art/projects.svg    static
      │
      └─ fetch_contributions.py ──> data/contributions.json ──> render_heatmap.py
                                                                   │
                                                                   v
                                                            art/heatmap.svg
                                                                DYNAMIC
                                                        (rebuilt daily by Actions)
```

`README.md` only places the four SVGs. It contains no animation of its own,
because GitHub strips `<script>` and sanitises inline CSS in READMEs.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r scripts/requirements.txt
export PYTHONPATH=scripts
```

## Rebuild the static plates

Do this after editing `config.py`:

```bash
python scripts/make_wordmark.py
python scripts/make_dossier.py
python scripts/make_projects.py
```

You can also trigger it without a local checkout: **Actions → Update profile
art → Run workflow → tick "Also rebuild static art"**.

## Rebuild the heatmap by hand

```bash
python scripts/fetch_contributions.py
python scripts/render_heatmap.py
```

## Previewing

Animations play once and freeze, which makes local preview awkward — most
viewers show frame 0, i.e. an empty plate. Set `STATIC=1` to emit the final
frame instead:

```bash
STATIC=1 python scripts/make_wordmark.py   # frozen; do NOT commit this version
```

Regenerate without `STATIC` before committing. To see the real animation, open
the SVG in a browser and hard-reload.

## Things worth knowing

- **Fonts resolve on the viewer's machine.** SVG can't ship a font here, so
  everything uses a generic monospace stack. The wordmark positions every
  character at an exact x rather than trusting an advance width, so the grid
  survives whatever fallback font a viewer has.
- **The contributions endpoint is unversioned.** `fetch_contributions.py` exits
  non-zero if it parses fewer than 300 day cells, so a markup change on
  GitHub's side surfaces as a failed workflow rather than a blank heatmap.
- **Private repos are excluded by default.** Turn on *Settings → Public profile
  → Contributions → Include private contributions on my profile* or the
  heatmap will undercount your actual work.
- **Animations play once and freeze.** Nothing loops. A profile that pulses
  forever is noise; one that prints itself in once reads as deliberate.
- **`prefers-reduced-motion` is respected** — the SVGs jump straight to the
  final frame for anyone who's asked for that.

"""
Single source of truth for the profile art.
Edit this file, re-run the generators, commit. Nothing else needs touching.
"""

USERNAME = "hetanshdoshi25-max"

# ---------------------------------------------------------------- palette
# "Blueprint Dossier": deep ink ground, ultramarine structure, bone type,
# gold used exactly twice (classification rule + best-day marker).
INK = "#0A0C12"   # ground
PANEL = "#11141D"   # raised surfaces
RULE = "#1C2233"   # hairlines, grid, crop marks
BONE = "#E7E3D8"   # primary type
MUTED = "#6F7891"   # labels, captions
ULTRA = "#3B5BFF"   # accent structure
ULTRA_LT = "#8AA0FF"   # accent type
GOLD = "#C8A227"   # rationed accent

# Contribution exposure ramp — deliberately NOT GitHub green.
# Reads as a photographic plate: unexposed ink, exposed ultramarine, blown-out white.
# GitHub only emits levels 0-4; level 5 is derived locally (top decile) so the
# brightest tier has to be earned. See fetch_contributions.py.
RAMP = ["#141824", "#1D2A6B", "#2A44C4", "#3B5BFF", "#7E97FF", "#C9D6FF"]

# SVG can only use fonts present on the *viewer's* machine, so every face
# must be a generic fallback chain. The monotype constraint is the aesthetic.
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'DejaVu Sans Mono', monospace"

# ---------------------------------------------------------------- content
WORDMARK = "HETANSH"
TAGLINE = "founder / aethon  ·  full-stack  ·  mumbai"

DOSSIER_TITLE = "hetansh@github"
DOSSIER_ROWS = [
    ("now",      "Founder & sole engineer — Aethon (aethonchat.com)"),
    ("building", "AETHON-ZYRA — desktop AI assistant, voice + gesture"),
    ("agency",   "WALNUTS Media — social, 12+ client accounts"),
    ("also",     "717 Productions · independent content"),
    ("study",    "Computer Engineering, SAKEC Mumbai — year 2"),
    ("stack",    "TypeScript · Next.js · Python · FastAPI · Electron"),
    ("ai",       "Gemini Live · Groq · LiveKit · Supabase · Firebase"),
    ("metal",    "Raspberry Pi · MediaPipe · OpenCV"),
    ("off-duty", "lifting · bikes · watches"),
    ("loc",      "Mumbai, IN — UTC+5:30"),
]

# Right-hand column. These map to real public repos so the names are checkable.
# Keep to three; a fourth breaks the height match with the dossier card.
PROJECTS = [
    ("01", "aethon-releases",   "Desktop AI assistant. Voice, gesture control,\nfile generation, Telegram remote."),
    ("02", "hetansh-portfolio", "hetanshdoshi.com — editorial dossier build,\nNext.js on Vercel."),
    ("03", "resume-analyzer",   "JavaFX + MySQL + Gemini. Reads a PDF resume,\nfinds the skill gaps."),
]

LINKS = "hetanshdoshi.com   ·   aethonchat.com"

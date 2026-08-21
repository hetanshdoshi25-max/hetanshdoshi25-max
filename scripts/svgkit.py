"""Small helpers shared by every generator. No dependencies."""

from config import INK, PANEL, RULE, ULTRA


def esc(s: str) -> str:
    """XML-escape. ASCII art is full of & < > so this is not optional."""
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;")
             .replace('"', "&quot;"))


def header(w: int, h: int, title: str) -> str:
    """Root <svg>. role=img + <title> so screen readers get something."""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}">\n'
        f'<title>{esc(title)}</title>\n'
    )


def base_css(extra: str = "") -> str:
    """
    Every animation plays exactly once and freezes (fill-mode: forwards).
    Nothing loops — a README that pulses forever is noise.
    prefers-reduced-motion jumps straight to the final frame.
    """
    return f"""<style>
  .fx {{ opacity: 0; animation-fill-mode: forwards; animation-timing-function: cubic-bezier(.2,.7,.2,1); }}
  @keyframes rise {{ from {{ opacity: 0; transform: translateY(6px); }} to {{ opacity: 1; transform: translateY(0); }} }}
  @keyframes fade {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
  @keyframes drop {{ from {{ opacity: 0; transform: translateY(-7px) scale(.72); }} to {{ opacity: 1; transform: translateY(0) scale(1); }} }}
  @keyframes slide {{ from {{ opacity: 0; transform: translateX(-10px); }} to {{ opacity: 1; transform: translateX(0); }} }}
  @media (prefers-reduced-motion: reduce) {{
    .fx {{ opacity: 1 !important; animation: none !important; transform: none !important; }}
  }}
{extra}</style>
"""


def plate(x, y, w, h, fill=PANEL, stroke=RULE, tick=True, tick_color=ULTRA):
    """
    A panel with drafting registration marks at the corners instead of a
    plain box. The ticks are the structural device: this is a plate, not a card.
    """
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" '
           f'fill="{fill}" stroke="{stroke}" stroke-width="1"/>']
    if tick:
        L = 9
        for cx, cy, dx, dy in ((x, y, 1, 1), (x + w, y, -1, 1),
                               (x, y + h, 1, -1), (x + w, y + h, -1, -1)):
            out.append(
                f'<path d="M{cx + dx * L} {cy} H{cx} V{cy + dy * L}" '
                f'fill="none" stroke="{tick_color}" stroke-width="1.4" opacity=".85"/>')
    return "\n".join(out)


def bg(w, h):
    return f'<rect width="{w}" height="{h}" fill="{INK}"/>'

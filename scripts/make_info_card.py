# =============================================================================
# make_info_card.py — generates info-card.svg (neofetch-style info panel)
# Supports STATIC=1 env var for a frozen single-frame version.
# =============================================================================
import os
import sys

from pathlib import Path
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import theme
from svg import SVG
from utils import repo_path, info_line_delay

STATIC = os.getenv("STATIC") == "1"

W = theme.INFO_W
H = theme.INFO_H

svg = SVG(W, H)

# ===========================
# Window background
# ===========================
svg.rect(0, 0, W, H, theme.WINDOW, radius=16, stroke=theme.BORDER)

# ===========================
# Title bar
# ===========================
TITLEBAR_H = 42
svg.rect(0, 0, W, TITLEBAR_H, theme.TITLE, radius=16)
svg.rect(0, TITLEBAR_H // 2, W, TITLEBAR_H // 2, theme.TITLE)

svg.circle(22, 21, 6, theme.RED)
svg.circle(44, 21, 6, theme.YELLOW)
svg.circle(66, 21, 6, theme.LIME)

svg.text(W // 2, 27, "neofetch", size=13, color=theme.GRAY, anchor="middle")

# ===========================
# Prompt header (akshita@github)
# ===========================
HEADER_Y = 68
svg.text(26, HEADER_Y, "akshita30",
         size=18, color=theme.GREEN, weight="bold")
svg.text(26 + 9 * 10, HEADER_Y, "@",
         size=18, color=theme.TEXT)
svg.text(26 + 10 * 10, HEADER_Y, "github",
         size=18, color=theme.BLUE)

# Separator
svg.raw(
    f'<line x1="22" y1="{HEADER_Y + 10}" x2="{W - 22}" y2="{HEADER_Y + 10}" '
    f'stroke="{theme.BORDER}" stroke-width="1"/>'
)

# ===========================
# Neofetch info rows
# info_rows: list of (label, value, label_color, value_color)
# ===========================
info_rows = [
    ("Now",       "Building AI Systems",      theme.GREEN, theme.TEXT),
    ("Role",      "CS Student + SDE Intern",  theme.GREEN, theme.TEXT),
    ("Backend",   "Spring Boot · FastAPI",    theme.GREEN, theme.TEXT),
    ("AI/ML",     "PyTorch · LangChain",      theme.GREEN, theme.TEXT),
    ("Cloud",     "AWS · GCP · Docker",       theme.GREEN, theme.TEXT),
    ("DB",        "PostgreSQL · MongoDB",      theme.GREEN, theme.TEXT),
    ("Editor",    "VS Code · IntelliJ",        theme.GREEN, theme.TEXT),
    ("Location",  "India 🇮🇳",               theme.GREEN, theme.TEXT),
    ("Highlight", "Open to Collaboration",    theme.BLUE,  theme.GRAY),
]

ROW_START_Y  = HEADER_Y + 30   # y of first row
ROW_H        = 28               # pixels per row
LABEL_X      = 32
VALUE_X      = 185
FS           = theme.FONT_SIZE_INFO

# base delay — start info card lines after title-bar animation
BASE_DELAY   = 0.0 if STATIC else 0.5

for i, (label, value, lc, vc) in enumerate(info_rows):
    d = 0.0 if STATIC else info_line_delay(i, base_delay=BASE_DELAY)
    row_y = ROW_START_Y + i * ROW_H

    if STATIC:
        svg.text(LABEL_X, row_y, label, size=FS, color=lc, weight="bold")
        svg.text(VALUE_X, row_y, value, size=FS, color=vc)
    else:
        # Animated: fade-in + translate for the whole row (label + value grouped)
        svg.raw(f'<g opacity="0">')
        svg.raw(
            f'<animate attributeName="opacity" from="0" to="1" '
            f'begin="{d}s" dur="{theme.INFO_FADE_DUR}s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" '
            f'from="0,8" to="0,0" '
            f'begin="{d}s" dur="{theme.INFO_FADE_DUR}s" fill="freeze"/>'
        )
        svg.text(LABEL_X, row_y, label, size=FS, color=lc, weight="bold")
        svg.text(VALUE_X, row_y, value, size=FS, color=vc)
        svg.raw("</g>")

# ===========================
# Color-bar "OS palette" strip at the bottom
# ===========================
STRIP_Y  = H - 30
STRIP_H  = 12
STRIP_W  = W // 8
colors   = [theme.RED, theme.YELLOW, theme.LIME, theme.BLUE,
            theme.GREEN, theme.GRAY, theme.TEXT, theme.BORDER]
for idx, c in enumerate(colors):
    svg.rect(idx * STRIP_W, STRIP_Y, STRIP_W, STRIP_H, c)

# ===========================
# Write output
# ===========================
output = repo_path("info-card.svg")
svg.save(str(output))
print(f"info-card.svg -> {output}")

# =============================================================================
# make_terminal.py — generates avi-ascii.svg (ASCII portrait terminal window)
# Orchestrates: ascii.AsciiImage -> clip-path wipe SVG, neofetch prompt header.
# Set STATIC=1 to emit a frozen single-frame for local preview tools.
# Run from any directory: python scripts/make_terminal.py
# =============================================================================
import os
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import theme
from svg import SVG
from render_ascii import render as render_ascii
from utils import repo_path

STATIC = os.getenv("STATIC") == "1"

W = theme.PORTRAIT_W   # 560
H = theme.PORTRAIT_H   # 630

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
# Flat bottom strip to square off the lower half of the rounded title bar
svg.rect(0, TITLEBAR_H // 2, W, TITLEBAR_H // 2, theme.TITLE)

svg.circle(22, 21, 6, theme.RED)
svg.circle(44, 21, 6, theme.YELLOW)
svg.circle(66, 21, 6, theme.LIME)

svg.text(W // 2, 27, "terminal", size=13, color=theme.GRAY, anchor="middle")

# ===========================
# Prompt: akshita@github ~
# ===========================
PROMPT_Y = 68
svg.text(26, PROMPT_Y, "akshita30",
         size=18, color=theme.GREEN, weight="bold")
svg.text(26 + 9 * 10, PROMPT_Y, "@",
         size=18, color=theme.TEXT)
svg.text(26 + 10 * 10, PROMPT_Y, "github",
         size=18, color=theme.BLUE)

# Separator line
svg.raw(
    f'<line x1="22" y1="{PROMPT_Y + 10}" x2="{W - 22}" y2="{PROMPT_Y + 10}" '
    f'stroke="{theme.BORDER}" stroke-width="1"/>'
)

# ===========================
# $ neofetch  (typing animation)
# ===========================
CMD_Y = PROMPT_Y + 32
svg.text(26, CMD_Y, "$", size=20, color=theme.GREEN)

command = "neofetch"
base_delay = 0.0 if STATIC else theme.TYPING_START

if STATIC:
    # Static: emit the full command in one text element
    svg.text(46, CMD_Y, command, size=19, color=theme.TEXT)
else:
    # Animated: each character appears individually
    for i, ch in enumerate(command):
        char_delay = round(base_delay + i * theme.TYPING_STAGGER, 3)
        svg.animated_text(
            46 + i * 11, CMD_Y, ch, char_delay,
            size=19, color=theme.TEXT
        )

# ===========================
# ASCII Portrait
# ===========================
PORTRAIT_X = 26
PORTRAIT_Y = CMD_Y + 22   # a little breathing room below the prompt

portrait_delay = 0.0 if STATIC else round(
    base_delay + len(command) * theme.TYPING_STAGGER + 0.2, 3
)

svg.raw(render_ascii(
    repo_path("source-prepped.png"),
    x=PORTRAIT_X,
    y=PORTRAIT_Y,
    delay=portrait_delay,
))

# ===========================
# Output
# ===========================
output = repo_path("avi-ascii.svg")
svg.save(str(output))
print(f"avi-ascii.svg -> {output}")
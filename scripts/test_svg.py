# =============================================================================
# test_svg.py — quick sanity test for SVG builder
# =============================================================================
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import theme
from svg import SVG
from utils import repo_path

svg = SVG(400, 200)

svg.rect(0, 0, 400, 200, theme.WINDOW)
svg.text(20, 40, "SVG Engine Works", 20, theme.GREEN)
svg.text(20, 70, f"RAMP: {theme.RAMP!r}", 14, theme.TEXT)
svg.text(20, 100, f"ASCII_FILL: {theme.ASCII_FILL}", 14, theme.BLUE)

out = repo_path("test.svg")
svg.save(str(out))
print(f"test.svg -> {out}")
# =============================================================================
# test_ascii.py — quick sanity test: source-prepped.png -> ascii-test.svg
# =============================================================================
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from svg import SVG
from render_ascii import render
from utils import repo_path

svg = SVG(920, 700)

svg.raw(render(
    repo_path("source-prepped.png"),
    x=20,
    y=20,
    delay=0.0,
))

out = repo_path("ascii-test.svg")
svg.save(str(out))
print(f"ascii-test.svg -> {out}")
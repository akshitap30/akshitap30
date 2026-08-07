# =============================================================================
# render_ascii.py — thin wrapper: image path -> SVG fragment string
# All rendering logic lives in ascii.AsciiImage.render() which uses theme.py.
# =============================================================================
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import theme
from ascii import AsciiImage


def render(image_path, x: int, y: int, delay: float = 0.0) -> str:
    """Generate an SVG fragment of the ASCII portrait with row-wipe reveal.

    Args:
        image_path: Absolute path (or repo_path result) to source-prepped.png.
        x:          Left edge of the ASCII block in the parent SVG.
        y:          Baseline y of the first row.
        delay:      Base seconds before the first row starts animating.

    Returns:
        SVG fragment string (no outer <svg> tag).
    """
    img = AsciiImage(image_path, width=theme.ASCII_COLS)
    return img.render(x=x, y=y, delay=delay)

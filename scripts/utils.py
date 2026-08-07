# =============================================================================
# utils.py — shared helpers: path resolution, SVG boilerplate, timing math
# =============================================================================
from pathlib import Path
from html import escape

# --------------- Path resolution (fixes CWD bug) ----------------------------
# Always resolves relative to the repository root regardless of where the
# calling script is invoked from.
_SCRIPTS_DIR = Path(__file__).resolve().parent
REPO_ROOT    = _SCRIPTS_DIR.parent


def repo_path(*parts: str) -> Path:
    """Return an absolute path relative to the repo root.

    Usage:
        repo_path("data", "contributions.json")  # → <repo>/data/contributions.json
        repo_path("contrib-heatmap.svg")          # → <repo>/contrib-heatmap.svg
    """
    return REPO_ROOT.joinpath(*parts)


def scripts_path(*parts: str) -> Path:
    """Return an absolute path relative to the scripts/ directory."""
    return _SCRIPTS_DIR.joinpath(*parts)


# --------------- Animation stagger math -------------------------------------
def ascii_row_delay(row_index: int, base_delay: float = 0.0,
                    stagger: float | None = None) -> float:
    """Return the begin-time (seconds) for row `row_index` of the ASCII wipe."""
    from theme import ASCII_ROW_STAGGER
    if stagger is None:
        stagger = ASCII_ROW_STAGGER
    return round(base_delay + row_index * stagger, 4)


def info_line_delay(line_index: int, base_delay: float = 0.0,
                    stagger: float | None = None) -> float:
    """Return the begin-time (seconds) for info-card line `line_index`."""
    from theme import INFO_LINE_STAGGER
    if stagger is None:
        stagger = INFO_LINE_STAGGER
    return round(base_delay + line_index * stagger, 4)


def heatmap_col_delay(col_index: int, row_index: int,
                      stagger: float | None = None) -> float:
    """Return the begin-time for a heatmap cell at (col, row).

    Diagonal wave: begin = (col + row) * stagger
    """
    from theme import HEATMAP_COL_STAGGER
    if stagger is None:
        stagger = HEATMAP_COL_STAGGER
    return round((col_index + row_index) * stagger, 4)


# --------------- Lightweight SVG free-functions (for non-class callers) -----
def svg_start(width: int, height: int) -> str:
    return (
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">\n'
    )


def svg_end() -> str:
    return "</svg>"


def rect(x, y, w, h, fill, radius=0, stroke=None, stroke_width=1) -> str:
    s = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" '
         f'rx="{radius}" fill="{fill}"')
    if stroke:
        s += f' stroke="{stroke}" stroke-width="{stroke_width}"'
    s += "/>"
    return s


def circle(cx, cy, r, fill) -> str:
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"/>'


def text(x, y, value, size=16, color="#ffffff",
         weight="normal", family="monospace", anchor="start") -> str:
    return (
        f'<text x="{x}" y="{y}" font-family="{family}" '
        f'font-size="{size}" font-weight="{weight}" '
        f'text-anchor="{anchor}" fill="{color}">'
        f'{escape(str(value))}</text>'
    )


def fade_translate(delay: float, dur: float = 0.25,
                   dx: int = 0, dy: int = 8) -> str:
    """SMIL animations: opacity fade-in + translate slide-in."""
    return (
        f'<animate attributeName="opacity" from="0" to="1" '
        f'begin="{delay}s" dur="{dur}s" fill="freeze"/>'
        f'<animateTransform attributeName="transform" type="translate" '
        f'from="{dx},{dy}" to="0,0" '
        f'begin="{delay}s" dur="{dur}s" fill="freeze"/>'
    )
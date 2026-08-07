# =============================================================================
# render_heatmap_svg.py — data/contributions.json -> contrib-heatmap.svg
# 53-week × 7-day grid, diagonal column-wave reveal animation (plays once).
# =============================================================================
import json
import sys
from datetime import date, timedelta
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import theme
from utils import repo_path, heatmap_col_delay

# ---------------------------------------------------------------------------
DATA_FILE = repo_path("data", "contributions.json")
OUTPUT    = repo_path("contrib-heatmap.svg")

# Layout
COLS       = 53          # weeks
ROWS       = 7           # days per week
CELL       = 14          # px per cell (square)
GAP        = 3           # px gap between cells
GRID_X     = 44          # left margin (room for day labels)
GRID_Y     = 22          # top margin (room for month labels)
LEGEND_Y_OFF = 16        # px below grid bottom for legend strip

CELL_STEP  = CELL + GAP  # 17 px per cell+gap

WEEK_LABELS   = ["Mon", "Wed", "Fri"]   # only odd rows labelled
WEEK_ROWS     = [0, 2, 4]              # 0=Mon,1=Tue,… 6=Sun

W = theme.HEATMAP_W
H = theme.HEATMAP_H
# ---------------------------------------------------------------------------


def level(count: int) -> int:
    """Map contribution count to palette index 0–5."""
    if count == 0:   return 0
    if count <= 3:   return 1
    if count <= 9:   return 2
    if count <= 19:  return 3
    if count <= 49:  return 4
    return 5


def build_grid(daily: dict[str, int]) -> list[list[int]]:
    """Return a 53-col × 7-row grid of palette indices.

    Column 0 = oldest week (53 weeks ago), Column 52 = this week.
    Row 0 = Monday, Row 6 = Sunday.
    """
    today = date.today()
    # Start at the Monday of the week 52 weeks back
    start = today - timedelta(weeks=52)
    # Align to Monday (weekday() == 0)
    start -= timedelta(days=start.weekday())

    grid = [[0] * ROWS for _ in range(COLS)]
    for col in range(COLS):
        for row in range(ROWS):
            d = start + timedelta(weeks=col, days=row)
            if d <= today:
                cnt = daily.get(d.isoformat(), 0)
                grid[col][row] = level(cnt)
    return grid


def month_labels(daily: dict[str, int]) -> list[tuple[int, str]]:
    """Return list of (col_index, 'Mon') labels for month boundaries."""
    today = date.today()
    start = today - timedelta(weeks=52)
    start -= timedelta(days=start.weekday())

    labels = []
    seen_months = set()
    for col in range(COLS):
        d = start + timedelta(weeks=col)
        month_key = (d.year, d.month)
        if month_key not in seen_months:
            seen_months.add(month_key)
            labels.append((col, d.strftime("%b")))
    return labels


def render(grid, stats: dict, month_lbls) -> str:
    palette  = theme.HEATMAP_PALETTE
    fs       = theme.FONT_SIZE_HEATMAP
    font     = theme.FONT_UI

    parts = []
    parts.append(
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{W}" height="{H}" viewBox="0 0 {W} {H}">\n'
    )

    # ---- Background --------------------------------------------------------
    parts.append(
        f'<rect width="{W}" height="{H}" rx="12" '
        f'fill="{theme.WINDOW}" stroke="{theme.BORDER}" stroke-width="1"/>'
    )

    # ---- Month labels (top) ------------------------------------------------
    for col, month_name in month_lbls:
        mx = GRID_X + col * CELL_STEP
        parts.append(
            f'<text x="{mx}" y="{GRID_Y - 4}" '
            f'font-family="{font}" font-size="{fs}" fill="{theme.GRAY}">'
            f'{month_name}</text>'
        )

    # ---- Day-of-week labels (left) -----------------------------------------
    day_names = ["Mon", "", "Wed", "", "Fri", "", "Sun"]
    for row, label in enumerate(day_names):
        if label:
            ly = GRID_Y + row * CELL_STEP + CELL - 2
            parts.append(
                f'<text x="{GRID_X - 6}" y="{ly}" '
                f'font-family="{font}" font-size="{fs}" '
                f'fill="{theme.GRAY}" text-anchor="end">{label}</text>'
            )

    # ---- Heat cells (diagonal wave reveal) ---------------------------------
    for col in range(COLS):
        for row in range(ROWS):
            lvl   = grid[col][row]
            color = palette[lvl]
            cx    = GRID_X + col * CELL_STEP
            cy    = GRID_Y + row * CELL_STEP
            d     = heatmap_col_delay(col, row)

            parts.append(
                f'<rect x="{cx}" y="{cy}" width="{CELL}" height="{CELL}" '
                f'rx="3" fill="{color}" opacity="0">'
                f'<animate attributeName="opacity" from="0" to="1" '
                f'begin="{d}s" dur="0.18s" fill="freeze"/>'
                f'</rect>'
            )

    # ---- Legend (bottom-left) ----------------------------------------------
    legend_y = GRID_Y + ROWS * CELL_STEP + LEGEND_Y_OFF
    parts.append(
        f'<text x="{GRID_X}" y="{legend_y}" '
        f'font-family="{font}" font-size="{fs}" fill="{theme.GRAY}">Less</text>'
    )
    lx = GRID_X + 30
    for lvl, color in enumerate(palette):
        parts.append(
            f'<rect x="{lx + lvl * (CELL + 2)}" y="{legend_y - CELL + 2}" '
            f'width="{CELL}" height="{CELL}" rx="3" fill="{color}"/>'
        )
    more_x = lx + len(palette) * (CELL + 2) + 4
    parts.append(
        f'<text x="{more_x}" y="{legend_y}" '
        f'font-family="{font}" font-size="{fs}" fill="{theme.GRAY}">More</text>'
    )

    # ---- Stats footer (right side) -----------------------------------------
    stat_items = [
        f'Active days: {stats.get("total_active_days", 0)}',
        f'Current streak: {stats.get("current_streak", 0)} days',
        f'Longest streak: {stats.get("longest_streak", 0)} days',
        f'Best day: level {stats.get("best_day", {}).get("level", 0)}',
    ]
    stats_x = W - 16
    for i, label in enumerate(stat_items):
        parts.append(
            f'<text x="{stats_x}" y="{legend_y - (len(stat_items) - 1 - i) * 14}" '
            f'font-family="{font}" font-size="{fs}" '
            f'fill="{theme.GRAY}" text-anchor="end">{label}</text>'
        )

    parts.append("</svg>")
    return "\n".join(parts)


def main():
    if not DATA_FILE.exists():
        print(f"ERROR: {DATA_FILE} not found. Run fetch_contributions.py first.")
        sys.exit(1)

    payload = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    daily   = payload.get("daily", {})
    stats   = payload.get("stats", {})

    grid       = build_grid(daily)
    month_lbls = month_labels(daily)
    svg_text   = render(grid, stats, month_lbls)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(svg_text, encoding="utf-8")
    print(f"contrib-heatmap.svg -> {OUTPUT}")


if __name__ == "__main__":
    main()

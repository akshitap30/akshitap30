# =============================================================================
# theme.py — single source of truth for all colors, fonts, dims, timing
# Every other script imports from here; nothing is hardcoded elsewhere.
# =============================================================================

# --------------- Color palette -----------------------------------------------
WINDOW    = "#0d1117"
TITLE     = "#161b22"
BORDER    = "#30363d"
TEXT      = "#c9d1d9"
BLUE      = "#58a6ff"
GREEN     = "#7ee787"
RED       = "#ff5f56"
YELLOW    = "#ffbd2e"
LIME      = "#27c93f"
GRAY      = "#8b949e"
DARK_BG   = "#111827"   # inner panel background

# ASCII portrait monochrome fill (single color — avoids per-char noise)
ASCII_FILL = "#c9d1d9"

# --------------- ASCII glyph ramp -------------------------------------------
# Ordered light (sparse) → dark (dense).
# Leading space maps pure-white background pixels → invisible (nothing drawn).
RAMP = " .`:-=+*cs#%@"

# --------------- Heatmap palette (GitHub-style) ------------------------------
HEATMAP_PALETTE = [
    "#161b22",   # 0 contributions  (empty)
    "#0e4429",   # 1–3
    "#006d32",   # 4–9
    "#26a641",   # 10–19
    "#39d353",   # 20–49
    "#69f0a0",   # 50+
]

# --------------- Typography --------------------------------------------------
FONT_MONO   = "Consolas, 'Courier New', monospace"
FONT_UI     = "monospace"

FONT_SIZE_PROMPT   = 19    # akshita@github prompt line
FONT_SIZE_COMMAND  = 19    # neofetch command chars
FONT_SIZE_ASCII    = 10    # glyph size in SVG (matches line_height)
FONT_SIZE_INFO     = 17    # neofetch rows
FONT_SIZE_HEATMAP  = 11    # heatmap labels

# --------------- Canvas dimensions ------------------------------------------
PORTRAIT_W    = 560   # avi-ascii.svg total width
PORTRAIT_H    = 630   # avi-ascii.svg total height

INFO_W        = 560   # info-card.svg width (same as portrait → side-by-side)
INFO_H        = 360   # info-card.svg height

HEATMAP_W     = 1120  # contrib-heatmap.svg width  (= PORTRAIT_W + INFO_W)
HEATMAP_H     = 175   # contrib-heatmap.svg height

# ASCII grid resolution
ASCII_COLS    = 100   # chars wide
ASCII_LINE_H  = 10    # px per row in SVG

# --------------- Animation timing -------------------------------------------
# Portrait: horizontal clip-path wipe, row-by-row top→bottom
ASCII_ROW_STAGGER  = 0.03   # seconds between each row starting
ASCII_WIPE_DUR     = 0.35   # seconds for each row to wipe across

# Info card: fade+slide per line
INFO_FADE_DUR      = 0.25   # seconds per line fade
INFO_LINE_STAGGER  = 0.08   # seconds between lines

# Heatmap: diagonal column reveal
HEATMAP_COL_STAGGER = 0.012  # seconds between each column diagonal wave

# Typing animation for command chars
TYPING_START  = 0.4    # seconds after SVG load before first char appears
TYPING_STAGGER = 0.06  # seconds between each character
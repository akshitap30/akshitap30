# =============================================================================
# ascii.py — image -> character grid -> glyph ramp
# All constants come from theme.py — nothing hardcoded here.
# =============================================================================
import sys
from pathlib import Path
from html import escape

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from PIL import Image
import theme


class AsciiImage:
    """Downsample an image to a character grid using theme.RAMP.

    Uses monochrome fill only (theme.ASCII_FILL) — no per-character color,
    which avoids the 'noisy portrait' anti-pattern.
    """

    def __init__(self, image_path, width: int = None):
        self.image_path = Path(image_path)
        self.width = width or theme.ASCII_COLS
        self._rows: list[str] = []
        self._prepare()

    def _prepare(self):
        img = Image.open(self.image_path).convert("L")
        w, h = img.size
        aspect = h / w
        height = int(self.width * aspect * 0.55)
        img = img.resize((self.width, height), Image.LANCZOS)
        pixels = img.load()

        # theme.RAMP: " .`:-=+*cs#%@"  — light (space=transparent) → dark (dense)
        ramp = theme.RAMP
        ramp_len = len(ramp) - 1

        for y in range(height):
            row = ""
            for x in range(self.width):
                brightness = pixels[x, y]          # 0=black, 255=white
                idx = int(brightness / 255 * ramp_len)
                row += ramp[idx]
            self._rows.append(row)

    def resize(self, width: int) -> "AsciiImage":
        """Return a new AsciiImage re-sampled at `width` columns."""
        return AsciiImage(self.image_path, width=width)

    def rows(self) -> list[str]:
        return self._rows

    def render(
        self,
        x: int,
        y: int,
        font_size: int = None,
        line_height: int = None,
        color: str = None,
        delay: float = 0.8,
    ) -> str:
        """Generate SVG text elements with per-row clip-path wipe reveal.

        Uses theme constants for all styling; color defaults to ASCII_FILL.
        Animation plays once and freezes (fill='freeze').
        """
        fs     = font_size   or theme.FONT_SIZE_ASCII
        lh     = line_height or theme.ASCII_LINE_H
        fill   = color       or theme.ASCII_FILL
        font   = theme.FONT_MONO
        wipe_dur = theme.ASCII_WIPE_DUR
        stagger  = theme.ASCII_ROW_STAGGER
        clip_w = int(self.width * fs * 0.62 + 20)

        parts = []
        for i, row in enumerate(self._rows):
            row_esc = escape(row)
            d = round(delay + i * stagger, 4)
            cy = y + i * lh

            parts.append(
                f"<g>"
                f"<clipPath id=\"aclip{i}\">"
                f"<rect x=\"{x}\" y=\"{cy - lh + 1}\" width=\"0\" height=\"{lh}\">"
                f"<animate attributeName=\"width\""
                f" from=\"0\" to=\"{clip_w}\""
                f" begin=\"{d}s\" dur=\"{wipe_dur}s\" fill=\"freeze\"/>"
                f"</rect>"
                f"</clipPath>"
                f"<text clip-path=\"url(#aclip{i})\""
                f" x=\"{x}\" y=\"{cy}\""
                f" font-family=\"{font}\""
                f" font-size=\"{fs}\""
                f" fill=\"{fill}\">{row_esc}</text>"
                f"</g>"
            )

        return "\n".join(parts)


# Backward-compat alias so both old (ASCIIArt) and new (AsciiImage) names work.
ASCIIArt = AsciiImage
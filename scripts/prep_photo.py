# =============================================================================
# prep_photo.py — raw photo -> source-prepped.png
# Pipeline: background removal (rembg) + white composite + CLAHE contrast.
# Run once per photo change; NOT part of daily cron.
# =============================================================================
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from utils import repo_path

if len(sys.argv) != 2:
    print("Usage: python scripts/prep_photo.py <input_image>")
    sys.exit(1)

from rembg import remove
from PIL import Image
import cv2
import numpy as np

input_path = Path(sys.argv[1])
if not input_path.is_absolute():
    input_path = repo_path(sys.argv[1])

# Background removal
img = Image.open(input_path).convert("RGBA")
img = remove(img)

# Composite onto pure white
background = Image.new("RGBA", img.size, (255, 255, 255, 255))
background.paste(img, mask=img.getchannel("A"))
background = background.convert("RGB")

# CLAHE contrast boost
arr = np.array(background)
gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
gray = clahe.apply(gray)

output = repo_path("source-prepped.png")
Image.fromarray(gray).save(output)
print(f"source-prepped.png -> {output}")
from html import escape
from pathlib import Path
from utils import REPO_ROOT


class SVG:
    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.parts = []

        self.parts.append(
            f'''<?xml version="1.0" encoding="UTF-8"?>
<svg
xmlns="http://www.w3.org/2000/svg"
width="{width}"
height="{height}"
viewBox="0 0 {width} {height}">
'''
        )

    def finish(self):
        self.parts.append("</svg>")

    def save(self, filename):

        self.finish()

        path = Path(filename)
        if not path.is_absolute():
            path = REPO_ROOT / path

        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(self.parts))

    def raw(self, text):

        self.parts.append(text)

    def rect(
        self,
        x,
        y,
        w,
        h,
        fill,
        radius=0,
        stroke=None,
        stroke_width=1,
    ):

        s = f'''
<rect
x="{x}"
y="{y}"
width="{w}"
height="{h}"
rx="{radius}"
fill="{fill}"
'''

        if stroke:

            s += f'''
stroke="{stroke}"
stroke-width="{stroke_width}"
'''

        s += "/>"

        self.parts.append(s)

    def circle(
        self,
        cx,
        cy,
        r,
        fill,
    ):

        self.parts.append(
            f'''
<circle
cx="{cx}"
cy="{cy}"
r="{r}"
fill="{fill}"/>
'''
        )

    def text(
        self,
        x,
        y,
        value,
        size=16,
        color="#ffffff",
        family="monospace",
        weight="normal",
        anchor="start",
    ):

        value = escape(str(value))

        self.parts.append(
            f'''
<text
x="{x}"
y="{y}"
font-family="{family}"
font-size="{size}"
font-weight="{weight}"
text-anchor="{anchor}"
fill="{color}">
{value}
</text>
'''
        )

    def animated_text(
        self,
        x,
        y,
        value,
        delay,
        size=16,
        color="#ffffff",
        family="monospace",
        weight="normal",
    ):

        value = escape(str(value))

        self.parts.append(
            f'''
<g opacity="0">

<animate
attributeName="opacity"
from="0"
to="1"
begin="{delay}s"
dur="0.25s"
fill="freeze"/>

<animateTransform
attributeName="transform"
type="translate"
from="0,8"
to="0,0"
begin="{delay}s"
dur="0.25s"
fill="freeze"/>

<text
x="{x}"
y="{y}"
font-family="{family}"
font-size="{size}"
font-weight="{weight}"
fill="{color}">
{value}
</text>

</g>
'''
        )
    def group_start(self, opacity=1):

        self.parts.append(f'<g opacity="{opacity}">')

    def group_end(self):

        self.parts.append("</g>")
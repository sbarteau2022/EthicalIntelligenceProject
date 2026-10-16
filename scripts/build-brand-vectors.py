#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["fonttools[woff]>=4.60,<5"]
# ///
"""Generate editable brand masters and font-independent wordmark outlines."""

from pathlib import Path
from xml.sax.saxutils import escape
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "public/assets/brand"
FONTS = ASSETS / "fonts"
LOGOS = ASSETS / "logos"
LOGOS.mkdir(parents=True, exist_ok=True)

ATOMA = '<path d="M5 55 27 9h10l22 46H45L32 27 19 55H5Z" fill="{ink}"/><path d="M25 39h20l5 10H20l5-10Z" fill="{accent}"/>'
GRANT = '<path d="m42 10 6 6-7 7-5-4H24l-7 7v14l7 7h12v-9h-9v-9h19v27H21L7 43V23l14-13h21Z" fill="{ink}"/><path d="M51 10h9v46h-9z" fill="{accent}"/>'
font = TTFont(FONTS / "Geist-Variable.ttf", recalcTimestamp=False)
font = instantiateVariableFont(font, {"wght": 570}, inplace=False)
glyphs = font.getGlyphSet()
cmap = font.getBestCmap()
units = font["head"].unitsPerEm


def outline(text, x, y, size, fill, tracking=0):
    paths = []
    cursor = x
    scale = size / units
    for character in text:
        name = cmap[ord(character)]
        pen = SVGPathPen(glyphs)
        glyphs[name].draw(pen)
        d = pen.getCommands()
        if d:
            paths.append(f'<path d="{d}" transform="translate({cursor:.4f} {y}) scale({scale:.6f} {-scale:.6f})" fill="{fill}"/>')
        cursor += font["hmtx"][name][0] * scale + tracking
    return "".join(paths)


def svg(body, width, height, title):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img"><title>{escape(title)}</title>{body}</svg>\n'


for name, geometry, label in [("atoma", ATOMA, "Atoma Engineering"), ("grant-intelligence", GRANT, "Grant Intelligence")]:
    for variant, ink, accent in [("color", "#151D29", "#2F5BEA"), ("ink", "#151D29", "#151D29"), ("white", "#F2F1EB", "#C8D8FC")]:
        mark = geometry.format(ink=ink, accent=accent)
        (LOGOS / f"{name}-mark-{variant}.svg").write_text(svg(mark, 64, 64, label), encoding="utf-8")
        if name == "atoma":
            text = outline("ATOMA", 83, 35, 26, ink, 3.6) + outline("ENGINEERING", 84, 53, 10, ink, 2.25)
            width = 245
        else:
            text = outline("GRANT", 82, 31, 19, ink, 2.4) + outline("INTELLIGENCE", 83, 51, 13, ink, 1.3)
            width = 235
        (LOGOS / f"{name}-wordmark-{variant}.svg").write_text(svg(mark + text, width, 64, label), encoding="utf-8")

# This shared product asset is consumed by the existing customer UI.
(ROOT / "public/assets/grant-intelligence-mark.svg").write_text(
    (LOGOS / "grant-intelligence-mark-white.svg").read_text(encoding="utf-8"), encoding="utf-8")

for filename in ["Geist-Variable.ttf", "InstrumentSerif-Regular.ttf", "InstrumentSerif-Italic.ttf"]:
    source = TTFont(FONTS / filename, recalcTimestamp=False)
    source.flavor = "woff2"
    source.save(FONTS / filename.replace(".ttf", ".woff2"))

blue = "#2F5BEA"
ink = "#151D29"
paper = "#F2F1EB"
for name, headline, subtitle in [
    ("atoma", "Thoughtful engineering.", "Useful intelligence."),
    ("grant-intelligence", "Find the signal.", "Understand the evidence."),
]:
    wordmark = (LOGOS / f"{name}-wordmark-color.svg").read_text(encoding="utf-8")
    inner = wordmark.split("</title>", 1)[1].rsplit("</svg>", 1)[0]
    body = f'<rect width="1200" height="630" fill="{paper}"/><path d="M0 588h1200" stroke="#B8C1CB"/>'
    body += f'<g transform="translate(76 52) scale(1.15)">{inner}</g>'
    body += outline(headline, 76, 315, 67, ink, -1.5)
    body += outline(subtitle, 76, 402, 62, blue, -1.4)
    body += outline("ATOMA ENGINEERING / 2026", 78, 552, 14, "#5C6675", 2)
    body += f'<g transform="translate(1025 74) scale(1.65)">{(ATOMA if name == "atoma" else GRANT).format(ink="#D7DBDC",accent="#C8D8FC")}</g>'
    (ASSETS / f"{name}-social-1200x630.svg").write_text(svg(body, 1200, 630, f"{headline} {subtitle}"), encoding="utf-8")

favicon = '<rect width="64" height="64" rx="14" fill="#F2F1EB"/>' + f'<g transform="translate(7 7) scale(.78)">{ATOMA.format(ink=ink,accent=blue)}</g>'
(ASSETS / "atoma-favicon.svg").write_text(svg(favicon, 64, 64, "Atoma Engineering"), encoding="utf-8")
board = '<rect width="1600" height="1100" fill="#F2F1EB"/>'
board += outline("ATOMA ENGINEERING / DESIGN EDITION 01", 70, 68, 14, "#5C6675", 2)
board += outline("Thoughtful engineering. Useful intelligence.", 70, 150, 47, ink, -1)
board += '<path d="M70 192h1460M70 655h1460M70 1004h1460" stroke="#B8C1CB"/>'
for name, x, label in [("atoma", 70, "01 / THE STUDIO"), ("grant-intelligence", 830, "02 / THE PRODUCT")]:
    master = (LOGOS / f"{name}-wordmark-color.svg").read_text(encoding="utf-8")
    inner = master.split("</title>", 1)[1].rsplit("</svg>", 1)[0]
    board += outline(label, x, 251, 13, "#5C6675", 1.6)
    board += f'<g transform="translate({x} 320) scale(2.5)">{inner}</g>'
    board += outline("INTELLIGENCE IN SERVICE OF PEOPLE" if name == "atoma" else "FIND THE SIGNAL. UNDERSTAND THE EVIDENCE.", x, 565, 12, "#5C6675", .8)
board += outline("A CONSIDERED PALETTE", 70, 711, 13, "#5C6675", 1.7)
for index, (color, label) in enumerate([(paper,"EGGSHELL"),(ink,"INK"),(blue,"STUDIO BLUE"),("#B8C1CB","TITANIUM"),("#C8D8FC","PALE BLUE")]):
    x = 70 + index * 300
    board += f'<rect x="{x}" y="754" width="260" height="115" rx="3" fill="{color}" stroke="#B8C1CB"/>'
    board += outline(label, x, 901, 12, "#5C6675", 1)
    board += outline(color.upper(), x, 927, 13, ink)
board += outline("THE ETHICAL INTELLIGENCE PROJECT", 70, 1051, 13, "#5C6675", 1.6)
board += outline("ATOMA ENGINEERING / 2026", 1200, 1051, 12, "#5C6675", .7)
(ASSETS / "atoma-brand-board.svg").write_text(svg(board, 1600, 1100, "Atoma Engineering design package overview"), encoding="utf-8")
print("Built 12 outlined logo masters, 3 WOFF2 fonts, social masters, brand board, and favicon.")

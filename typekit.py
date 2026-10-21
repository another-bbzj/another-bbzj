"""Generate artwork using ONLY the profile's original font subsets/signature.

Python 3.10+, fonttools, brotli. Run from any directory: python gen.py.
Missing glyphs fail explicitly, so the original typography is never substituted.
"""
from pathlib import Path
from html import escape
import io, json, base64, re
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / 'assets'
ASSETS.mkdir(exist_ok=True)
FONTS = {}
for key, subsets in json.loads((ROOT/'design/typefaces.json').read_text()).items():
    FONTS[key] = []
    for encoded in subsets:
        font = TTFont(io.BytesIO(base64.b64decode(encoded)))
        FONTS[key].append((font, font.getGlyphSet(), font.getBestCmap()))
SIGNATURE = (ROOT/'design/signature.svg').read_text(encoding='utf-8')
SIGNATURE = SIGNATURE[SIGNATURE.index('>')+1:SIGNATURE.rindex('</svg>')]

P = {}
def text(value, x, y, size=20, color=None, face='sans', spacing=0):
    result = []
    for char in value:
        family = 'cjk' if ord(char) > 255 else face
        candidates = [item for item in FONTS[family] if ord(char) in item[2]]
        if not candidates:
            raise ValueError(f'Original {family} font missing character: {char!r}')
        f, glyphs, cmap = candidates[0]
        name = cmap[ord(char)]
        scale = size / f['head'].unitsPerEm
        pen = SVGPathPen(glyphs)
        glyphs[name].draw(pen)
        if pen.getCommands():
            result.append(f'<path d="{pen.getCommands()}" transform="translate({x:.3f} {y}) scale({scale:.6f} {-scale:.6f})"/>')
        x += glyphs[name].width * scale + spacing
    return f'<g fill="{color or P["ink"]}" aria-label="{escape(value, quote=True)}">' + ''.join(result) + '</g>'

def line(x1,y1,x2,y2,color=None,width=1,extra=''):
    return f'<path d="M{x1} {y1}L{x2} {y2}" fill="none" stroke="{color or P["edge"]}" stroke-width="{width}" {extra}/>'

def rect(x,y,w,h,fill=None,stroke=None,r=12,extra=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill or P["panel"]}" stroke="{stroke or P["edge"]}" {extra}/>'

def circle(x,y,r,color,extra=''):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}" {extra}/>'


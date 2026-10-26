"""Builds kol/index.html (one self-contained page) from source/kol-page.html.

Run from anywhere:  python3 source/build.py
Needs:              pip install fonttools brotli

What it embeds:
  - the two Special Gothic Condensed One font files (latin + latin-ext) as base64, with the
    unicode-range worked out from the real font tables, so letters the font lacks fall back cleanly;
  - the list of covered letters (used to warn about letters that fall back);
  - source/bg.png: the invitation exported from Figma with the name layer at opacity 0
    (keep the panel; do not use visible=false, it collapses the auto-layout).
To change the design: re-export bg.png at 1x (1080x1350) and run this script again.
"""
import base64, os, re
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, 'fonts')
OUT = os.path.join(HERE, '..', 'kol', 'index.html')
TITLE_DESC = 'Type a guest name and get the UNION press conference invitation as a picture, ready to post.'


def ranges(cps):
    cps = sorted(cps)
    out, start, prev = [], None, None
    for c in cps:
        if start is None:
            start = prev = c
        elif c == prev + 1:
            prev = c
        else:
            out.append((start, prev)); start = prev = c
    if start is not None:
        out.append((start, prev))
    return out


def fmt_css(rs):
    return ','.join('U+%04X' % a if a == b else 'U+%04X-%04X' % (a, b) for a, b in rs)


def fmt_js(rs):
    return ','.join(str(a) if a == b else '%d-%d' % (a, b) for a, b in rs)


latin = os.path.join(FONTS, 'special-gothic-condensed-one-latin-400-normal.woff2')
ext = os.path.join(FONTS, 'special-gothic-condensed-one-latin-ext-400-normal.woff2')
cm_latin = {c for c in TTFont(latin).getBestCmap().keys() if c > 0x1F}
cm_ext = {c for c in TTFont(ext).getBestCmap().keys() if c > 0x1F} - cm_latin
faces = []
for path, cps in ((latin, cm_latin), (ext, cm_ext)):
    b64 = base64.b64encode(open(path, 'rb').read()).decode()
    faces.append("@font-face{font-family:'SGCO';font-style:normal;font-weight:400;font-display:block;"
                 "src:url(data:font/woff2;base64,%s) format('woff2');unicode-range:%s;}" % (b64, fmt_css(ranges(cps))))
covered = fmt_js(ranges(cm_latin | cm_ext))

bg = 'data:image/png;base64,' + base64.b64encode(open(os.path.join(HERE, 'bg.png'), 'rb').read()).decode()

page = open(os.path.join(HERE, 'kol-page.html'), encoding='utf-8').read()
page = page.replace('@@FONT_FACES@@', '\n'.join(faces)).replace('@@COVERED@@', covered).replace('@@BG@@', bg)

title = re.search(r'<title>.*?</title>', page, re.S).group(0)
body = page.replace(title, '', 1)
html = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
        '<meta name="robots" content="noindex,nofollow">\n'
        '<meta name="color-scheme" content="light dark">\n'
        '<meta name="description" content="' + TITLE_DESC + '">\n'
        + title + '\n</head>\n<body>\n' + body + '\n</body>\n</html>\n')
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, 'w', encoding='utf-8').write(html)
print('built kol/index.html,', len(html), 'bytes; covered code points', len(cm_latin | cm_ext))

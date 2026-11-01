from pathlib import Path
import re,base64,io
from PIL import Image
brand=Path('branding.js').read_text()
m=re.search(r'OFFICIAL_LOGO_SOURCE\s*=\s*"data:image/jpeg;base64,([^"]+)',brand)
if not m: raise RuntimeError("Approved official logo is missing")
logo=Image.open(io.BytesIO(base64.b64decode(m.group(1)))).convert('RGBA')
logo.thumbnail((420,420))
import numpy as np
from collections import deque
a=np.array(logo); rgb=a[:,:,:3]; h,w=rgb.shape[:2]
target=np.median(np.array([rgb[0,0],rgb[0,-1],rgb[-1,0],rgb[-1,-1]]),axis=0)
mask=(np.max(abs(rgb.astype('int16')-target),axis=2)<25)
seen=np.zeros((h,w),bool);q=deque()
for y in range(h):
 for x in (0,w-1):
  if mask[y,x] and not seen[y,x]:seen[y,x]=True;q.append((y,x))
for x in range(w):
 for y in (0,h-1):
  if mask[y,x] and not seen[y,x]:seen[y,x]=True;q.append((y,x))
while q:
 y,x=q.popleft()
 for yy,xx in ((y-1,x),(y+1,x),(y,x-1),(y,x+1)):
  if 0<=yy<h and 0<=xx<w and mask[yy,xx] and not seen[yy,xx]:seen[yy,xx]=True;q.append((yy,xx))
a[seen,3]=0
buff=io.BytesIO();Image.fromarray(a).save(buff,format='PNG')
data=base64.b64encode(buff.getvalue()).decode()
svg='''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1248" height="1248" viewBox="0 0 1248 1248">
<rect width="1248" height="1248" fill="#EDE4D7"/>
<g id="logo" data-layer="movable" transform="translate(20,16)"><image width="250" height="250" xlink:href="data:image/png;base64,LOGODATA"/></g>
<g id="header" data-layer="movable" fill="#091D40" font-family="Arial,sans-serif" text-anchor="middle">
<text x="685" y="96" font-size="73" font-weight="900" textLength="770" lengthAdjust="spacingAndGlyphs">BASEBALL JERSEY</text>
<path d="M295 159H372 M1000 159H1083" stroke="#091D40" stroke-width="3"/>
<text x="682" y="174" font-size="43" font-weight="900">MEASUREMENT GUIDE</text></g>
<g id="brand-right" data-layer="movable"><rect x="1082" y="29" width="150" height="157" rx="6" fill="#091D40"/>
<g font-family="Arial,sans-serif" text-anchor="middle" fill="white"><text x="1157" y="58" font-size="17" font-weight="bold">THE PORKY YORKIE</text><text x="1157" y="98" font-size="20" font-style="italic">Curated Finds,</text><text x="1157" y="130" font-size="17" font-style="italic">Vintage &amp; Beyond.</text><text x="1157" y="165" font-size="22">★</text></g></g>
<g id="item-size" data-layer="movable" font-family="Arial,sans-serif" fill="#091D40">
<rect x="295" y="206" width="935" height="132" rx="8" fill="none" stroke="#091D40" stroke-width="2.5"/>
<path d="M295 271H1230 M650 271V338 M493 245H1205 M500 313H626" stroke="#091D40" stroke-width="2"/>
<text x="317" y="249" font-weight="900" font-size="26">ITEM NAME:</text>
<text x="317" y="317" font-weight="900" font-size="26">TAGGED SIZE:</text>
<text x="677" y="308" fill="#2445C6" font-size="28">★</text>
<text x="715" y="298" font-size="19">For best fit, please compare the measurements</text>
<text x="715" y="322" font-size="19">below to a similar garment you own.</text></g>
<g id="jersey" data-layer="movable" fill="none" stroke="#1C2934" stroke-width="3.2" stroke-linejoin="round">
<path d="M505 384 L551 360 Q623 389 697 360 L743 384 L837 477 L797 533 L746 492 L745 820 Q625 855 505 820 L504 492 L453 533 L413 477 Z"/>
<path d="M551 360 Q586 407 621 421 Q661 407 697 360 M576 373 Q591 412 620 435 M676 374 Q654 412 633 435 M618 429V843 M635 429V843 M505 813 Q625 843 745 813" />
<path d="M452 530L416 477 M797 530L834 477" opacity=".6"/>
<circle cx="626" cy="465" r="4"/><circle cx="626" cy="518" r="4"/><circle cx="626" cy="571" r="4"/><circle cx="626" cy="624" r="4"/><circle cx="626" cy="677" r="4"/><circle cx="626" cy="730" r="4"/></g>
<g id="pit-arrow" data-layer="movable" stroke="#2449E0" stroke-width="4" fill="#2449E0">
<path d="M504 545H745"/><path d="M504 545l15 -9v18z M745 545l-15 -9v18z"/></g>
<g id="length-arrow" data-layer="movable" stroke="#2449E0" stroke-width="4" fill="#2449E0">
<path d="M858 367V833"/><path d="M858 367l-9 16h18z M858 833l-9 -16h18z"/>
<path d="M805 367H901 M806 833H901" stroke-width="2" stroke-dasharray="5 4"/></g>
<g id="measurement-labels" data-layer="movable" font-family="Arial,sans-serif" fill="#091D40" text-anchor="middle">
<text x="275" y="557" font-size="29" font-weight="900">PIT TO PIT</text><text x="275" y="745" font-size="24">____ in.</text>
<text x="997" y="557" font-size="29" font-weight="900">LENGTH</text><text x="997" y="745" font-size="24">____ in.</text></g>
<g id="how-to-measure" data-layer="movable" font-family="Arial,sans-serif" fill="#091D40">
<rect x="55" y="902" width="1140" height="214" rx="14" stroke="#091D40" stroke-width="2.5" fill="none"/>
<path d="M421 910V1112 M801 910V1112" stroke="#091D40" stroke-width="2"/>
<rect x="133" y="910" width="230" height="35" rx="5" fill="#091D40"/>
<rect x="491" y="910" width="220" height="35" rx="5" fill="#091D40"/>
<rect x="913" y="910" width="170" height="35" rx="5" fill="#091D40"/>
<g fill="white" font-size="20" font-weight="bold" text-anchor="middle">
<text x="248" y="936">PIT TO PIT</text><text x="601" y="936">LENGTH</text><text x="998" y="936">NOTES</text></g>
<g font-size="18"><text x="83" y="979">Measure straight across the chest</text><text x="83" y="1005">from armpit seam to seam.</text>
<text x="447" y="979">Measure from the top of the shoulder</text><text x="447" y="1005">straight down to the bottom hem.</text>
<text x="832" y="979">• Measurements are taken laid flat.</text><text x="832" y="1011">• All measurements are in inches.</text><text x="832" y="1043">• Allow for ±1/2” variance.</text></g>
<g stroke="#091D40" stroke-width="2.5" fill="none">
<path d="M182 1039 l15 -10 24 10 24 -10 15 10 21 18 -11 17 -14 -9 1 33 -72 0 1 -33 -14 9 -11 -17z"/>
<path d="M536 1039 l15 -10 24 10 24 -10 15 10 21 18 -11 17 -14 -9 1 33 -72 0 1 -33 -14 9 -11 -17z"/></g>
<path d="M190 1070H261 M190 1070l9 -5v10z M261 1070l-9 -5v10z M574 1030V1100 M574 1030l-5 9h10z M574 1100l-5 -9h10z" stroke="#2449E0" stroke-width="3" fill="#2449E0"/></g>
<g id="footer" data-layer="movable"><rect y="1132" width="1248" height="75" fill="#091D40"/>
<g font-family="Arial,sans-serif" fill="white"><text x="25" y="1177" font-size="17">QUALITY FINDS. HONEST MEASUREMENTS.</text>
<text x="624" y="1182" font-size="34" font-weight="900" text-anchor="middle">★ THE PORKY YORKIE ★</text>
<text x="1228" y="1177" font-size="16" text-anchor="end">MEASURED BY HAND. LISTED WITH CARE.</text></g>
<text x="624" y="1237" font-size="20" fill="#091D40" font-family="Arial,sans-serif" text-anchor="middle">All measurements are in inches.</text></g></svg>'''
svg=svg.replace('LOGODATA',data)
Path('guides/baseball_jersey.svg').write_text(svg)
print('SVG groups:',svg.count('data-layer="movable"'),'size:',len(svg))

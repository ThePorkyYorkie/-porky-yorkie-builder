from pathlib import Path
import re,base64,io
from PIL import Image,ImageDraw,ImageFont
p=Path('guides/baseball_jersey.svg')
s=p.read_text()
m=re.search(r'data:image/jpeg;base64,([^"]+)',s)
assert m, 'Missing embedded baseball master'
base=Image.open(io.BytesIO(base64.b64decode(m.group(1)))).convert('RGB')
assert base.size==(1248,1248),base.size
brand=Path('branding.js').read_text()
b=re.search(r"const OFFICIAL_LOGO_SOURCE\\s*=\\s*\\\"data:image/jpeg;base64,([^\\\"]+)",brand)
assert b, 'Official approved logo missing'
logo=Image.open(io.BytesIO(base64.b64decode(b.group(1)))).convert('RGB')
color=(237,228,215)
# Preserve existing bottom instruction boxes and all other guide-specific visual branding.
# Replace the upper-left obsolete badge only.
d=ImageDraw.Draw(base)
d.rectangle((0,0,271,299), fill=color)
# Preserve the exact original logo pixels while making the source paper color transparent
# to eliminate the appearance of an off-color pasted rectangle.
logo.thumbnail((250,255),Image.Resampling.LANCZOS)
from PIL import ImageChops
pix=logo.load()
corners=[pix[0,0],pix[logo.width-1,0],pix[0,logo.height-1],pix[logo.width-1,logo.height-1]]
bg=tuple(sorted(v[i] for v in corners)[len(corners)//2] for i in range(3))
rgba=Image.new('RGBA',logo.size,(0,0,0,0)); op=rgba.load()
for y in range(logo.height):
 for x in range(logo.width):
  r,g,b=pix[x,y]; delta=max(abs(r-bg[0]),abs(g-bg[1]),abs(b-bg[2]))
  # Whitespace removal does not alter the black outline or dog drawing.
  alpha=255 if delta>=30 else int(255*delta/30)
  op[x,y]=(r,g,b,alpha)
base.paste(rgba,(10,8),rgba)
# Remove the two redundant paragraphs and team lettering in the central region;
# recreate the garment as a neutral jersey illustration with the same blue arrows.
d=ImageDraw.Draw(base)
d.rectangle((218,360,1050,930),fill=color)
navy=(9,27,54); blue=(30,57,216)
# Jersey shape and binding: a plain button-front baseball silhouette
outline=[(536,379),(574,357),(630,380),(671,358),(710,379),(774,418),(861,502),(817,559),(766,523),(769,822),(714,840),(625,850),(532,840),(480,822),(484,523),(435,560),(393,502),(476,416)]
d.polygon(outline,fill=color)
d.line(outline+[outline[0]],fill=(40,45,50),width=4,joint='curve')
d.line([(574,357),(603,396),(629,420),(651,397),(671,358)],fill=navy,width=4,joint='curve')
d.line([(609,402),(624,437),(624,844)],fill=navy,width=3)
d.line([(641,403),(638,437),(638,844)],fill=navy,width=3)
for y in (462,511,560,609,658,707,756): d.ellipse((629,y,637,y+8),outline=(70,70,70),width=2)
d.line([(479,822),(530,840),(625,850),(712,840),(768,822)],fill=(75,75,75),width=3)
d.line([(483,521),(435,557),(393,501)],fill=navy,width=3)
d.line([(765,522),(817,555),(861,501)],fill=navy,width=3)
# blue pit-to-pit and length arrows
d.line((482,540,767,540),fill=blue,width=4)
d.polygon([(482,540),(497,531),(497,549)],fill=blue)
d.polygon([(767,540),(752,531),(752,549)],fill=blue)
d.line((897,388,897,833),fill=blue,width=4)
d.polygon([(897,388),(888,404),(906,404)],fill=blue)
d.polygon([(897,833),(888,817),(906,817)],fill=blue)
for y in (388,833): d.line((835,y,930,y),fill=blue,width=2)
def font(sz,bold=True):
 paths=['/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf']
 return ImageFont.truetype(paths[0 if bold else 1],sz)
d.text((225,518),'PIT TO PIT',fill=navy,font=font(23),anchor='mm')
d.text((225,624),'_____ in.',fill=navy,font=font(17),anchor='mm')
d.text((1042,518),'LENGTH',fill=navy,font=font(23),anchor='mm')
d.text((1042,624),'_____ in.',fill=navy,font=font(17),anchor='mm')
# Force background color in formerly white-ish open paper regions, while preserving
# contrast of dark printed elements and bottom diagrams.
# Retain exact existing top title, fit note, and bottom measurement explanations.
buf=io.BytesIO();base.save(buf,format='PNG',optimize=True)
payload=base64.b64encode(buf.getvalue()).decode()
p.write_text('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1248" height="1248" viewBox="0 0 1248 1248"><image width="1248" height="1248" xlink:href="data:image/png;base64,'+payload+'"/></svg>')
assert 'base64' in p.read_text()

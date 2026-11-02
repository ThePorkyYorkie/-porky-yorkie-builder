from PIL import Image, ImageDraw, ImageFilter
from io import BytesIO
from pathlib import Path
import base64,re
from xml.etree import ElementTree as ET
import cv2,numpy as np
p=Path('guides/baseball_jersey.svg')
src=p.read_text()
m=re.search(r'data:image/jpeg;base64,([^"]+)',src)
assert m
im=Image.open(BytesIO(base64.b64decode(m.group(1)))).convert('RGB')
assert im.size==(1248,1248)
a=np.array(im)
# Rebuild unprinted jersey surface with neighboring cloth, preserving panel linework.
mask=np.zeros((1248,1248),np.uint8)
# Isolate lettering and player numeral within body, avoiding sleeve, collar and placket.
# Mask individual lines of lettering at y 470-640 including underline, on left and right chest.
cv2.rectangle(mask,(460,473),(597,640),255,-1)
cv2.rectangle(mask,(646,473),(776,622),255,-1)
# Number on right front
cv2.rectangle(mask,(670,619),(777,699),255,-1)
# Avoid covering edge of breast and center placket.
# Inpaint preserves nearby shirt colour but might soften button areas.
out=cv2.inpaint(a,mask,9,cv2.INPAINT_TELEA)
# Recover the original placket, buttons and surrounding linework exactly, from original.
out[:,597:666]=a[:,597:666]
im=Image.fromarray(out)
d=ImageDraw.Draw(im)
# Remove the duplicated instructional paragraphs ONLY beside the body, using matching plain background
# Restrict to inner column areas, preserving measurement captions and inch blank.
def replace_from_adjacent(x0,y0,x1,y1,sx,sy):
  # smooth fill using adjacent background samples, resized to region
  w=x1-x0;h=y1-y0
  sample=im.crop((sx,sy,sx+w,sy+h))
  im.paste(sample,(x0,y0))
# left explanation and right explanation; surrounding cream is nearly uniform
replace_from_adjacent(202,648,357,752,112,648)
replace_from_adjacent(943,614,1120,773,1040,386)
# Special handling: ensure length label remains from the original
# label is at x948..1042 y574..606; do not touch.
# Make side inch placements close beneath their headings and keep output dynamic overlays available.
# preserve original "in." for builder positions, so leave inch lines.
buf=BytesIO(); im.save(buf,format='PNG',optimize=True)
data=base64.b64encode(buf.getvalue()).decode()
p.write_text('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 1248 1248" width="1248" height="1248"><image width="1248" height="1248" xlink:href="data:image/png;base64,'+data+'"/></svg>')
Path('guides/baseball-review.png').write_bytes(buf.getvalue())
print("OUTPUT",len(buf.getvalue()))

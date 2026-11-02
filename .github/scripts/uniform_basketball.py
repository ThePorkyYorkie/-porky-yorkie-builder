from PIL import Image
from io import BytesIO
from pathlib import Path
import base64,re,numpy as np
def load_svg(path):
 s=Path(path).read_text()
 m=re.search(r'data:image/(?:png|jpeg);base64,([^"]+)',s)
 assert m,path
 return Image.open(BytesIO(base64.b64decode(m.group(1)))).convert('RGB')
base=load_svg('guides/baseball_jersey.svg')
basket=load_svg('guides/basketball_jersey.svg')
assert base.size==basket.size
a=np.array(base)
b=np.array(basket)
# Use the approved Baseball Jersey ONLY for shared header components.
# Never copy the garment area or touch Basketball Jersey wording.
sections=[
 (0,0,271,335),          # official logo, exact
 (970,0,1248,218),       # upper-right navy brand box
 (270,148,968,217),      # MEASUREMENT GUIDE secondary line
 (275,217,1248,355),     # item name, tagged size, star and fit note
]
for x0,y0,x1,y1 in sections:
 b[y0:y1,x0:x1,:]=a[y0:y1,x0:x1,:]
# Single-source fixed elements are exact pixels; garment stays wholly Basketball.
for x0,y0,x1,y1 in sections:
 assert np.array_equal(b[y0:y1,x0:x1],a[y0:y1,x0:x1])
assert np.array_equal(b[370:940,350:1050],np.asarray(basket)[370:940,350:1050])
out=Image.fromarray(b)
buf=BytesIO();out.save(buf,'PNG',optimize=True)
Path('guides/basketball_jersey.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 1248 1248" width="1248" height="1248"><image width="1248" height="1248" xlink:href="data:image/png;base64,'+base64.b64encode(buf.getvalue()).decode()+'"/></svg>')
out.thumbnail((700,700))
out.save('basketball-uniform-review.jpg',quality=84)
print('Verbatim master header components; untouched basketball illustration; preview created')

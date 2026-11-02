from PIL import Image
from io import BytesIO
from pathlib import Path
import base64,re,numpy as np,subprocess
def load_svg(s):
 m=re.search(r'data:image/(?:png|jpeg);base64,([^"]+)',s)
 assert m
 return Image.open(BytesIO(base64.b64decode(m.group(1)))).convert('RGB')
base=load_svg(Path('guides/baseball_jersey.svg').read_text())
ball=load_svg(Path('guides/basketball_jersey.svg').read_text())
assert base.size==ball.size,(base.size,ball.size)
old=subprocess.check_output(['git','show','origin/backup/pre-layered-baseball-2026-11-01:guides/basketball_jersey.svg']).decode()
original=load_svg(old).resize(base.size)
a=np.array(base)
b=np.array(ball)
o=np.array(original)
# Exact shared top: original approved baseball image is the sole source for
# everything from the top through the Tagged Size and fit note.
b[:355,:,:]=a[:355,:,:]
# Garment-only content comes from the separate Basketball Jersey original.
# Only the original basketball headline changes, as a single clean text region.
# The neighboring frame, brand box, note, and form remain approved Baseball master.
x0,x1=275,947
y0,y1=12,152
b[y0:y1,x0:x1,:]=o[y0:y1,x0:x1,:]
out=Image.fromarray(b)
# Invariant check: brand box, official logo, and form must be pixel-identical.
assert np.array_equal(b[:355,:270],a[:355,:270])
assert np.array_equal(b[:355,970:],a[:355,970:])
assert np.array_equal(b[220:355,280:960],a[220:355,280:960])
buf=BytesIO();out.save(buf,'PNG',optimize=True)
text='<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 1248 1248" width="1248" height="1248"><image width="1248" height="1248" xlink:href="data:image/png;base64,'+base64.b64encode(buf.getvalue()).decode()+'"/></svg>'
Path('guides/basketball_jersey.svg').write_text(text)
out.thumbnail((700,700));out.save('basketball-uniform-review.jpg',quality=77)
print('Shared sections pixel-identical; title only modified')

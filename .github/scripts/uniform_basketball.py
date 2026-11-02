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
b[:435,:,:]=a[:435,:,:]
# Garment-only content comes from the separate Basketball Jersey original.
# The headline alone changes. Borrow only original dark lettering, not the
# original basketball background, so the top remains identical.
# Determine letter foreground from dark navy original title text.
x0,x1=277,952
y0,y1=14,147
src=o[y0:y1,x0:x1,:].astype(float)
dst=b[y0:y1,x0:x1,:].astype(float)
# Remove baseball heading text from this rectangle with a locally sampled
# smooth cream backdrop (only title, never other shared masthead elements).
for row in range(y0,y1):
 left=a[row,275,:].astype(float)
 right=a[row,952,:].astype(float)
 xs=np.linspace(0,1,x1-x0)[:,None]
 b[row,x0:x1,:]=np.clip(left*(1-xs)+right*xs,0,255).astype(np.uint8)
# Restore dark letter ink exactly; soft antialias edge from original.
region=b[y0:y1,x0:x1,:].astype(float)
v=np.mean(src,axis=2)
alpha=np.clip((205-v)/135,0,1)
alpha=np.where((src[:,:,2] < src[:,:,0]+30)&(src[:,:,0]<210),alpha,0)
alpha=alpha[:,:,None]
# ink source pixel remains dark and sharp, cream background from master.
b[y0:y1,x0:x1,:]=np.clip(region*(1-alpha)+src*alpha,0,255).astype(np.uint8)
out=Image.fromarray(b)
# Invariant check: brand box, official logo, and form must be pixel-identical.
assert np.array_equal(b[:435,:270],a[:435,:270])
assert np.array_equal(b[:435,970:],a[:435,970:])
assert np.array_equal(b[220:435,280:960],a[220:435,280:960])
buf=BytesIO();out.save(buf,'PNG',optimize=True)
text='<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 1248 1248" width="1248" height="1248"><image width="1248" height="1248" xlink:href="data:image/png;base64,'+base64.b64encode(buf.getvalue()).decode()+'"/></svg>'
Path('guides/basketball_jersey.svg').write_text(text)
out.thumbnail((700,700));out.save('basketball-uniform-review.jpg',quality=77)
print('Shared sections pixel-identical; title only modified')

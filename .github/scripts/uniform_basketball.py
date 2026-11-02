from PIL import Image
from io import BytesIO
from pathlib import Path
import base64,re,numpy as np,subprocess,cv2
def load_svg(s):
 m=re.search(r'data:image/(?:png|jpeg);base64,([^"]+)',s)
 assert m
 return Image.open(BytesIO(base64.b64decode(m.group(1)))).convert('RGB')
base=load_svg(Path('guides/baseball_jersey.svg').read_text())
basket=load_svg(subprocess.check_output(['git','show','origin/main:guides/basketball_jersey.svg']).decode())
assert base.size==basket.size
a=np.asarray(base)
src=np.asarray(basket)
out=a.copy()
# All header, logo, brand panel, tagged size, fit note are ONE common master.
# Keep only the differing garment NAME from existing Basketball Jersey.
out[0:145,271:970,:]=src[0:145,271:970,:]
# Never import the Baseball garment into the Basketball guide.
out[355:,:,:]=src[355:,:,:]
# Remove any Baseball shoulder/neckline ink from the narrow transition zone
# below the common form's lower border. Inpaint individual ink strokes, not
# large rectangular patches or underlying texture.
x0,x1,y0,y1=355,950,325,355
part=out[y0:y1,x0:x1,:].copy()
dark=(np.max(part,axis=2)<180).astype(np.uint8)*255
dark=cv2.dilate(dark,np.ones((3,3),np.uint8),iterations=2)
out[y0:y1,x0:x1,:]=cv2.inpaint(part,dark,4,cv2.INPAINT_TELEA)
# Common master check, and no change below upper guide.
assert np.array_equal(out[145:320,:,:],a[145:320,:,:])
assert np.array_equal(out[355:,:,:],src[355:,:,:])
assert np.array_equal(out[:145,:270,:],a[:145,:270,:])
assert np.array_equal(out[:145,970:,:],a[:145,970:,:])
im=Image.fromarray(out)
b=BytesIO();im.save(b,'PNG',optimize=True)
Path('guides/basketball_jersey.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 1248 1248" width="1248" height="1248"><image width="1248" height="1248" xlink:href="data:image/png;base64,'+base64.b64encode(b.getvalue()).decode()+'"/></svg>')
im.thumbnail((700,700));im.save('basketball-uniform-review.jpg',quality=85)
print('Full header identical to approved master except garment title; garment preserved; preview made')

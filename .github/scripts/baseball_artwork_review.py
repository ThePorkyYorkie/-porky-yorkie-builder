from PIL import Image, ImageDraw, ImageFilter
from io import BytesIO
from pathlib import Path
import base64,re
from xml.etree import ElementTree as ET
import cv2,numpy as np
p=Path('guides/baseball_jersey.svg')
import subprocess
src=subprocess.check_output(['git','show','origin/backup/pre-layered-baseball-2026-11-01:guides/baseball_jersey.svg']).decode()
m=re.search(r'data:image/jpeg;base64,([^"]+)',src)
assert m
im=Image.open(BytesIO(base64.b64decode(m.group(1)))).convert('RGB')
print('original dimensions',im.size)
im=im.resize((1248,1248),Image.Resampling.LANCZOS)
a=np.array(im)
# Restore ink narrowly, never the whole cloth panels.
mask=np.zeros((1248,1248),np.uint8)
# Select dark printed team graphics in their exclusive interior bounding regions.
ink=((a[:,:,0]<130)&(a[:,:,1]<120)&(a[:,:,2]<165)).astype(np.uint8)*255
for x0,y0,x1,y1 in [(464,479,598,644),(649,479,777,627),(673,618,778,705)]:
    mask[y0:y1,x0:x1]=ink[y0:y1,x0:x1]
mask=cv2.dilate(mask,np.ones((3,3),np.uint8),iterations=1)
out=cv2.inpaint(a,mask,4,cv2.INPAINT_TELEA)
im=Image.fromarray(out)
# Inpaint duplicate paragraphs beside artwork only, without erasing labels, arrows or values.
a=np.array(im)
mask=np.zeros((1248,1248),np.uint8)
dark=(np.max(a,axis=2)<170).astype(np.uint8)*255
for x0,y0,x1,y1 in [(202,650,355,750),(946,615,1119,770)]:
    mask[y0:y1,x0:x1]=dark[y0:y1,x0:x1]
mask=cv2.dilate(mask,np.ones((2,2),np.uint8),iterations=1)
im=Image.fromarray(cv2.inpaint(a,mask,3,cv2.INPAINT_TELEA))
buf=BytesIO(); im.save(buf,format='PNG',optimize=True)
data=base64.b64encode(buf.getvalue()).decode()
p.write_text('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 1248 1248" width="1248" height="1248"><image width="1248" height="1248" xlink:href="data:image/png;base64,'+data+'"/></svg>')
Path('guides/baseball-review.png').write_bytes(buf.getvalue())
print("OUTPUT",len(buf.getvalue()))

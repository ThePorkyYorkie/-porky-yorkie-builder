from PIL import Image,ImageDraw,ImageFont
from io import BytesIO
import numpy as np,cv2,base64,re
from pathlib import Path
def image_from_svg(path):
 s=Path(path).read_text()
 m=re.search(r'data:image/(?:jpeg|png);base64,([^"]+)',s)
 assert m,path
 return Image.open(BytesIO(base64.b64decode(m.group(1)))).convert('RGB')
orig=image_from_svg('guides/basketball_jersey.svg')
baseball=image_from_svg('guides/baseball_jersey.svg').resize(orig.size)
a=np.asarray(orig).copy(); out=a.copy()
sample=a[783:850,480:690]
for x0,y0,x1,y1 in [(485,509,744,773),(728,850,799,898)]:
 for y in range(y0,y1):
  for x in range(x0,x1):
   edge=min(x-x0,x1-1-x,y-y0,y1-1-y)
   blend=max(0,min(1,edge/2))
   px=sample[(y-y0)%67,(x-x0)%210]
   out[y,x]=(1-blend)*a[y,x]+blend*px
out[608:624,414:440]=a[608:624,414:440]
out[608:624,784:814]=a[608:624,784:814]
cv2.line(out,(440,615),(784,615),(29,43,229),2)
im=Image.fromarray(out);d=ImageDraw.Draw(im)
for x0,y0,x1,y1 in [(255,649,399,746),(880,605,1079,756),(300,754,390,784),(890,760,990,794)]:
 for y in range(y0,y1):
  pix=a[y,1100:1150];pix=pix[(pix[:,0]>220)&(pix[:,1]>210)&(pix[:,2]>190)]
  c=tuple(np.median(pix,axis=0).astype(int)) if len(pix) else (250,246,237)
  d.line((x0,y,x1,y),fill=c)
d.rectangle((876,771,892,789),fill=(248,240,229))
navy=(7,27,59)
f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',20)
d.line((267,679,315,679),fill=navy,width=2);d.text((321,660),'in.',font=f,fill=navy)
d.line((888,640,936,640),fill=navy,width=2);d.text((942,621),'in.',font=f,fill=navy)
arr=np.asarray(im).astype(float).copy()
r,g,b=arr[:,:,0],arr[:,:,1],arr[:,:,2]
bright=(r>227)&(g>218)&(b>199)&((r-g)<24)&((g-b)<30)
arr[bright]+=[-15,-18,-20]
im=Image.fromarray(np.clip(arr,0,255).astype('uint8'))
# Exact approved logo artwork is copied from the already-published Baseball guide.
# Only the logo region, not the heading, is replaced.
im.paste(baseball.crop((0,0,274,283)),(0,0))
buf=BytesIO();im.save(buf,format='PNG',optimize=True)
enc=base64.b64encode(buf.getvalue()).decode()
Path('guides/basketball_jersey.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1248" height="1248" viewBox="0 0 1248 1248"><image width="1248" height="1248" xlink:href="data:image/png;base64,'+enc+'"/></svg>')
im.save('basketball-review-preview.png',optimize=True)
print('Candidate bytes',len(buf.getvalue()))

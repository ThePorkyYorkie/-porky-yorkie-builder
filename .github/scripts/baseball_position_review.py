from pathlib import Path
import re
p=Path("index.html")
s=p.read_text()
marker='"baseball_jersey":{"positions":'
start=s.find(marker)
assert start>=0,"Baseball Jersey layout not found"
end=s.find(',"numberSize":0.75}',start)
assert end>start
end+=len(',"numberSize":0.75}')
old=s[start:end]
new=old
for key,x,y in [("Pit to Pit",17.9,48.4),("Length",77.9,48.4)]:
  pat=r'("'+re.escape(key)+r'":\{"x":)[0-9.]+(,"y":)[0-9.]+'
  new,n=re.subn(pat,lambda m:m.group(1)+str(x)+m.group(2)+str(y),new)
  assert n==1,(key,n)
assert new!=old
s=s[:start]+new+s[end:]
assert s.count(new)==1
p.write_text(s)
print("Updated Baseball Jersey layout:",new)

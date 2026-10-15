import sys, json, numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage as ndi
src, out = sys.argv[1], sys.argv[2]
im = Image.open(src).convert('RGBA'); a = np.array(im)[:,:,3]
mask = a > 24
# merge pieces separated by <=3px gaps (antialias halos, thin straps)
merged = ndi.binary_dilation(mask, iterations=3)
lab, n = ndi.label(merged)
objs = ndi.find_objects(lab)
boxes=[]
for i,s in enumerate(objs):
    ys,xs=s
    sub = (lab[s]==i+1) & mask[s]
    area=int(sub.sum())
    if area<40: continue
    y0,y1,x0,x1=ys.start,ys.stop,xs.start,xs.stop
    # shrink to true pixels
    yy,xx=np.nonzero(sub); 
    boxes.append(dict(id=len(boxes),x0=int(x0+xx.min()),y0=int(y0+yy.min()),x1=int(x0+xx.max()+1),y1=int(y0+yy.max()+1),area=area,
        touches_edge=bool(x0+xx.min()==0 or y0+yy.min()==0 or x0+xx.max()+1>=a.shape[1] or y0+yy.max()+1>=a.shape[0])))
boxes.sort(key=lambda b:(b['y0']//60, b['x0']))
for i,b in enumerate(boxes): b['id']=i
json.dump(dict(size=im.size,boxes=boxes),open(out+'.json','w'),indent=0)
# annotated preview
bg=Image.new('RGBA',im.size,(235,235,235,255)); bg.alpha_composite(im)
d=ImageDraw.Draw(bg)
try: f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',14)
except: f=None
for b in boxes:
    d.rectangle([b['x0'],b['y0'],b['x1'],b['y1']],outline=(255,0,0,255) if b['touches_edge'] else (0,120,255,255))
    d.text((b['x0']+1,b['y0']+1),str(b['id']),fill=(200,0,0,255),font=f)
bg.convert('RGB').save(out+'_annot.png')
print(src, im.size, len(boxes),'components')

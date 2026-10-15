import sys, json, os, numpy as np
from PIL import Image
from scipy import ndimage as ndi
src, tag, outdir = sys.argv[1], sys.argv[2], sys.argv[3]
dil=int(sys.argv[4]) if len(sys.argv)>4 else 1
os.makedirs(outdir, exist_ok=True)
arr=np.array(Image.open(src).convert('RGBA')); a=arr[:,:,3]
mask=a>8
lab,n=ndi.label(ndi.binary_dilation(mask,iterations=dil) if dil else mask)
H,W=a.shape; res=[]
for i,s in enumerate(ndi.find_objects(lab)):
    sub=(lab[s]==i+1)&mask[s]
    area=int(sub.sum())
    if area<30: continue
    yy,xx=np.nonzero(sub); y0=s[0].start+yy.min(); y1=s[0].start+yy.max()+1; x0=s[1].start+xx.min(); x1=s[1].start+xx.max()+1
    m=(lab[y0:y1,x0:x1]==i+1)&mask[y0:y1,x0:x1]
    crop=arr[y0:y1,x0:x1].copy(); crop[~m]=0  # drop neighbour fragments
    al=crop[:,:,3].astype(int); rgb=crop[:,:,:3].astype(int); lum=rgb.mean(2)
    semi=((al>8)&(al<200)).sum()/area
    haze=((al>8)&(al<235)&(lum>195)).sum()/area      # pale translucent fringe = baked bg remnant
    opaque_white=((al>=235)&(lum>238)).sum()/area
    edge=bool(x0==0 or y0==0 or x1>=W or y1>=H)
    name=f'{tag}_{len(res):03d}'
    Image.fromarray(crop).save(f'{outdir}/{name}.png')
    res.append(dict(name=name,sheet=tag,x0=int(x0),y0=int(y0),x1=int(x1),y1=int(y1),w=int(x1-x0),h=int(y1-y0),area=area,edge=edge,semi=round(semi,3),haze=round(haze,3),white=round(opaque_white,3)))
json.dump(res,open(f'{outdir}/{tag}.json','w'),indent=0)
print(tag,len(res))

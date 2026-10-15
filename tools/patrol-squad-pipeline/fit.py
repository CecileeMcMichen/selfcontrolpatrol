import numpy as np, json, sys
from PIL import Image, ImageDraw
from scipy import ndimage as ndi
B='game/assets/patrol-squad'
board=np.array(Image.open('orig/assets/board.png').convert('RGB')).astype(int)
r,g,b=board[...,0],board[...,1],board[...,2]
yellow=(r>215)&(g>200)&(b<120)&(abs(r-g)<45)
free=ndi.binary_erosion(ndi.binary_opening(yellow,iterations=1),iterations=5)  # 5px clearance from any printed ink
# also keep away from every playable space (radius 46)
sys.path.insert(0,'.')
spaces=[]
import re
src=open('orig/data/spaces.js').read()
for x,y,t in re.findall(r'\[(\d+),(\d+),"(\w+)"\]',src): spaces.append((int(x),int(y)))
yy,xx=np.mgrid[0:board.shape[0],0:board.shape[1]]
for x,y in spaces: free&=((xx-x)**2+(yy-y)**2)>46**2
H,W=free.shape
def fit(path,region,hmax,hmin=80,step=3):
    im=Image.open(path).convert('RGBA')
    best=None
    for h in range(hmax,hmin-1,-4):
        w=round(im.width*h/im.height); m=np.array(im.resize((w,h),Image.BILINEAR))[...,3]>30
        x0,y0,x1,y1=region
        for by in range(y1,y0+h-1,-step):          # baseline (feet) y
            for cx in range(x0+w//2,x1-w//2,step):
                tx,ty=cx-w//2,by-h
                if ty<0 or tx<0 or tx+w>W or by>H: continue
                if not free[ty:by,tx:tx+w][m].all(): continue
                return dict(h=h,w=w,cx=cx,by=by)
    return None
if __name__=='__main__':
    plan=json.loads(sys.argv[1]); res={}
    vis=Image.open('orig/assets/board.png').convert('RGBA')
    for key,(path,region,hmax) in plan.items():
        f=fit(f'{B}/{path}',region,hmax); res[key]=f; print(key,f)
        if f:
            im=Image.open(f'{B}/{path}').convert('RGBA').resize((f['w'],f['h']),Image.LANCZOS)
            vis.alpha_composite(im,(f['cx']-f['w']//2,f['by']-f['h']))
        d=ImageDraw.Draw(vis); d.rectangle(region,outline=(255,0,255,255),width=2)
    vis.convert('RGB').save('seg/fit_preview.png'); json.dump(res,open('seg/fit.json','w'))

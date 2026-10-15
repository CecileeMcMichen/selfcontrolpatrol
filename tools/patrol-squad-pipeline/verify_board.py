"""Pixel-level check: every pose a board mascot can show sits on plain board background,
clear of printed ink and of every playable space (same criteria as fit.py)."""
import json, re, numpy as np
from PIL import Image
from scipy import ndimage as ndi
import sys
G=(sys.argv[1].rstrip('/')+'/') if len(sys.argv)>1 else './'
m=json.load(open(G+'assets/patrol-squad/manifest.json'))
board=np.array(Image.open(G+'assets/board.png').convert('RGB')).astype(int)
r,g,b=board[...,0],board[...,1],board[...,2]
yellow=(r>215)&(g>200)&(b<120)&(abs(r-g)<45)
free_ink=ndi.binary_erosion(ndi.binary_opening(yellow,iterations=1),iterations=3)   # >=3px from any ink
H,W=yellow.shape; yy,xx=np.mgrid[0:H,0:W]
spaces=[(int(x),int(y)) for x,y,t in re.findall(r'\[(\d+),(\d+),"(\w+)"\]',open(G+'data/spaces.js').read())]
near_space=np.zeros_like(yellow)
for x,y in spaces: near_space|=((xx-x)**2+(yy-y)**2)<=40**2
bad=[]; n=0
for k,c in m['characters'].items():
    bd=c['board']; poses=set(bd['idle'])|set(bd['alternates'])|set(bd['statePose'].values())
    for p in sorted(poses):
        info=c['poses'][p]; im=Image.open(G+info['src']).convert('RGBA')
        h=round(bd['unit']*info['heightFactor']); w=round(im.width*h/im.height)
        a=np.array(im.resize((w,h),Image.BILINEAR))[...,3]>40
        x0=round(bd['x']-w/2); y0=bd['baseline']-h
        ys,xs=np.nonzero(a); X=xs+x0; Y=ys+y0
        inside=(X>=0)&(X<W)&(Y>=0)&(Y<H)
        ink=int((~free_ink[Y[inside],X[inside]]).sum()); sp=int(near_space[Y[inside],X[inside]].sum())
        n+=1
        if ink or sp: bad.append((k,p,'ink px',ink,'space px',sp))
print(f'{n} board pose placements checked; problems: {bad}')

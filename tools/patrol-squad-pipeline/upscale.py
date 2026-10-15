import sys, numpy as np
from PIL import Image, ImageFilter
def up2(im, sharpen=True):
    im=im.convert('RGBA'); a=np.array(im).astype(np.float32)/255
    al=a[...,3:4]; pre=np.concatenate([a[...,:3]*al,al],-1)
    W,H=im.width*2,im.height*2
    ch=[np.array(Image.fromarray((pre[...,i]*255).astype(np.uint8)).resize((W,H),Image.LANCZOS)).astype(np.float32)/255 for i in range(4)]
    rgb=np.stack(ch[:3],-1); A=np.clip(ch[3],0,1)
    out=np.where(A[...,None]>1e-3, rgb/np.maximum(A[...,None],1e-3), 0)
    o=Image.fromarray((np.clip(np.concatenate([out,A[...,None]],-1),0,1)*255).astype(np.uint8),'RGBA')
    if sharpen:
        rgbim=o.convert('RGB').filter(ImageFilter.UnsharpMask(radius=1.6,percent=70,threshold=2))
        o=Image.merge('RGBA',(*rgbim.split(),o.getchannel('A')))
    return o
if __name__=='__main__':
    up2(Image.open(sys.argv[1])).save(sys.argv[2])

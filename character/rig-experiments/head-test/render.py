from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import math
import numpy as np
root=Path(__file__).resolve().parents[3]; out=Path(__file__).resolve().parent
im=Image.open(root/'character/poses/presenter-wave.png').convert('RGBA'); w,h=im.size
# Crop an actual head layer from the selected artwork, including the lower jaw.
# The underlying area is filled with the original neutral background; existing neck remains.
mask=Image.new('L',(w,h)); d=ImageDraw.Draw(mask)
d.polygon([(50,0),(570,0),(570,390),(560,453),(552,520),(533,582),(500,625),(456,653),(410,673),(365,662),(319,642),(275,612),(240,572),(216,520),(216,453),(208,400),(50,400)],fill=255)
mask=mask.filter(ImageFilter.GaussianBlur(1.5))
# Remove cream background from head layer, retaining only the actual artwork.
a=np.asarray(im).astype(float); region=np.asarray(mask).astype(float)/255
# Background is light cream; preserve dark hair, skin, earrings and antialiased edges.
bgscore=np.maximum(0,np.minimum(1,(242-a[:,:,0])/18))
alpha=(region*bgscore*255).astype('uint8')
head=im.copy();head.putalpha(Image.fromarray(alpha))
# Preserve the natural background gradient sampled on the right side of each row.
fill=np.zeros((h,w,4),dtype=np.uint8); sample=np.asarray(im)[:,w-8,:]; fill[:]=sample[:,None,:]
base=im.copy();base.paste(Image.fromarray(fill),(0,0),mask)
# Articulated 2D pivot: chin at the neck is held fixed. This does not synthesize a new 3D perspective.
pivot=(386,650); frames=[]
for i in range(72):
 t=i/18; angle=2.8*math.sin(2*math.pi*t/4)
 h2=head.rotate(angle,Image.Resampling.BICUBIC,center=pivot)
 frame=Image.alpha_composite(base,h2).convert('RGB').resize((384,688),Image.Resampling.LANCZOS)
 frames.append(frame)
frames[0].save(out/'head-pivot-test.gif',save_all=True,append_images=frames[1:],duration=56,loop=0,optimize=False)

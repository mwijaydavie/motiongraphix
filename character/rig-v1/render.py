#!/usr/bin/env python3
"""Experimental 2D cutout rig with real head and arm pivots; no generative video."""
from pathlib import Path
import math, subprocess, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import imageio_ffmpeg
D=Path(__file__).resolve().parent; R=D.parents[1]; f=imageio_ffmpeg.get_ffmpeg_exe()
source=Image.open(R/'character/poses/presenter-wave.png').convert('RGBA'); body=Image.open(D/'body-plate.png').convert('RGBA')
# Use the armless plate only on the left; retain the original other arm.
left=Image.open(D/'base-plate.png').convert('RGBA'); blend=Image.new('L',body.size); bd=ImageDraw.Draw(blend);bd.rectangle((0,500,205,1376),fill=255);blend=blend.filter(ImageFilter.GaussianBlur(14));body=Image.composite(left,body,blend)
if source.size!=body.size: raise ValueError('image dimensions differ')
w,h=source.size
# Region-specific foreground mask; cream background fades out at its borders.
def layer(image,polygon):
 region=Image.new('L',(w,h));ImageDraw.Draw(region).polygon(polygon,fill=255);region=region.filter(ImageFilter.GaussianBlur(1))
 a=np.asarray(image).astype(float); a_bg=np.clip((246-a[:,:,0])/26,0,1); m=np.asarray(region)/255
 alpha=(a_bg*m*255).astype('uint8'); result=image.copy(); result.putalpha(Image.fromarray(alpha));return result
head_area=[(45,0),(590,0),(590,430),(570,510),(552,570),(520,622),(470,658),(410,690),(365,675),(320,653),(275,620),(242,580),(210,525),(205,440),(45,430)]
arm_area=[(0,525),(230,525),(230,700),(235,810),(247,920),(231,1115),(180,1200),(20,1200),(0,1100)]
def face_variant(path,center,rx,ry):
 other=Image.open(path).convert('RGBA');m=Image.new('L',(w,h));d=ImageDraw.Draw(m);x,y=center;d.ellipse((x-rx,y-ry,x+rx,y+ry),fill=255);m=m.filter(ImageFilter.GaussianBlur(7));return Image.composite(other,source,m)
openmouth=face_variant(R/'character/rig-experiments/wave-mouth-open.png',(400,590),66,38)
closedeyes=face_variant(R/'character/rig-experiments/wave-blink.png',(420,475),125,60)
head=layer(source,head_area); headtalk=layer(openmouth,head_area);headblink=layer(closedeyes,head_area);arm=layer(source,arm_area)
# Renderer chooses blend from voice activity; no phoneme alignment yet.
voice=R/'production/noellyne-intro/voice.mp3'; pcm=subprocess.run([f,'-loglevel','error','-i',str(voice),'-ac','1','-ar','24000','-f','s16le','-'],stdout=subprocess.PIPE,check=True).stdout
samples=np.frombuffer(pcm,dtype=np.int16).astype('float32')/32768; sr=24000
fps=24;W,H=540,960;dur=8
cmd=[f,'-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(fps),'-i','-','-i',str(voice),'-t',str(dur),'-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-movflags','+faststart',str(D/'rig-test.tmp.mp4')]
p=subprocess.Popen(cmd,stdin=subprocess.PIPE); value=0
for i in range(dur*fps):
 t=i/fps;pos=int(t*sr);s=samples[max(0,pos-400):pos+400];rms=float(np.sqrt(np.mean(s*s))) if len(s) else 0; value=value*.5+min(1,max(0,(rms-.015)*13))*.5
 isblink=(t%4.3)<.13 and t>1
 face=headblink if isblink else Image.blend(head,headtalk,value*.9)
 angle=1.6*math.sin(t*1.4)+.5*math.sin(t*.62)
 # Separately rotated layers: elbow/cuff as arm pivot, neck as head pivot.
 cur=body.copy();cur.alpha_composite(arm.rotate(3.2*math.sin(t*2.7),Image.Resampling.BICUBIC,center=(145,1005)))
 cur.alpha_composite(face.rotate(angle,Image.Resampling.BICUBIC,center=(390,658)))
 p.stdin.write(cur.convert('RGB').resize((W,H),Image.Resampling.LANCZOS).tobytes())
 if i%48==0:print(i,flush=True)
p.stdin.close();assert p.wait()==0;(D/'rig-test.tmp.mp4').replace(D/'rig-test.mp4')

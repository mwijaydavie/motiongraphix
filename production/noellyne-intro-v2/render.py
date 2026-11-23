#!/usr/bin/env python3
"""Noellyne v2: pose-cut test and softly aligned AI mouth patches, not a 3D rig."""
from pathlib import Path
import sys, math, subprocess, wave
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageFilter
import imageio_ffmpeg
root=Path(__file__).resolve().parents[2]; out=Path(__file__).resolve().parent
ff=imageio_ffmpeg.get_ffmpeg_exe(); voice=root/'production/noellyne-intro/voice.mp3'; wav=out/'analysis.wav'
subprocess.run([ff,'-y','-loglevel','error','-i',str(voice),'-ac','1','-ar','24000',str(wav)],check=True)
with wave.open(str(wav),'rb') as w:
 sr=w.getframerate(); audio=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype('float32')/32768
wav.unlink(); dur=len(audio)/sr; fps=24; W,H=540,960; n=math.ceil((dur+.7)*fps)
coords={'wave':(400,590),'open':(432,605),'point':(440,595),'like':(401,553),'thanks':(398,570)}
# Avoid changing any other pixels in independently generated mouth edits.
def patch_mask(size,center,rx,ry,blur=8):
 m=Image.new('L',size); d=ImageDraw.Draw(m); x,y=center;d.ellipse((x-rx,y-ry,x+rx,y+ry),fill=255);return m.filter(ImageFilter.GaussianBlur(blur))
assets={}
for key in coords:
 base=Image.open(root/f'character/poses/presenter-{key}.png').convert('RGB')
 editname='wave-mouth-open.png' if key=='wave' else key+'-mouth-ah.png'
 edit=Image.open(root/'character/rig-experiments'/editname).convert('RGB')
 if edit.size!=base.size: raise ValueError('different image geometry')
 mask=patch_mask(base.size,coords[key],65,36,7)
 talk=Image.composite(edit,base,mask)
 assets[key]=(base.resize((W,H),Image.Resampling.LANCZOS),talk.resize((W,H),Image.Resampling.LANCZOS))
# Waves are full pose changes, not hand cutouts: no detached wrist.
shots=[(0,'wave'),(4.3,'open'),(9.4,'point'),(14.6,'wave'),(20.6,'like'),(26.2,'thanks'),(30.8,'open')]
font='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; regular='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
f1=ImageFont.truetype(font,20); f2=ImageFont.truetype(font,28); fr=ImageFont.truetype(regular,16)
cmd=[ff,'-y','-loglevel','error','-f','rawvideo','-pixel_format','rgb24','-video_size',f'{W}x{H}','-framerate',str(fps),'-i','-','-i',str(voice),'-filter_complex','[1:a]apad[a]','-map','0:v','-map','[a]','-t',str(n/fps),'-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart',str(out/'intro-v2.tmp.mp4')]
p=subprocess.Popen(cmd,stdin=subprocess.PIPE); smooth=0
for i in range(n):
 t=i/fps; st,key=max((s for s in shots if s[0]<=t),key=lambda z:z[0]); b,talk=assets[key]
 pos=int(t*sr); smp=audio[max(0,pos-350):min(len(audio),pos+350)]; rms=float(np.sqrt(np.mean(smp*smp))) if len(smp) else 0
 target=max(0,min(1,(rms-.015)*16)); smooth=.4*smooth+.6*target
 # Blend photorealistic mouth patch, gated by voice activity, not phoneme-based.
 frame=Image.blend(b,talk,smooth*.9)
 # Soft push-in and drift for the shot, no claim of articulated neck motion.
 scale=1.018+0.012*((t-st)/5%1); nw=round(W*scale);nh=round(H*scale)
 frame=frame.resize((nw,nh),Image.Resampling.BICUBIC); dx=(nw-W)//2+int(2*math.sin(t*.6));dy=(nh-H)//2
 frame=frame.crop((dx,dy,dx+W,dy+H))
 d=ImageDraw.Draw(frame,'RGBA');d.rounded_rectangle((18,19,164,50),radius=15,fill=(92,40,81,235));d.text((30,23),'NOELLYNE',font=f1,fill='white')
 d.rounded_rectangle((18,820,W-18,925),radius=18,fill=(43,25,40,235))
 if t<8: a,c='HABARI!','Mimi ni Noellyne.'
 elif t<16: a,c='KARIBU','Stories za maisha & vicheko.'
 elif t<25: a,c='SIDE EYE','Hapa hatuhukumiani.'
 else: a,c='TUKO PAMOJA','Uko tayari? Twende!'
 d.text((32,831),a,font=f1,fill=(246,174,160,255));d.text((32,866),c,font=f2,fill=(255,250,245,255));d.text((33,904),'INTRO  /  MOTION STUDY',font=fr,fill=(215,193,205,255))
 p.stdin.write(frame.tobytes())
 if i%120==0: print(f'{i}/{n}',flush=True)
p.stdin.close(); rc=p.wait()
if rc: sys.exit(rc)
(out/'intro-v2.tmp.mp4').replace(out/'noellyne-intro-v2.mp4');print(f'{n/fps:.2f}s')

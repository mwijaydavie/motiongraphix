#!/usr/bin/env python3
"""Narrated motion-comic: intentional still portraits, editorial cards, no fake lip sync."""
from pathlib import Path
import math, subprocess
from PIL import Image,ImageDraw,ImageFont
import imageio_ffmpeg
D=Path(__file__).resolve().parent; R=D.parents[1]; ff=imageio_ffmpeg.get_ffmpeg_exe(); W,H=540,960; fps=24
# Editorial text, not verbatim subtitles. Shot boundaries are approximate speech beats.
beats=[
 (0,3.8,'presenter-surprised','DUKANI KITU KIMOJA','Halafu ukatoka na vitano?','01 / THE PLAN'),
 (3.8,9.1,'presenter-point','SABUNI TU.','Hiyo ilikuwa mission.','02 / THE MISSION'),
 (9.1,13.7,'presenter-open','BISKUTI + JUICE','Na ile “deal ya leo” 😅','03 / THE DETOUR'),
 (13.7,17.1,'side-eye','SABUNI JE?','Niliisahau. Bila aibu.','04 / PLOT TWIST'),
 (17.1,23.0,'thinking','KABLA YA KUNUNUA','Nilihitaji kabla sijakiona?','05 / THE CHECK'),
 (23.0,28.9,'presenter-thanks','HESHIMU LIST YAKO','Shopping list nayo ina feelings.','06 / THE LESSON')]
font='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; reg='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
fbrand=ImageFont.truetype(font,17);fsmall=ImageFont.truetype(font,15);fheadline=ImageFont.truetype(font,31);fsub=ImageFont.truetype(reg,22);fend=ImageFont.truetype(font,19)
images={name:Image.open(R/'character/poses'/f'{name}.png').convert('RGB').resize((540,968),Image.Resampling.LANCZOS) for _,_,name,*_ in beats}
# Static editorial panels, prepared once for consistent typography.
panels=[]
for _,_,name,title,sub,tag in beats:
 p=Image.new('RGBA',(500,170),(0,0,0,0)); d=ImageDraw.Draw(p)
 d.rounded_rectangle((0,0,499,169),radius=23,fill='#311c32');d.rounded_rectangle((20,18,184,44),radius=11,fill='#f6b69d');d.text((30,22),tag,font=fsmall,fill='#44213d')
 # Fit long titles to the panel instead of clipping.
 size=31; ft=ImageFont.truetype(font,size)
 while d.textbbox((0,0),title,font=ft)[2]>458 and size>18:
  size-=1;ft=ImageFont.truetype(font,size)
 d.text((20,57),title,font=ft,fill='#fff7eb');d.text((20,109),sub.replace(' 😅',''),font=fsub,fill='#f4c5b6')
 panels.append(p)
cmd=[ff,'-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','540x960','-r',str(fps),'-i','-','-i',str(D/'voice.mp3'),'-t','29','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart',str(D/'story.tmp.mp4')]
p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
for i in range(29*fps):
 t=i/fps; idx=next((j for j,b in enumerate(beats) if b[0]<=t<b[1]),len(beats)-1); start,end,name,*_=beats[idx]; local=t-start
 # Comic cut with restrained push-in; stills are deliberately not called character animation.
 scale=1.0+min(local,5)*.004; nw=round(W*scale);nh=round(968*scale); pic=images[name].resize((nw,nh),Image.Resampling.BICUBIC); pic=pic.crop(((nw-W)//2,0,(nw-W)//2+W,H)).convert('RGBA')
 d=ImageDraw.Draw(pic,'RGBA');d.rounded_rectangle((18,20,204,52),radius=16,fill=(73,36,68,235));d.text((32,26),'NOELLYNE / STORY',font=fbrand,fill='#fff6eb')
 # A quick eased entrance for each editorial card.
 u=min(1,max(0,local/.32)); eased=1-(1-u)**3; y=770+round((1-eased)*28); pic.alpha_composite(panels[idx],(20,y))
 # Small timed beat marker reinforces pacing without claiming subtitles.
 d=ImageDraw.Draw(pic,'RGBA');d.rounded_rectangle((20,947,520,953),radius=3,fill=(63,34,59,95));d.rounded_rectangle((20,947,20+int(500*t/29),953),radius=3,fill=(237,122,110,255))
 p.stdin.write(pic.convert('RGB').tobytes())
 if i%120==0: print(i,flush=True)
p.stdin.close(); assert p.wait()==0;(D/'story.tmp.mp4').replace(D/'shopping-story.mp4')

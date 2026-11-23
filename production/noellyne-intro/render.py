#!/usr/bin/env python3
"""Early Noellyne performance test. Audio amplitude is NOT phoneme lip sync."""
from pathlib import Path
import subprocess, math, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[2]; HERE=Path(__file__).resolve().parent
ffmpeg=imageio_ffmpeg.get_ffmpeg_exe(); FPS=24; W,H=540,960
# Mono PCM is used only to drive the approximate mouth opening.
wav=HERE/'voice-analysis.wav'
subprocess.run([ffmpeg,'-y','-loglevel','error','-i',str(HERE/'voice.mp3'),'-ac','1','-ar','24000',str(wav)],check=True)
with wave.open(str(wav),'rb') as f:
 sr=f.getframerate(); a=np.frombuffer(f.readframes(f.getnframes()),dtype=np.int16).astype(np.float32)/32768
D=len(a)/sr; frames=math.ceil((D+0.7)*FPS)
img=Image.open(ROOT/'character/poses/presenter-wave.png').convert('RGB').resize((W,H),Image.Resampling.LANCZOS)
font='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; regular='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
f1=ImageFont.truetype(font,24); f2=ImageFont.truetype(font,38); small=ImageFont.truetype(regular,18); med=ImageFont.truetype(font,20)
# Cut just the greeting hand above the cuff; repaint the exposed background, animate with a small pivot.
# Coordinates on this 540x960 source are deliberately conservative.
base=img.copy(); d=ImageDraw.Draw(base); bg=img.getpixel((5,430)); d.rectangle((0,380,152,520),fill=bg)
hand=img.crop((0,380,152,550)).convert('RGBA'); ma=Image.new('L',hand.size); md=ImageDraw.Draw(ma); md.polygon([(6,52),(23,14),(43,0),(92,0),(133,33),(151,79),(133,143),(109,169),(57,169),(28,133)],fill=255);ma=ma.filter(ImageFilter.GaussianBlur(3)); mask=np.array(ma); mask[130:,:]=(mask[130:,:]*(np.linspace(1,0,40)[:,None])).astype("uint8"); hand.putalpha(Image.fromarray(mask))
cmd=[ffmpeg,'-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-i',str(HERE/'voice.mp3'),'-filter_complex','[1:a]apad[a]','-map','0:v','-map','[a]','-t',str(frames/FPS),'-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart',str(HERE/'noellyne-intro.tmp.mp4')]
p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
for i in range(frames):
 t=i/FPS; x=base.copy().convert('RGBA')
 # Animated hand cutout; this is only a 2D sticker and does not change elbow pose.
 theta=3.0*math.sin(t*3.2) if t<5 else 1.1*math.sin(t*1.6)
 hp=hand.rotate(theta,resample=Image.Resampling.BICUBIC,center=(78,160),expand=False)
 x.alpha_composite(hp,(0,380)); draw=ImageDraw.Draw(x)
 # A small dark opening inside the existing mouth, driven by vocal energy. No phonetic claims.
 pos=int(t*sr); sample=a[max(0,pos-400):min(len(a),pos+400)]
 rms=float(np.sqrt(np.mean(sample*sample))) if len(sample) else 0
 openness=min(1,max(0,(rms-.012)*8));
 if openness>0.1:
  cx,cy=283,408; ry=2+int(openness*6); draw.ellipse((cx-12,cy-1,cx+12,cy+ry), fill=(66,26,28,255));
  if openness>.4: draw.arc((cx-8,cy-2,cx+8,cy+3),0,180,fill=(236,208,185,255),width=2)
 # Occasional blink over the existing eyelids, stylised overlay.
 phase=(t+0.4)%5.8
 if .0<phase<.12:
  draw.line([(225,330),(269,346)],fill=(67,32,24,255),width=4);draw.line([(311,348),(365,353)],fill=(67,32,24,255),width=4)
 # Gentle breathing: entire photograph tilts; not a separate head joint.
 tilt=0.7*math.sin(t*.95)+0.3*math.sin(t*.4)
 x=x.rotate(tilt,Image.Resampling.BICUBIC,center=(W//2,680),fillcolor=(247,237,221,255)).convert('RGB')
 draw=ImageDraw.Draw(x,'RGBA')
 draw.rounded_rectangle((22,24,187,56),radius=16,fill=(91,34,84,225)); draw.text((36,31),'NOELLYNE',font=med,fill='white')
 draw.text((W-153,33),'INTRO / 01',font=small,fill=(90,48,69,220))
 # Short editorial cards, not subtitles; generously held on screen.
 if t<5.8: line1,line2='HABARI,','MIMI NI NOELLYNE.'
 elif t<13.3: line1,line2='STORIES ZA','MAISHA & VICHEKO.'
 elif t<22: line1,line2='NGOJA KIDOGO…','KWELI?'
 elif t<29: line1,line2='HAPA','HATUHUKUMIANI.'
 else: line1,line2='UKO TAYARI?','TWENDE!'
 draw.rounded_rectangle((18,777,W-18,932),radius=23,fill=(41,24,42,224))
 draw.text((39,793),line1,font=f1,fill=(244,182,167,255));draw.text((39,832),line2,font=f2,fill=(255,250,243,255),stroke_width=0)
 draw.text((41,898),'STORIES  ·  KICHEKO  ·  MAISHA',font=small,fill=(221,199,211,255))
 p.stdin.write(x.tobytes())
 if i%120==0: print(f'{i}/{frames}',flush=True)
p.stdin.close(); rc=p.wait(); wav.unlink(missing_ok=True)
if rc: sys.exit(rc)
(HERE/'noellyne-intro.tmp.mp4').replace(HERE/'noellyne-intro.mp4')
print('duration',frames/FPS,flush=True)

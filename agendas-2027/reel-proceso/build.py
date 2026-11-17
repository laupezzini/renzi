#!/usr/bin/env python3
"""Reel "Así nace una agenda Renzi": el proceso en 6 pasos, con tarjetas Renzi y fundidos suaves.
Uso: python3 build.py CARPETA_FUENTES SALIDA.mp4
CARPETA: IMG_7377.MOV, IMG_7386.MP4 (parte 1), costura_105/509.mp4, parte3.mp4, fin2.mp4, s_agenda.mp4, s_2027.mp4, s_cta.mp4"""
import subprocess, sys, tempfile
RAW, OUT = sys.argv[1:3]; X = 0.3
GR = "eq=contrast=1.04:saturation=1.06:gamma=1.02,huesaturation=saturation=-0.2:colors=r+y:strength=1"
# (fuente, inicio, duración, velocidad, zoom0, zoom1, recorte extra, tarjetas)
T = [
 ("s_agenda.mp4",0.2,1.9,1,1.00,1.07,1.0,["hook"]),
 ("fotos/15_225023.jpg",0,1.2,1,1.00,1.07,1.0,["p1"]), ("fotos/15_225118.jpg",0,1.1,1,1.06,1.00,1.0,["p1"]),
 ("IMG_7377.MOV",32.5,1.6,1,1.00,1.06,1.0,["p2"]), ("IMG_7386.MP4",17.0,1.3,1,1.02,1.08,1.0,["p2"]),
 ("costura_105.mp4",0.0,1.5,1,1.00,1.06,1.5,["p3"]), ("costura_509.mp4",0.0,1.4,2,1.02,1.08,1.5,["p3"]),
 ("fotos/15_230423.jpg",0,1.2,1,1.00,1.08,1.0,["p4"]), ("fotos/15_230255_h.jpg",0,1.1,1,1.08,1.00,1.0,["p4"]),
 ("parte3.mp4",38.4,1.7,1,1.00,1.06,1.35,["p5"]),
 ("fin2.mp4",0.2,1.5,1,1.00,1.07,1.0,["p6"]),
 ("s_2027.mp4",0.3,1.5,1,1.00,1.06,1.0,["lista"]),
 ("s_cta.mp4",0.0,4.4,0.6,1.00,1.05,1.0,["cta"]),
]
def run(c): subprocess.run(c, check=True)
tmp=tempfile.mkdtemp(); starts=[]; t=0
for i,(src,a,d,sp,z0,z1,cr,_) in enumerate(T):
    starts.append(t); t+=d-(X if i<len(T)-1 else 0); n=int(round(d*30))
    base=f"scale=1188:2112:force_original_aspect_ratio=increase:flags=lanczos,crop=1188:2112"
    if cr>1: base=f"scale=iw*{cr}:ih*{cr}:flags=lanczos,crop=iw/{cr}:ih/{cr},"+base
    zp=f"{base},zoompan=z='{z0}+({z1}-{z0})*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,setsar=1,{GR},unsharp=5:5:0.5,format=yuv420p"
    if src.endswith(".jpg"):
        run(["ffmpeg","-v","error","-y","-loop","1","-framerate","30","-i",src,"-vf",zp,"-frames:v",str(n),"-c:v","libx264","-crf","15","-preset","veryfast",f"{tmp}/c{i}.mp4"])
    else:
        run(["ffmpeg","-v","error","-y","-ss",str(a),"-i",f"{RAW}/{src}","-an","-vf",f"setpts=PTS/{sp},fps=30,{zp}","-frames:v",str(n),"-c:v","libx264","-crf","15","-preset","veryfast",f"{tmp}/c{i}.mp4"])
total=t; inp=[]; fc=[]; prev="0:v"
for i in range(len(T)): inp+=["-i",f"{tmp}/c{i}.mp4"]
for i in range(1,len(T)): fc.append(f"[{prev}][{i}:v]xfade=transition=fade:duration={X}:offset={starts[i]:.3f}[x{i}]"); prev=f"x{i}"
# tarjetas: una por tramo continuo con la misma tarjeta
spans=[]
for i,(*_,cards) in enumerate(T):
    c=cards[0]; st=starts[i]; en=starts[i]+T[i][2]-(X/2 if i<len(T)-1 else 0)
    if spans and spans[-1][0]==c: spans[-1][2]=en
    else: spans.append([c,st,en])
k=len(T)
for c,st,en in spans:
    st+=0.12; inp+=["-loop","1","-t",f"{en+0.1:.2f}","-i",f"card_{c}.png"]
    fc.append(f"[{k}:v]format=rgba,fade=in:st={st:.2f}:d=0.3:alpha=1,fade=out:st={en-0.22:.2f}:d=0.22:alpha=1[o{k}]")
    fc.append(f"[{prev}][o{k}]overlay=x=0:y='if(lt(t,{st:.2f}),28,max(0,28-28*(t-{st:.2f})/0.3))':eof_action=pass[y{k}]"); prev=f"y{k}"; k+=1
fc.append(f"[{prev}]format=yuv420p[v]")
run(["ffmpeg","-v","error","-y"]+inp+["-f","lavfi","-i","anullsrc=r=44100:cl=stereo","-filter_complex",";".join(fc),"-map","[v]","-map",f"{k}:a","-t",f"{total:.3f}",
     "-c:v","libx264","-profile:v","high","-level","4.0","-preset","slow","-crf","18","-maxrate","8M","-bufsize","16M","-g","60","-r","30","-c:a","aac","-b:a","96k","-movflags","+faststart",OUT])
print("listo",round(total,2),"s")

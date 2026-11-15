#!/usr/bin/env python3
"""Reel de Navidad, versión elegante con las tomas nuevas (agenda rosa, libreta de gamuza, taller de Federico).
Tomas largas con fundidos suaves, zoom lento, color cálido y tarjetas con la tipografía de Renzi.
Uso: python3 build_elegante.py CARPETA_TOMAS SALIDA.mp4   (tomas ya retocadas: s_*.mp4)"""
import subprocess, sys, tempfile
RAW, OUT = sys.argv[1:3]
X = 0.4   # fundido entre tomas
GR = "eq=contrast=1.04:saturation=1.07:gamma=1.02,colorbalance=rm=0.03:bm=-0.03,huesaturation=saturation=-0.15:colors=r+y:strength=1"
# (toma, inicio, duración, velocidad, zoom inicial, zoom final, tarjetas [(png, desde, hasta) relativos a la toma])
T = [
 ("s_cta",0.0,2.7,1,1.00,1.08,[("hook",0.15,None)]),
 ("s_agenda",0.0,2.5,1,1.04,1.10,[("p1",0.1,None),("p1l",0.7,None)]),
 ("s_lib1",0.0,2.5,1,1.10,1.02,[("p2",0.1,None),("p2l",0.7,None)]),
 ("s_lib2",0.0,2.4,1,1.02,1.09,[("p3",0.1,None),("p3l",0.7,None)]),
 ("s_corp",0.0,2.4,1,1.03,1.10,[("p4",0.1,None),("p4l",0.7,None)]),
 ("s_2027",0.0,2.4,1,1.08,1.00,[("p5",0.1,None),("p5l",0.7,None)]),
 ("s_vos",0.0,1.6,1,1.02,1.08,[("vos",0.1,None)]),
 ("s_mano",0.0,2.1,1,1.04,1.10,[("mano",0.1,None),("manol",0.6,None)]),
 ("s_hook",0.0,4.6,0.6,1.00,1.06,[("cta",0.35,None)]),
]
def run(c): subprocess.run(c, check=True)
tmp=tempfile.mkdtemp(); starts=[]; t=0
for i,(src,a,d,sp,z0,z1,_) in enumerate(T):
    starts.append(t); t+=d-(X if i<len(T)-1 else 0); n=int(round(d*30))
    vf=(f"setpts=PTS/{sp},fps=30,scale=1188:2112:force_original_aspect_ratio=increase:flags=lanczos,crop=1188:2112,"
        f"zoompan=z='{z0}+({z1}-{z0})*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,setsar=1,{GR},unsharp=5:5:0.5,format=yuv420p")
    run(["ffmpeg","-v","error","-y","-ss",str(a),"-i",f"{RAW}/{src}.mp4","-an","-vf",vf,"-frames:v",str(n),"-c:v","libx264","-crf","15","-preset","veryfast",f"{tmp}/c{i}.mp4"])
total=t
inp=[]; fc=[]; prev="0:v"
for i in range(len(T)): inp+=["-i",f"{tmp}/c{i}.mp4"]
for i in range(1,len(T)): fc.append(f"[{prev}][{i}:v]xfade=transition=fade:duration={X}:offset={starts[i]:.3f}[x{i}]"); prev=f"x{i}"
# tarjetas: aparecen con fundido y suben 30 px; se van con el fundido de la toma
k=len(T)
for i,(src,a,d,sp,z0,z1,cards) in enumerate(T):
    end = starts[i]+d-(X/2 if i<len(T)-1 else 0)
    for png,frm,_ in cards:
        st=starts[i]+frm; dur=end-st
        path="cta.png" if png=="cta" else f"card_{png}.png"
        inp+=["-loop","1","-t",f"{end+0.1:.2f}","-i",path]
        fc.append(f"[{k}:v]format=rgba,fade=in:st={st:.2f}:d=0.35:alpha=1,fade=out:st={end-0.25:.2f}:d=0.25:alpha=1[o{k}]")
        fc.append(f"[{prev}][o{k}]overlay=x=0:y='if(lt(t,{st:.2f}),30,max(0,30-30*(t-{st:.2f})/0.35))':eof_action=pass[y{k}]"); prev=f"y{k}"; k+=1
fc.append(f"[{prev}]format=yuv420p[v]")
run(["ffmpeg","-v","error","-y"]+inp+["-f","lavfi","-i","anullsrc=r=44100:cl=stereo","-filter_complex",";".join(fc),"-map","[v]","-map",f"{k}:a","-t",f"{total:.3f}",
     "-c:v","libx264","-profile:v","high","-level","4.0","-preset","slow","-crf","18","-maxrate","8M","-bufsize","16M","-g","60","-r","30",
     "-c:a","aac","-b:a","96k","-movflags","+faststart",OUT])
print("listo",round(total,2),"s")

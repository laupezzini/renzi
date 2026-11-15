#!/usr/bin/env python3
"""Reel de Navidad con tomas reales y edición dinámica (cortes cortos, zooms, transiciones, textos con pop).
Uso: python3 build.py CARPETA_FUENTES FONTS_DIR SALIDA.mp4
CARPETA: hojeada_r.mp4, cuad_r.mp4 (fin1 desde 50 s, retocado), fin1.mp4, costura_105.mp4, costura_509.mp4"""
import subprocess, sys, tempfile, os
RAW, FONTS, OUT = sys.argv[1:4]
K = "../reel-final/fotos/kraft/"
PIEL = "huesaturation=saturation=-0.2:colors=r+y:strength=1,eq=gamma=1.02:saturation=1.08:contrast=1.04"
X = 0.16          # duración de cada transición
# (fuente, inicio, duración en pantalla, velocidad, zoom)  zoom: in | out | punch
C = [
 ("cuad_r.mp4",12.7,1.4,1,"out"),  ("hojeada_r.mp4",0.2,1.0,1.2,"in"), ("cuad_r.mp4",14.0,1.0,1,"punch"),          # gancho
 (K+"foto12.jpg",0,0.95,1,"punch"), ("hojeada_r.mp4",44.2,1.0,1,"in"), ("hojeada_r.mp4",15.8,0.95,1,"in"),          # agenda
 ("cuad_r.mp4",14.6,0.95,1,"punch"),("cuad_r.mp4",18.0,0.95,1,"in"),  ("cuad_r.mp4",24.2,0.95,1,"in"),              # cuaderno de tela
 ("cuad_r.mp4",20.6,1.0,1,"punch"), ("hojeada_r.mp4",82.4,0.95,1,"in"),                                               # libretas
 ("fin1.mp4",9.0,1.0,1.6,"punch"),  ("costura_509.mp4",0.0,1.0,2,"in"),                                               # corporativos
 (K+"foto13.jpg",0,1.0,1,"punch"),  ("hojeada_r.mp4",90.0,1.0,1,"in"),                                                # fin de año
 (K+"foto9.jpg",0,0.85,1,"punch"),  ("cuad_r.mp4",27.0,0.85,1,"in"),  (K+"foto14.jpg",0,0.85,1,"in"),                 # y para vos
 ("costura_105.mp4",0.0,1.3,1,"in"),                                                                                  # hecho a mano
 (K+"foto10.jpg",0,4.2,1,"cta"),                                                                                      # cierre
]
TRANS = ["smoothleft","zoomin","smoothup","fadewhite","smoothright","slideleft","circleopen","smoothdown","wipeleft","zoomin"]
def run(c): subprocess.run(c, check=True)
tmp = tempfile.mkdtemp()
def zexpr(kind, n):
    return {"in":f"1+0.10*on/{n}", "out":f"1.20-0.20*on/{n}", "punch":f"1+0.22*max(0,1-on/7)+0.05*on/{n}", "cta":f"1.04+0.06*on/{n}"}[kind]
starts=[]; t=0.0
for i,(src,a,d,sp,z) in enumerate(C):
    starts.append(t); t += d - (X if i < len(C)-1 else 0)
    n=int(round(d*30)); o=f"{tmp}/c{i:02d}.mp4"
    zp=f"scale=1296:2304:force_original_aspect_ratio=increase:flags=lanczos,crop=1296:2304,zoompan=z='{zexpr(z,n)}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,setsar=1"
    if src.endswith(".jpg"):
        run(["ffmpeg","-v","error","-y","-loop","1","-framerate","30","-t",f"{d}","-i",src,"-vf",f"{zp},{PIEL},unsharp=5:5:0.4,format=yuv420p","-frames:v",str(n),"-c:v","libx264","-crf","16","-preset","veryfast",o])
    else:
        run(["ffmpeg","-v","error","-y","-ss",f"{a}","-t",f"{d*sp+0.1}","-i",f"{RAW}/{src}","-an","-vf",f"setpts=PTS/{sp},fps=30,{zp},{PIEL},unsharp=5:5:0.6,format=yuv420p","-frames:v",str(n),"-c:v","libx264","-crf","16","-preset","veryfast",o])
total = t
# cadena de transiciones
inp=[]; fc=[]; prev="0:v"; off=0.0
for i in range(len(C)): inp += ["-i",f"{tmp}/c{i:02d}.mp4"]
for i in range(1,len(C)):
    off = starts[i]; tr = TRANS[(i-1)%len(TRANS)] if C[i][0]!=C[i-1][0] or True else "fade"
    fc.append(f"[{prev}][{i}:v]xfade=transition={tr}:duration={X}:offset={off:.3f}[x{i}]"); prev=f"x{i}"
# placa final
fc.append(f"[{prev}]null[base]")
cta_t = starts[-1]
run(["ffmpeg","-v","error","-y"]+inp+["-loop","1","-i","cta.png","-filter_complex",";".join(fc)+
     f";[{len(C)}:v]format=rgba,fade=in:st={cta_t+0.25:.2f}:d=0.35:alpha=1[ov];[base][ov]overlay=0:0:shortest=1,format=yuv420p[v]",
     "-map","[v]","-t",f"{total:.3f}","-c:v","libx264","-crf","16","-preset","veryfast",f"{tmp}/video.mp4"])
# textos
S = starts
def sec(i,j): return S[i], S[j]+0.05
EV=[]  # (estilo, inicio, fin, texto)
def persona(i,j,l1,l2,lab,price=None):
    a,b=sec(i,j)
    EV.append(("T1",a+0.05,b,l1)); EV.append(("T2",a+0.22,b,l2))
    lb = lab + (r"{\c&H8AD3F6&} · "+price if price else "")
    EV.append(("Lab",S[i+1]+0.05 if i+1<=j else a+0.6,b,lb))
EV += [("H1",0.05,S[3]+0.05,"Mandale esto"),("H2",0.3,S[3]+0.05,"a quien te tiene\\Nque regalar"),("H3",0.7,S[3]+0.05,"en Navidad")]
persona(3,6,"Para la que anota","todo en post-its","Agenda 2027","desde $40.000")
persona(6,9,"Para el que dice","«no necesito nada»","Cuaderno de tela","$28.000")
persona(9,11,"Para la que siempre","tiene una idea","Libretas y cuadernos","desde $8.000")
persona(11,13,"Para la empresa","que saluda a su equipo","Regalos corporativos","consultá por cantidad")
persona(13,15,"Para saludar a alguien","por fin de año","Un presente hecho a mano")
a,b=sec(15,18); EV += [("T1",a+0.05,b,"Y para vos,"),("T2",a+0.22,b,"porque también\\Nte lo merecés")]
a,b=sec(18,19); EV += [("T1",a+0.05,b,"Hecho a mano,"),("T2",a+0.22,b,"hilo por hilo"),("Lab",a+0.4,b,"Renzi · La Plata")]
POP=r"{\fscx55\fscy55\t(0,140,\fscx110\fscy110)\t(140,230,\fscx100\fscy100)\fad(60,90)}"
def ts(x): return f"{int(x//3600)}:{int(x%3600//60):02d}:{x%60:05.2f}"
ass="""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: H1,DM Sans 9pt ExtraBold,88,&H00465D2F,&H00FFFFFF,&H00F3FAFF,&H00F3FAFF,1,0,0,0,100,100,0,0,3,22,0,8,60,60,330,1
Style: H2,DM Sans 9pt ExtraBold,88,&H00465D2F,&H00FFFFFF,&H00F3FAFF,&H00F3FAFF,1,0,0,0,100,100,0,0,3,22,0,8,60,60,470,1
Style: H3,DM Sans 9pt ExtraBold,96,&H00FFFFFF,&H00FFFFFF,&H006B45D6,&H006B45D6,1,0,0,0,100,100,0,0,3,24,0,8,60,60,750,1
Style: T1,DM Sans 9pt ExtraBold,74,&H00FFFFFF,&H00FFFFFF,&H00465D2F,&H00465D2F,1,0,0,0,100,100,0,0,3,20,0,8,70,70,270,1
Style: T2,Dancing Script,136,&H006B45D6,&H00FFFFFF,&H00F8FDFF,&H50000000,1,0,0,0,100,100,0,0,1,3,3,8,50,50,385,1
Style: Lab,DM Sans 9pt ExtraBold,64,&H00FFFFFF,&H00FFFFFF,&H00465D2F,&H00465D2F,1,0,0,0,100,100,0,0,3,22,0,2,70,70,560,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""+"\n".join(f"Dialogue: 1,{ts(a)},{ts(b)},{k},,0,0,0,,{POP}{x}" for k,a,b,x in EV)+"\n"
open(f"{tmp}/t.ass","w").write(ass)
run(["ffmpeg","-v","error","-y","-i",f"{tmp}/video.mp4","-vf",f"ass={tmp}/t.ass:fontsdir={FONTS},format=yuv420p","-c:v","libx264","-crf","16","-preset","veryfast",f"{tmp}/vtext.mp4"])
# eventos de sonido para sfx_real.py
import json
json.dump({"total":total,"cuts":S[1:],"personas":[S[i] for i in (3,6,9,11,13)],"labels":[e[1] for e in EV if e[0]=="Lab"],
           "vos":S[15],"mano":S[18],"cta":cta_t},open(f"{tmp}/ev.json","w"))
os.replace(f"{tmp}/vtext.mp4", OUT.replace(".mp4","_mudo_tmp.mp4")); os.replace(f"{tmp}/ev.json", OUT.replace(".mp4",".ev.json"))
print("listo", round(total,2), "s")

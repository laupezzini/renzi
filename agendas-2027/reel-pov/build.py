#!/usr/bin/env python3
"""Reel "POV: le pedís a un encuadernador «una agenda nomás»". Cortes rápidos con aceleración, remate lento y cierre con pregunta.
Uso: python3 build.py CARPETA_FUENTES FONTS_DIR SALIDA.mp4"""
import subprocess, sys, tempfile
RAW, FONTS, OUT = sys.argv[1:4]
GR="eq=contrast=1.05:saturation=1.08:gamma=1.02,huesaturation=saturation=-0.2:colors=r+y:strength=1"
# (fuente, inicio, duración en pantalla, velocidad, zoom inicial, zoom final, recorte, texto)
T=[
 ("IMG_7374.MOV",0.3,1.9,1,1.00,1.10,1.0,"POV: le pedís\\Na un encuadernador\\N«una agenda nomás»"),
 ("IMG_7377.MOV",11.5,0.8,2.2,1.15,1.00,1.0,"dobla 420 hojas"),
 ("IMG_7386.MP4",17.0,0.7,2.2,1.00,1.12,1.0,"una por una"),
 ("costura_105.mp4",0.0,0.8,1.6,1.20,1.00,1.5,"las cose a mano"),
 ("costura_509.mp4",0.0,0.7,3,1.00,1.12,1.5,"hilo por hilo"),
 ("15_230423.jpg",0,0.7,1,1.18,1.00,1.0,"las prensa"),
 ("parte3.mp4",38.4,0.8,2,1.00,1.12,1.35,"encola el lomo"),
 ("15_230255_h.jpg",0,0.7,1,1.00,1.15,1.0,"lo deja 6 horas\\Nen la prensa"),
 ("fin1.mp4",9.0,0.8,2.2,1.15,1.00,1.0,"lo saca…"),
 ("fin2.mp4",0.2,2.2,0.7,1.00,1.08,1.0,"…y te entrega esto"),
 ("s_agenda.mp4",0.2,1.5,1,1.00,1.06,1.0,"420 hojas,\\Nun día por página"),
 ("s_2027.mp4",0.3,1.4,0.8,1.05,1.00,1.0,"«una agenda nomás»"),
 ("s_cta.mp4",0.0,3.8,0.5,1.00,1.06,1.0,"¿Cuánto creés\\Nque vale?"),
]
def run(c): subprocess.run(c, check=True)
tmp=tempfile.mkdtemp(); lst=open(f"{tmp}/l.txt","w"); t=0; ev=[]
for i,(src,a,d,sp,z0,z1,cr,txt) in enumerate(T):
    n=int(round(d*30)); o=f"{tmp}/c{i:02d}.mp4"
    base="scale=1188:2112:force_original_aspect_ratio=increase:flags=lanczos,crop=1188:2112"
    if cr>1: base=f"scale=iw*{cr}:ih*{cr}:flags=lanczos,crop=iw/{cr}:ih/{cr},"+base
    blur=",tmix=frames=3" if sp>=2 else ""
    zp=f"{base},zoompan=z='{z0}+({z1}-{z0})*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,setsar=1,{GR},unsharp=5:5:0.5,format=yuv420p"
    if src.endswith(".jpg"):
        run(["ffmpeg","-v","error","-y","-loop","1","-framerate","30","-i",src,"-vf",zp,"-frames:v",str(n),"-c:v","libx264","-crf","15","-preset","veryfast",o])
    else:
        run(["ffmpeg","-v","error","-y","-ss",str(a),"-i",f"{RAW}/{src}","-an","-vf",f"setpts=PTS/{sp},fps=30{blur},{zp}","-frames:v",str(n),"-c:v","libx264","-crf","15","-preset","veryfast",o])
    lst.write(f"file '{o}'\n"); ev.append((t,t+d,txt,i)); t+=d
lst.close(); total=t
run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",f"{tmp}/l.txt","-c","copy",f"{tmp}/v.mp4"])
POP=r"{\fscx70\fscy70\t(0,110,\fscx106\fscy106)\t(110,180,\fscx100\fscy100)}"
def ts(x): return f"{int(x//3600)}:{int(x%3600//60):02d}:{x%60:05.2f}"
L=[]
for a,b,txt,i in ev:
    st="Hook" if i==0 else ("Q" if i==len(T)-1 else "Cap")
    if st=="Q": b=a+1.3
    L.append(f"Dialogue: 1,{ts(a+0.03)},{ts(b)},{st},,0,0,0,,{POP}{txt}")
ass="""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Hook,DM Sans 9pt ExtraBold,100,&H00FFFFFF,&H00FFFFFF,&H00141414,&H96000000,1,0,0,0,100,100,0,0,1,8,5,8,40,40,330,1
Style: Cap,DM Sans 9pt ExtraBold,128,&H00FFFFFF,&H00FFFFFF,&H00141414,&H96000000,1,0,0,0,100,100,0,0,1,9,6,5,50,50,0,1
Style: Q,DM Sans 9pt ExtraBold,124,&H00FFFFFF,&H00FFFFFF,&H00141414,&H96000000,1,0,0,0,100,100,0,0,1,9,6,8,50,50,480,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""+"\n".join(L)+"\n"
open(f"{tmp}/t.ass","w").write(ass)
qa=ev[-1][0]+1.2
run(["ffmpeg","-v","error","-y","-i",f"{tmp}/v.mp4","-loop","1","-i","cta.png","-f","lavfi","-i","anullsrc=r=44100:cl=stereo","-filter_complex",
     f"[0:v]ass={tmp}/t.ass:fontsdir={FONTS}[v0];[1:v]format=rgba,fade=in:st={qa:.2f}:d=0.3:alpha=1[o];[v0][o]overlay=0:'if(lt(t,{qa:.2f}),40,max(0,40-40*(t-{qa:.2f})/0.3))':shortest=1,format=yuv420p[v]",
     "-map","[v]","-map","2:a","-t",f"{total:.3f}","-c:v","libx264","-profile:v","high","-level","4.0","-preset","slow","-crf","18","-maxrate","8M","-bufsize","16M","-g","60","-r","30",
     "-c:a","aac","-b:a","96k","-movflags","+faststart",OUT])
print("listo",round(total,2),"s")

#!/usr/bin/env python3
"""Video para estados de WhatsApp, solo la agenda (material nuevo con fondo de papel madera, sin la prensa). Sin sonido.
Uso: python3 build_wa_kraft.py CARPETA_CON_hojeada.mp4 SALIDA.mp4"""
import subprocess, sys, tempfile
RAW, OUT = sys.argv[1], sys.argv[2]
SUAVE = "huesaturation=saturation=-0.3:colors=r+y:strength=1,eq=gamma=1.02"
# (tipo, fuente, inicio, duración, velocidad, subtítulo, cartel)
T = [
 ("foto",  "fotos/kraft/foto9.jpg",  0,    2.6, 1,   "tapa dura ilustrada",               "AGENDA 2027 · HECHA A MANO"),
 ("video", "hojeada.mp4",            8.2,  3.0, 1,   None,                                 None),
 ("video", "hojeada.mp4",           12.0,  6.0, 1.5, "guardas azules por dentro",         None),
 ("foto",  "fotos/kraft/foto13.jpg", 0,    2.4, 1,   "dos cintas para marcar las páginas", None),
 ("foto",  "fotos/kraft/foto17.jpg", 0,    2.4, 1,   "página de datos personales",        None),
 ("foto",  "fotos/kraft/foto18.jpg", 0,    3.0, 1,   "calendario mensual y un día por página", None),
 ("foto",  "fotos/kraft/foto15.jpg", 0,    2.2, 1,   "con horarios y espacio para notas", None),
 ("video", "hojeada.mp4",           55.0,  8.0, 2.0, "420 hojas cosidas a mano",          None),
]
FIN_FOTO, FIN = "fotos/kraft/foto10.jpg", 4.5
# foto que no es vertical: se ve entera sobre un fondo desenfocado de sí misma
FIT = ("split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:4[bg];"
       "[b]scale=1000:1800:force_original_aspect_ratio=decrease:flags=lanczos[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1")
def run(c): subprocess.run(c, check=True)
def ts(t): return f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"
def foto_vf(path, d):
    from PIL import Image
    w,h = Image.open(path).size
    base = ("scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,setsar=1" if h/w > 1.7 else FIT)
    return f"{base},scale=1188:2112,zoompan=z='1+0.0008*on':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d={int(d*30)}:s=1080x1920:fps=30"
tmp=tempfile.mkdtemp(); lst=open(f"{tmp}/l.txt","w"); t=0.0; ev=[]
for n,(tipo,src,a,d,sp,sub,label) in enumerate(T):
    od=d/sp
    if tipo=="foto":
        run(["ffmpeg","-v","error","-y","-loop","1","-t",str(od),"-i",src,"-vf",foto_vf(src,od)+",format=yuv420p","-t",str(od),"-c:v","libx264","-crf","17","-preset","veryfast","-r","30",f"{tmp}/s{n}.mp4"])
    else:
        vf=f"setpts=PTS/{sp},fps=30,scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,setsar=1,{SUAVE},format=yuv420p"
        run(["ffmpeg","-v","error","-y","-ss",str(a),"-t",str(d),"-i",f"{RAW}/{src}","-an","-vf",vf,"-t",f"{od:.3f}","-c:v","libx264","-crf","17","-preset","veryfast","-r","30",f"{tmp}/s{n}.mp4"])
    lst.write(f"file '{tmp}/s{n}.mp4'\n")
    if sub: ev.append(f"Dialogue: 0,{ts(t+0.15)},{ts(t+od)},Sub,,0,0,0,,{sub}")
    if label: ev.append(f"Dialogue: 1,{ts(t)},{ts(t+od)},Top,,0,0,0,,{label}")
    t+=od
run(["ffmpeg","-v","error","-y","-loop","1","-t",str(FIN),"-i",FIN_FOTO,"-loop","1","-t",str(FIN),"-i","overlays/end_wa.png","-filter_complex",
     f"[0:v]{foto_vf(FIN_FOTO,FIN)}[v];[1:v]format=rgba,fade=in:st=0.2:d=0.4:alpha=1[o];[v][o]overlay=0:0,format=yuv420p","-t",str(FIN),"-c:v","libx264","-crf","17","-preset","veryfast","-r","30",f"{tmp}/fin.mp4"])
lst.write(f"file '{tmp}/fin.mp4'\n"); lst.close()
ass="""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,Inter,64,&H00FFFFFF,&H00FFFFFF,&H00281E14,&H96000000,1,0,0,0,100,100,0,0,1,7,2,2,90,90,430,1
Style: Top,Inter,46,&H00FFFFFF,&H00FFFFFF,&H006B45D6,&H006B45D6,1,0,0,0,100,100,3,0,3,18,0,8,90,90,230,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""+"\n".join(ev)+"\n"
open(f"{tmp}/s.ass","w").write(ass)
run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",f"{tmp}/l.txt","-c","copy",f"{tmp}/all.mp4"])
run(["ffmpeg","-v","error","-y","-i",f"{tmp}/all.mp4","-f","lavfi","-i","anullsrc=r=44100:cl=stereo","-map","0:v","-map","1:a","-shortest",
     "-vf",f"ass={tmp}/s.ass:fontsdir=/usr/share/fonts/opentype/inter,fps=30,format=yuv420p",
     "-c:v","libx264","-profile:v","high","-level","4.0","-preset","slow","-crf","20","-maxrate","8M","-bufsize","16M","-g","60",
     "-c:a","aac","-b:a","96k","-movflags","+faststart",OUT])
print(f"listo: {OUT} ({t+FIN:.1f} s)")

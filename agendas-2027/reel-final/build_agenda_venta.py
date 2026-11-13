#!/usr/bin/env python3
"""Reel de venta "agenda_venta.mp4" (estilo UGC sensorial, solo texto, sin voz; la música se elige en Instagram).
Uso: python3 build_agenda_venta.py CARPETA SALIDA.mp4
CARPETA: costura_105/128/509.mp4 y hojeada_r.mp4 (ya retocados: luz + piel de manos, ver retoque_video.py), hojeada.mp4 (papel madera), postits.mp4 (animación del problema)."""
import subprocess, sys, tempfile
RAW, OUT = sys.argv[1], sys.argv[2]
PIEL = "huesaturation=saturation=-0.25:colors=r+y:strength=1,huesaturation=saturation=-0.05,eq=gamma=1.02"
def macro(x,y): return f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,crop=540:960:{x}:{y},scale=1080:1920:flags=lanczos,unsharp=5:5:0.4"
FULL = "scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920"
# (tipo, fuente, inicio, duración, velocidad, encuadre, texto grande, texto chico)
T = [
 ("v","costura_105.mp4",0.0,1.6,1,  macro(110,80), "Esto no es\nuna agenda más.", None),                       # hook: macro aguja
 ("v","costura_128.mp4",0.0,1.4,1,  macro(60,0),   None, "cosida a mano, hilo por hilo"),                       # aguja en el lomo
 ("v","postits.mp4",0.0,  4.0,1.33,None,         None, None),                                                  # problema (animación)
 ("v","hojeada_r.mp4",0.0,  2.4,1,  FULL,          "Agenda 2027", "hecha a mano en La Plata"),                   # solución: tapa en las manos
 ("v","costura_509.mp4",0.0,5.0,2,  macro(200,0),  "Cosida hilo a hilo", "firme, para todo el año"),             # valor 1
 ("v","hojeada_r.mp4",3.6,  3.0,1.2,FULL,          "Cosida hilo a hilo", "420 hojas, una por una"),
 ("v","hojeada_r.mp4",19.4, 2.0,1,  FULL,          "Papel de calidad", "con página de datos personales"),        # valor 2: interior
 ("v","hojeada_r.mp4",25.0, 1.8,1,  FULL,          "Papel de calidad", "calendario 2027 completo"),
 ("v","hojeada_r.mp4",35.2, 1.8,1,  FULL,          "Papel de calidad", "páginas para planificar"),
 ("v","hojeada_r.mp4",49.0, 1.8,1,  FULL,          "Papel de calidad", "calendario mensual"),
 ("v","hojeada_r.mp4",44.2, 1.6,1,  FULL,          "Papel de calidad", "un día por página, con horarios"),
 ("v","hojeada_r.mp4",82.4, 1.6,1,  FULL,          "Papel de calidad", "y hojas para notas"),
 ("o","hojeada_r.mp4",44.2, 2.4,0.55,FULL,       None, None),                                                  # formatos (placa)
 ("v","hojeada_r.mp4",15.6, 2.0,1,  FULL,          "Pieza única", "guardas azules y dos cintas"),            # valor 3
 ("f","fotos/kraft/foto18.jpg",0,2.0,1,None,     "Tu año, en orden.", "planificá con calma"),                  # emoción
 ("v","hojeada_r.mp4",90.0, 2.9,1,  FULL,          "Tu 2027 empieza acá.", None),
]
FIN_FOTO, FIN = "fotos/kraft/foto9.jpg", 5.0
FIT = ("split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:4[bg];"
       "[b]scale=1000:1800:force_original_aspect_ratio=decrease:flags=lanczos[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1")
def run(c): subprocess.run(c, check=True)
def ts(t): return f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"
def foto_vf(path, d):
    from PIL import Image
    w,h = Image.open(path).size
    base = (FULL+",setsar=1") if h/w > 1.7 else FIT
    return f"{base},scale=1188:2112,zoompan=z='1+0.0009*on':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d={int(d*30)}:s=1080x1920:fps=30"
tmp=tempfile.mkdtemp(); lst=open(f"{tmp}/l.txt","w"); t=0.0; ev=[]; prev=(None,None)
for n,(tipo,src,a,d,sp,enc,big,small) in enumerate(T):
    od=d/sp
    if tipo=="f":
        run(["ffmpeg","-v","error","-y","-loop","1","-t",str(od),"-i",src,"-vf",foto_vf(src,od)+",format=yuv420p","-t",str(od),"-c:v","libx264","-crf","17","-preset","veryfast","-r","30",f"{tmp}/s{n}.mp4"])
    elif tipo=="o":
        run(["ffmpeg","-v","error","-y","-ss",str(a),"-t",str(d),"-i",f"{RAW}/{src}","-loop","1","-i","overlays/formatos_venta.png","-filter_complex",
             f"[0:v]setpts=PTS/{sp},fps=30,{enc},setsar=1,{PIEL},gblur=sigma=6[v];[1:v]format=rgba,fade=in:st=0:d=0.3:alpha=1[o];[v][o]overlay=0:0,format=yuv420p",
             "-an","-t",f"{od:.3f}","-c:v","libx264","-crf","17","-preset","veryfast","-r","30",f"{tmp}/s{n}.mp4"])
    else:
        vf=f"setpts=PTS/{sp},fps=30" + (f",{enc},setsar=1" if enc else "") + ("" if src=="postits.mp4" else f",{PIEL}") + ",format=yuv420p"
        run(["ffmpeg","-v","error","-y","-ss",str(a),"-t",str(d),"-i",f"{RAW}/{src}","-an","-vf",vf,"-t",f"{od:.3f}","-c:v","libx264","-crf","17","-preset","veryfast","-r","30",f"{tmp}/s{n}.mp4"])
    lst.write(f"file '{tmp}/s{n}.mp4'\n")
    # textos: si se repiten en el tramo siguiente, se extienden (no parpadean)
    for kind,txt in (("Big",big),("Small",small)):
        if not txt: continue
        txt=txt.replace("\n","\\N")
        if ev and ev[-1][0]==kind and ev[-1][1]==txt and abs(ev[-1][3]-t)<0.01: ev[-1][3]=t+od
        else: ev.append([kind,txt,t,t+od])
    t+=od
run(["ffmpeg","-v","error","-y","-loop","1","-t",str(FIN),"-i",FIN_FOTO,"-loop","1","-t",str(FIN),"-i","overlays/end_venta.png","-filter_complex",
     f"[0:v]{foto_vf(FIN_FOTO,FIN)}[v];[1:v]format=rgba,fade=in:st=0.15:d=0.4:alpha=1[o];[v][o]overlay=0:0,format=yuv420p","-t",str(FIN),"-c:v","libx264","-crf","17","-preset","veryfast","-r","30",f"{tmp}/fin.mp4"])
lst.write(f"file '{tmp}/fin.mp4'\n"); lst.close()
lines=[]
for kind,txt,a,b in ev:
    fx="{\\fad(180,120)}"
    lines.append(f"Dialogue: {1 if kind=='Big' else 0},{ts(a)},{ts(b)},{kind},,0,0,0,,{fx}{txt}")
ass="""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Big,Inter,92,&H00FFFFFF,&H00FFFFFF,&H00281E14,&HA0000000,1,0,0,0,100,100,0,0,1,8,3,8,70,70,300,1
Style: Small,Inter,58,&H00FFFFFF,&H00FFFFFF,&H006B45D6,&H006B45D6,1,0,0,0,100,100,0,0,3,16,0,2,90,90,380,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""+"\n".join(lines)+"\n"
open(f"{tmp}/s.ass","w").write(ass)
run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",f"{tmp}/l.txt","-c","copy",f"{tmp}/all.mp4"])
run(["ffmpeg","-v","error","-y","-i",f"{tmp}/all.mp4","-f","lavfi","-i","anullsrc=r=44100:cl=stereo","-map","0:v","-map","1:a","-shortest",
     "-vf",f"ass={tmp}/s.ass:fontsdir=/usr/share/fonts/opentype/inter,fps=30,format=yuv420p",
     "-c:v","libx264","-profile:v","high","-level","4.0","-preset","slow","-crf","20","-maxrate","8M","-bufsize","16M","-g","60",
     "-c:a","aac","-b:a","96k","-movflags","+faststart",OUT])
print(f"listo: {OUT} ({t+FIN:.1f} s)")

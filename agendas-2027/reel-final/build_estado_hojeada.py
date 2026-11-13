#!/usr/bin/env python3
"""Estado de WhatsApp solo con la hojeada sobre papel madera (sin sonido). Derivado de build_armala.py.\nReel "Armá tu agenda 2027 en 3 pasos" (solo texto, sin voz; la música se elige en Instagram).
Idea: en vez de listar virtudes, el video muestra cómo se compra: 1 tapa, 2 interior, 3 la cosemos a mano.
Cierra con la preventa (hasta el 20/11) y un pedido simple: escribir AGENDA por mensaje.
Uso: python3 build_armala.py CARPETA SALIDA.mp4   (CARPETA: hojeada_r.mp4, costura_105.mp4, costura_509.mp4)"""
import subprocess, sys, tempfile
RAW, OUT = sys.argv[1], sys.argv[2]
PIEL = "huesaturation=saturation=-0.25:colors=r+y:strength=1,huesaturation=saturation=-0.05,eq=gamma=1.02"
def macro(x,y): return f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,crop=540:960:{x}:{y},scale=1080:1920:flags=lanczos,unsharp=5:5:0.4"
FULL = "scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920"
FIT = ("split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:4[bg];"
       "[b]scale=1000:1800:force_original_aspect_ratio=decrease:flags=lanczos[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1")
TV = "../reel-venta/overlays/"
# (tipo, fuente, inicio, duración, velocidad, encuadre, paso (arriba), texto grande, etiqueta (abajo))
T = [
 ("v","hojeada_r.mp4",0.0, 2.4,1,  FULL, None, "Agenda 2027", "hecha a mano en La Plata"),
 ("v","hojeada_r.mp4",3.6, 3.0,1.2,FULL, None, "Cosida a mano", "hilo por hilo"),
 ("v","hojeada_r.mp4",10.1,1.8,1,  FULL, None, "Guardas azules", "y dos cintas"),
 ("v","hojeada_r.mp4",15.6,2.0,1,  FULL, None, "Guardas azules", "y dos cintas"),
 ("v","hojeada_r.mp4",19.4,2.0,1,  FULL, None, "Adentro", "tus datos personales"),
 ("v","hojeada_r.mp4",25.0,1.8,1,  FULL, None, "Adentro", "calendario 2027"),
 ("v","hojeada_r.mp4",27.6,1.8,1,  FULL, None, "Adentro", "el año de un vistazo"),
 ("v","hojeada_r.mp4",35.2,1.8,1,  FULL, None, "Adentro", "páginas para planificar"),
 ("v","hojeada_r.mp4",49.0,1.8,1,  FULL, None, "Adentro", "calendario mensual"),
 ("v","hojeada_r.mp4",44.2,1.8,1,  FULL, None, "Adentro", "un día por página"),
 ("v","hojeada_r.mp4",65.4,2.2,1,  FULL, None, "Adentro", "todo el año, día por día"),
 ("v","hojeada_r.mp4",82.4,1.6,1,  FULL, None, "Adentro", "y hojas para notas"),
 ("o","hojeada_r.mp4",44.2,2.75,0.5,FULL, None, None, None),
 ("v","hojeada_r.mp4",75.0,2.2,1,  FULL, None, "Tu 2027,\\Nen orden.", None),
]
FIN_SRC, FIN = (90.0, 2.9), 5.0
def run(c): subprocess.run(c, check=True)
def ts(t): return f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"
def foto_vf(path, d):
    from PIL import Image
    w,h = Image.open(path).size
    base = (FULL+",setsar=1") if h/w > 1.7 else FIT
    return f"{base},scale=1188:2112,zoompan=z='1+0.0011*on':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d={int(d*30)}:s=1080x1920:fps=30"
enc = ["-c:v","libx264","-crf","17","-preset","veryfast","-r","30"]
tmp=tempfile.mkdtemp(); lst=open(f"{tmp}/l.txt","w"); t=0.0; ev=[]
for n,(tipo,src,a,d,sp,vf_,paso,big,lab) in enumerate(T):
    od=d/sp; o=f"{tmp}/s{n}.mp4"
    if tipo=="f":
        run(["ffmpeg","-v","error","-y","-loop","1","-t",str(od),"-i",src,"-vf",foto_vf(src,od)+",format=yuv420p","-t",str(od)]+enc+[o])
    elif tipo=="o":
        run(["ffmpeg","-v","error","-y","-ss",str(a),"-t",str(d),"-i",f"{RAW}/{src}","-loop","1","-i","overlays/estado_interiores.png","-filter_complex",
             f"[0:v]setpts=PTS/{sp},fps=30,{vf_},setsar=1,{PIEL},gblur=sigma=8[v];[1:v]format=rgba,fade=in:st=0:d=0.3:alpha=1[o];[v][o]overlay=0:0,format=yuv420p",
             "-an","-t",f"{od:.3f}"]+enc+[o])
    else:
        run(["ffmpeg","-v","error","-y","-ss",str(a),"-t",str(d),"-i",f"{RAW}/{src}","-an","-vf",f"setpts=PTS/{sp},fps=30,{vf_},setsar=1,{PIEL},format=yuv420p","-t",f"{od:.3f}"]+enc+[o])
    lst.write(f"file '{o}'\n")
    for kind,txt in (("Paso",paso),("Big",big),("Lab",lab)):
        if not txt: continue
        if ev and ev[-1][0]==kind and ev[-1][1]==txt and abs(ev[-1][3]-t)<0.01: ev[-1][3]=t+od
        else:
            # mismo tipo, distinto texto: cerrar el anterior para que no se pisen
            ev.append([kind,txt,t,t+od])
    t+=od
run(["ffmpeg","-v","error","-y","-ss",str(FIN_SRC[0]),"-t",str(FIN_SRC[1]),"-i",f"{RAW}/hojeada_r.mp4","-loop","1","-t",str(FIN),"-i","overlays/estado_end.png","-filter_complex",
     f"[0:v]setpts=PTS*{FIN/FIN_SRC[1]:.4f},fps=30,{FULL},setsar=1,{PIEL},gblur=sigma=5[v];[1:v]format=rgba,fade=in:st=0.1:d=0.4:alpha=1[o];[v][o]overlay=0:0,format=yuv420p","-t",str(FIN)]+enc+[f"{tmp}/fin.mp4"])
lst.write(f"file '{tmp}/fin.mp4'\n"); lst.close()
lay={"Paso":2,"Big":1,"Lab":0}
lines=[f"Dialogue: {lay[k]},{ts(a)},{ts(b)},{k},,0,0,0,,{{\\fad(150,100)}}{x}" for k,x,a,b in ev]
ass="""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Paso,Inter,46,&H00221D2B,&H00221D2B,&H00C4B3FF,&H00C4B3FF,1,0,0,0,100,100,6,0,3,14,0,8,90,90,230,1
Style: Big,Inter,100,&H00FFFFFF,&H00FFFFFF,&H00281E14,&HA0000000,1,0,0,0,100,100,0,0,1,8,3,8,70,70,330,1
Style: Lab,Inter,64,&H00FFFFFF,&H00FFFFFF,&H006B45D6,&H006B45D6,1,0,0,0,100,100,0,0,3,18,0,2,90,90,640,1
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

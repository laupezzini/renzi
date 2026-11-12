#!/usr/bin/env python3
"""Video "solo la agenda" para estados de WhatsApp (sin voz).
Uso: python3 build_final.py CARPETA_CRUDOS SALIDA.mp4
CARPETA_CRUDOS debe tener: p1_hojas.mov, p1_doblado.mov, p2.mp4, p3.mp4 (partes 1-3), fin1.mp4 (prensa), fin2.mp4 (hojeando).
Tramo: (archivo, ini_video, duración_original, velocidad, con_voz, plano, [(ini, fin, subtítulo) en tiempo original], cartel)"""
import subprocess, sys, tempfile
RAW, OUT = sys.argv[1], sys.argv[2]
T = [
 ("foto_tapa.mp4",   0.0, 2.4, 1,   False, "foto", [(0.0,2.4,"tapa dura ilustrada")], "AGENDA 2027 · HECHA A MANO"),
 ("fin2.mp4",        0.3, 2.2, 1,   False, "zoom", [], None),
 ("fin2.mp4",        2.5, 5.5, 1.4, False, "sp235", [(2.5,8.0,"guardas azules por dentro")], None),
 ("foto_cintas.mp4", 0.0, 2.2, 1,   False, "foto", [(0.0,2.2,"dos cintas para marcar las páginas")], None),
 ("fin2.mp4",       11.5, 4.0, 1.2, False, "sp280", [(11.5,15.5,"un día por página, con horarios")], None),
 ("fin1.mp4",       31.9, 3.5, 1,   False, "gen",  [(31.9,35.4,"420 hojas cosidas a mano")], None),
]
FOTO, FIN = "fotos/sin-prensa/abierta1.jpg", 4.5
GEN = "scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,setsar=1,eq=saturation=1.06:contrast=1.03"
CER = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,crop=490:872:420:840,scale=1080:1920:flags=lanczos,setsar=1,eq=saturation=1.06:contrast=1.03"
ZOOM = "crop=350:622:105:232,scale=1080:1920:flags=lanczos,setsar=1,eq=saturation=1.06:contrast=1.03"
END_PNG = "overlays/end_wa.png"
PIEL = "huesaturation=saturation=-0.5:colors=r+y:strength=1,huesaturation=hue=-3:colors=r+y,huesaturation=saturation=-0.08,eq=gamma=1.03"
WB = {"fin1.mp4":(0.981,1.005,1.015),"fin2.mp4":(0.989,1.0,1.013)}
def color(f, vf):
    r,g,b = WB.get(f,(1,1,1))
    return f"{vf},colorchannelmixer=rr={r}:gg={g}:bb={b},{PIEL}"
def sin_prensa(y):
    # recorta desde y (debajo de la prensa) y completa el formato vertical con un fondo desenfocado de la misma toma
    return (f"crop=480:{854-y}:0:{y},split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:4,eq=brightness=0.04[bg];"
            f"[b]scale=1080:-2:flags=lanczos[fg];[bg][fg]overlay=0:(H-h)/2,setsar=1")
def run(c): subprocess.run(c, check=True)
def ts(t): return f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"
tmp=tempfile.mkdtemp(); lst=open(f"{tmp}/l.txt","w"); t=0.0; ev=[]
for n,(f,v,d,sp,voz,plano,subs,label) in enumerate(T):
    od=d/sp; vf={"cer":CER,"zoom":ZOOM}.get(plano,GEN)
    if plano.startswith("sp"): vf = sin_prensa(int(plano[2:]))
    if plano != "foto": vf = color(f, vf)
    if f.startswith("fin"): vf+=",unsharp=5:5:0.5"
    if voz:
        af=f"aresample=48000,aformat=channel_layouts=stereo,highpass=f=80,afftdn=nf=-25,afade=t=in:d=0.03,afade=t=out:st={d-0.03:.3f}:d=0.03"
        asrc, ast = (voz if isinstance(voz, tuple) else (f, v))
        run(["ffmpeg","-v","error","-y","-ss",str(v),"-t",str(d),"-i",f"{RAW}/{f}","-ss",str(ast),"-t",str(d),"-i",f"{RAW}/{asrc}","-map","0:v","-map","1:a","-vf",f"fps=30,{vf}","-af",af,
             "-c:v","libx264","-crf","18","-preset","veryfast","-c:a","pcm_s16le","-t",f"{od:.3f}",f"{tmp}/s{n}.mov"])
    else:
        run(["ffmpeg","-v","error","-y","-ss",str(v),"-t",str(d),"-i",f"{RAW}/{f}","-f","lavfi","-t",f"{od:.3f}","-i","anullsrc=r=48000:cl=stereo",
             "-map","0:v","-map","1:a","-vf",f"setpts=PTS/{sp},fps=30,{vf}","-c:v","libx264","-crf","18","-preset","veryfast","-c:a","pcm_s16le","-t",f"{od:.3f}",f"{tmp}/s{n}.mov"])
    lst.write(f"file '{tmp}/s{n}.mov'\n")
    for a,b,tx in subs: ev.append(f"Dialogue: 0,{ts(t+max(0,a-v)/sp)},{ts(t+min(d,b-v)/sp)},Sub,,0,0,0,,{tx}")
    if label: ev.append(f"Dialogue: 1,{ts(t)},{ts(t+od)},{'Precio' if '$' in label else 'Top'},,0,0,0,,{label}")
    t+=od
run(["ffmpeg","-v","error","-y","-loop","1","-t",str(FIN),"-i",FOTO,"-loop","1","-t",str(FIN),"-i",END_PNG,"-f","lavfi","-t",str(FIN),"-i","anullsrc=r=48000:cl=stereo",
     "-filter_complex",f"[0:v]{PIEL},zoompan=z='1+0.0007*on':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d={int(FIN*30)}:s=1080x1920:fps=30,setsar=1[v];[1:v]format=rgba,fade=in:st=0.2:d=0.4:alpha=1[o];[v][o]overlay=0:0,format=yuv420p[vo]",
     "-map","[vo]","-map","2:a","-c:v","libx264","-crf","18","-preset","veryfast","-r","30","-c:a","pcm_s16le","-t",str(FIN),f"{tmp}/fin.mov"])
lst.write(f"file '{tmp}/fin.mov'\n"); lst.close()
ass="""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,Inter,64,&H00FFFFFF,&H00FFFFFF,&H00281E14,&H96000000,1,0,0,0,100,100,0,0,1,7,2,2,90,90,430,1
Style: Top,Inter,46,&H00FFFFFF,&H00FFFFFF,&H006B45D6,&H006B45D6,1,0,0,0,100,100,3,0,3,18,0,8,90,90,230,1
Style: Precio,Inter,38,&H00FFFFFF,&H00FFFFFF,&H006B45D6,&H006B45D6,1,0,0,0,100,100,0,0,3,16,0,8,40,40,230,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""+"\n".join(ev)+"\n"
open(f"{tmp}/s.ass","w").write(ass)
run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",f"{tmp}/l.txt","-c","copy",f"{tmp}/all.mov"])
run(["ffmpeg","-v","error","-y","-i",f"{tmp}/all.mov","-vf",f"ass={tmp}/s.ass:fontsdir=/usr/share/fonts/opentype/inter,fps=30,format=yuv420p",
     "-af","loudnorm=I=-16:TP=-1.5","-c:v","libx264","-profile:v","high","-level","4.0","-preset","slow","-crf","20","-maxrate","8M","-bufsize","16M","-g","60",
     "-c:a","aac","-b:a","160k","-ar","44100","-ac","2","-movflags","+faststart",OUT])
print(f"listo: {OUT} ({t+FIN:.1f} s)")

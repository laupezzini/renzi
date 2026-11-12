#!/usr/bin/env python3
"""Reel final "La agenda terminada".
Uso: python3 build_final.py CARPETA_CRUDOS SALIDA.mp4
CARPETA_CRUDOS debe tener: p1_hojas.mov, p1_doblado.mov, p2.mp4, p3.mp4 (partes 1-3), fin1.mp4 (prensa), fin2.mp4 (hojeando).
Tramo: (archivo, ini_video, duración_original, velocidad, con_voz, plano, [(ini, fin, subtítulo) en tiempo original], cartel)"""
import subprocess, sys, tempfile
RAW, OUT = sys.argv[1], sys.argv[2]
T = [
 ("fin1.mp4",  7.0,  5.4,  1, ("fin1.mp4", 1.25), "gen", [(1.4,4.4,"Vamos a ver cómo salieron la agenda y el cuaderno,"),(4.4,6.65,"que los vamos a sacar de la prensa. ¡Mirá!")], "LA AGENDA TERMINADA"),   # arranca en la prensa con la agenda adentro
 ("fin1.mp4", 24.05, 1.95, 1, True,  "gen", [(24.1,26.0,"¡Mirá la agenda, mirá la agenda!")], None),   # corta antes de que el celular cambie el color
 ("fin1.mp4", 31.9, 3.52, 1, True,  "gen", [(32.4,34.1,"420 hojas…"),(34.1,35.42,"¡420 hojas!")], None),
 ("fin1.mp4", 37.0,  6.0,  1, True,  "gen", [(41.4,43.0,"¡Qué hermosa está!")], None),
 ("fin1.mp4", 46.6,  5.6,  1, True,  "gen", [(46.8,50.3,"Este es un papel con motivo, unos pajaritos,"),(50.3,52.2,"pero también puede ser tela")], None),
 ("fin2.mp4",  0.3,  7.7,  1.6, False, "gen", [(0.3,3.4,"tapa dura ilustrada"),(3.4,8.0,"guardas azules y dos cintas")], None),
 ("formatos.mp4", 0.0, 8.530000, 1, ("tts_formatos.wav", 0.0), "gen", [], None),   # aclara formato y opciones a medida, con voz en off
]
FOTO, FIN = "fotos/abierta1.jpg", 10.410000
VOZ_CIERRE = "tts_cierre.wav"   # voz en off grabada por Laura (limpiada y ecualizada): otras opciones y preventa
GEN = "scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,setsar=1,eq=saturation=1.06:contrast=1.03"
CER = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,crop=490:872:420:840,scale=1080:1920:flags=lanczos,setsar=1,eq=saturation=1.06:contrast=1.03"
# la parte 3 se filmó con más luz: misma corrección de color que en su reel
CER3 = CER + ",eq=brightness=-0.04:saturation=0.62:gamma=0.97,selectivecolor=reds=0 0.10 0.16 0:yellows=0 0.08 0.14 0,colorbalance=rs=-0.06:bs=0.05:rm=-0.08:bm=0.07:rh=-0.04:bh=0.04"

# ---- corrección de color (edición) ----
# piel: menos saturación en rojos/amarillos para que brazos y manos no queden naranjas
PIEL = "huesaturation=saturation=-0.5:colors=r+y:strength=1,huesaturation=hue=-3:colors=r+y,huesaturation=saturation=-0.08,eq=gamma=1.03"
# balance de blancos por archivo (medido sobre papel/mesa/pared, que deben verse blancos)
WB = {"p1_hojas.mov":(0.935,0.989,1.088),"p1_doblado.mov":(0.937,0.998,1.075),"p2.mp4":(1.0,1.0,1.0),"p3.mp4":(1.036,0.987,0.978),
      "fin1.mp4":(0.981,1.005,1.015),"fin2.mp4":(0.989,1.0,1.013)}
# las tomas de la parte 1 son HDR (HLG) del iPhone: se convierten a SDR antes de todo
HDR = {"p1_hojas.mov","p1_doblado.mov"}
TM = "zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p"
def color(f, vf):
    r,g,b = WB.get(f,(1,1,1))
    pre = (TM + ",") if f in HDR else ""
    return f"{pre}{vf},colorchannelmixer=rr={r}:gg={g}:bb={b},{PIEL}"
GANANCIA = {0: -3.5}   # el arranque estaba grabado más cerca y sonaba más fuerte
def run(c): subprocess.run(c, check=True)
def ts(t): return f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"
tmp=tempfile.mkdtemp(); lst=open(f"{tmp}/l.txt","w"); t=0.0; ev=[]
for n,(f,v,d,sp,voz,plano,subs,label) in enumerate(T):
    od=d/sp; vf={"cer":CER,"cer3":CER3}.get(plano,GEN)
    if f.startswith("fin"): vf+=",unsharp=5:5:0.5"
    if not f.startswith("formatos"): vf = color(f, vf)
    if voz:
        af=f"aresample=48000,aformat=channel_layouts=stereo,highpass=f=80,afftdn=nf=-25,afade=t=in:d=0.03,afade=t=out:st={d-0.03:.3f}:d=0.03"
        if n in GANANCIA: af += f",volume={GANANCIA[n]}dB"
        asrc, ast = (voz if isinstance(voz, tuple) else (f, v))
        run(["ffmpeg","-v","error","-y","-ss",str(v),"-t",str(d),"-i",f"{RAW}/{f}","-ss",str(ast),"-t",str(d),"-i",f"{RAW}/{asrc}","-map","0:v","-map","1:a","-vf",f"fps=30,{vf}","-af",af,
             "-c:v","libx264","-crf","18","-preset","veryfast","-c:a","pcm_s16le","-t",f"{od:.3f}",f"{tmp}/s{n}.mov"])
    else:
        run(["ffmpeg","-v","error","-y","-ss",str(v),"-t",str(d),"-i",f"{RAW}/{f}","-f","lavfi","-t",f"{od:.3f}","-i","anullsrc=r=48000:cl=stereo",
             "-map","0:v","-map","1:a","-vf",f"setpts=PTS/{sp},fps=30,{vf}","-c:v","libx264","-crf","18","-preset","veryfast","-c:a","pcm_s16le","-t",f"{od:.3f}",f"{tmp}/s{n}.mov"])
    lst.write(f"file '{tmp}/s{n}.mov'\n")
    ref = voz[1] if isinstance(voz, tuple) else v
    for a,b,tx in subs: ev.append(f"Dialogue: 0,{ts(t+max(0,a-ref)/sp)},{ts(t+min(d,b-ref)/sp)},Sub,,0,0,0,,{tx}")
    if label: ev.append(f"Dialogue: 1,{ts(t)},{ts(t+od)},Top,,0,0,0,,{label}")
    t+=od
run(["ffmpeg","-v","error","-y","-loop","1","-t",str(FIN),"-i",FOTO,"-loop","1","-t",str(FIN),"-i","overlays/end.png","-i",f"{RAW}/{VOZ_CIERRE}",
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
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""+"\n".join(ev)+"\n"
open(f"{tmp}/s.ass","w").write(ass)
run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",f"{tmp}/l.txt","-c","copy",f"{tmp}/all.mov"])
# volumen general: una sola ganancia fija (no dinámica) para respetar las diferencias entre las voces
_m = subprocess.run(["ffmpeg","-i",f"{tmp}/all.mov","-vn","-af","ebur128","-f","null","-"],capture_output=True,text=True).stderr
_I = float([l for l in _m.splitlines() if l.strip().startswith("I:")][-1].split()[1])
gain = -16.0 - _I
run(["ffmpeg","-v","error","-y","-i",f"{tmp}/all.mov","-vf",f"ass={tmp}/s.ass:fontsdir=/usr/share/fonts/opentype/inter,fps=30,format=yuv420p",
     "-af",f"volume={gain:.2f}dB,alimiter=limit=0.89","-c:v","libx264","-profile:v","high","-level","4.0","-preset","slow","-crf","20","-maxrate","8M","-bufsize","16M","-g","60",
     "-c:a","aac","-b:a","160k","-ar","44100","-ac","2","-movflags","+faststart",OUT])
print(f"listo: {OUT} ({t+FIN:.1f} s)")

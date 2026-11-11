#!/usr/bin/env python3
"""Reel "Parte 3: el lomo". Uso: python3 build_p3.py VIDEO_ORIGINAL SALIDA.mp4
Tramo: (video_ini, audio_ini, duración, plano, subtítulos [(ini, fin, texto)] en tiempo de AUDIO original, cartel)
plano: "general" = toma completa; "cerca" = primer plano del lomo (sin la cara)."""
import subprocess, sys, tempfile
SRC, OUT = sys.argv[1], sys.argv[2]
TRAMOS = [
 (50.0, 2.8, 4.8, "cerca", [(2.8,7.5,"Les voy a mostrar cómo encolo el lomo de la agenda 2027")], "PARTE 3 · EL LOMO"),
 (14.3, 14.3, 5.27, "general", [(14.3,16.5,"Para encolar el lomo"),(16.5,19.57,"uso una prensa que construí con madera")], None),
 (31.58, 31.58, 1.75, "general", [(31.58,33.33,"Ajusto la prensa…")], None),
 (38.2, 38.2, 6.0, "cerca", [(38.2,40.0,"y empiezo a encolar el lomo."),(40.0,44.2,"Lo ajusto no mucho, porque después,")], None),
 (44.2, 44.2, 5.7, "general", [(44.2,46.6,"apenas se empieza a secar la cola,"),(46.6,49.9,"lo bajo un poco más y lo ajusto más fuerte")], None),
 (70.8, 70.8, 8.2, "cerca", [(70.8,74.0,"Lo dejamos secando y prensado"),(74.0,79.0,"para después hacer la tapa")], None),
 (79.0, 79.0, 8.1, "general", [(79.0,80.6,"de cartón duro"),(80.6,87.1,"con una lámina hermosa que más tarde van a ver")], None),
 (87.2, 87.2, 4.2, "cerca", [(87.2,89.6,"Muy bien…"),(89.6,91.4,"ahí va quedando el lomo")], None),
 (92.0, 97.9, 1.8, "cerca", [(97.9,99.7,"¡Nos vemos en la próxima!")], None),
]
FIN, FIN_T = 3.8, 91.0
# voz cortada antes del final del tramo (segundos de audio que se usan); el resto queda en silencio
VOZ_HASTA = {0: 4.53}   # "…agenda 2027" termina en 7.33; enseguida dice "que…"   # cuadro final: primer plano del lomo encolado
GEN = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,eq=saturation=1.06:contrast=1.04"
CER = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,crop=490:872:420:840,scale=1080:1920:flags=lanczos,unsharp=5:5:0.6,setsar=1,eq=saturation=1.06:contrast=1.04"
def run(c): subprocess.run(c, check=True)
def ts(t): return f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"
tmp=tempfile.mkdtemp(); lst=open(f"{tmp}/l.txt","w"); t=0.0; ev=[]
for n,(v,a,d,plano,subs,label) in enumerate(TRAMOS):
    vf = CER if plano=="cerca" else GEN
    if n in VOZ_HASTA:
        h = VOZ_HASTA[n]
        af = f"aresample=48000,aformat=channel_layouts=stereo,highpass=f=80,afftdn=nf=-25,afade=t=in:d=0.04,atrim=0:{h},afade=t=out:st={h-0.015:.3f}:d=0.015,apad"
    else:
        af = f"aresample=48000,aformat=channel_layouts=stereo,highpass=f=80,afftdn=nf=-25,afade=t=in:d=0.04,afade=t=out:st={d-0.06:.3f}:d=0.06"
    run(["ffmpeg","-v","error","-y","-ss",str(v),"-t",str(d),"-i",SRC,"-ss",str(a),"-t",str(d),"-i",SRC,"-map","0:v","-map","1:a",
         "-vf",f"fps=30,{vf}","-af",af,"-c:v","libx264","-crf","18","-preset","veryfast","-c:a","pcm_s16le","-t",str(d),f"{tmp}/s{n}.mov"])
    lst.write(f"file '{tmp}/s{n}.mov'\n")
    for sa,sb,tx in subs: ev.append(f"Dialogue: 0,{ts(t+sa-a)},{ts(t+sb-a)},Sub,,0,0,0,,{tx}")
    if label: ev.append(f"Dialogue: 1,{ts(t)},{ts(t+d)},Top,,0,0,0,,{label}")
    t+=d
run(["ffmpeg","-v","error","-y","-ss",str(FIN_T),"-i",SRC,"-frames:v","1","-vf",CER,f"{tmp}/last.png"])
run(["ffmpeg","-v","error","-y","-loop","1","-t",str(FIN),"-i",f"{tmp}/last.png","-loop","1","-t",str(FIN),"-i","overlays/end.png",
     "-f","lavfi","-t",str(FIN),"-i","anullsrc=r=48000:cl=stereo","-filter_complex",
     "[1:v]format=rgba,fade=in:st=0.1:d=0.4:alpha=1[o];[0:v][o]overlay=0:0,format=yuv420p[v]","-map","[v]","-map","2:a",
     "-c:v","libx264","-crf","18","-preset","veryfast","-r","30","-c:a","pcm_s16le","-t",str(FIN),f"{tmp}/fin.mov"])
lst.write(f"file '{tmp}/fin.mov'\n"); lst.close()
ass=f"""[Script Info]
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
run(["ffmpeg","-v","error","-y","-i",f"{tmp}/all.mov","-vf",f"ass={tmp}/s.ass:fontsdir=/usr/share/fonts/opentype/inter,fps=30,format=yuv420p",
     "-af","loudnorm=I=-16:TP=-1.5","-c:v","libx264","-profile:v","high","-level","4.0","-preset","slow","-crf","20","-maxrate","8M","-bufsize","16M","-g","60",
     "-c:a","aac","-b:a","160k","-ar","44100","-ac","2","-movflags","+faststart",OUT])
print(f"listo: {OUT} ({t+FIN:.1f} s)")

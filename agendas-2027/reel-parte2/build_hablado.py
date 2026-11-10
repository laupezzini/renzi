#!/usr/bin/env python3
"""Reel "Parte 2: la costura" con la voz de Federico y subtítulos.
Uso: python3 build_hablado.py VIDEO_ORIGINAL SALIDA.mp4
Cada tramo: (inicio, fin, velocidad, [(t_ini, t_fin, subtítulo), ...] en tiempos del original, cartel)."""
import subprocess, sys, tempfile, os
SRC, OUT = sys.argv[1], sys.argv[2]
TRAMOS = [
 (0.0,   7.3, 1,  [(0.0,0.9,"Bueno, ¿cómo están?"),(1.1,3.7,"Quedate conmigo que te voy a mostrar"),(3.7,7.3,"cómo construimos una agenda de cero, cosida a mano")], "PARTE 2 · LA COSTURA"),
 (24.0, 28.8, 1,  [(24.0,26.2,"Tenemos unas 420 hojas"),(26.2,28.8,"y unos 20 cuadernillos")], None),
 (43.7, 49.1, 1,  [(43.7,45.9,"Hacemos dos punciones en los extremos,"),(45.9,49.1,"dos en el centro y dos en el otro extremo")], None),
 (103.5,109.3, 1, [(103.5,106.3,"Enhebramos la aguja, el hilo…"),(106.3,109.3,"acá usamos una aguja curva")], None),
 (126.2,131.3, 1, [(126.2,128.8,"Siempre con cuidado"),(128.8,131.3,"para no romper las hojas ni dañarlas")], None),
 (151.8,156.4, 1, [(151.8,153.9,"Y el segundo cuadernillo:"),(153.9,156.4,"acá empezamos con la costura")], None),
 (187.9,192.5, 1, [(187.9,189.5,"Salimos en el segundo de abajo"),(189.5,192.5,"y nos encontramos con el hilo del primer cuadernillo")], None),
 (194.1,203.0, 1, [(194.1,196.0,"Acá salimos,"),(196.0,199.3,"lo pasamos por arriba al hilo del primer cuadernillo"),(199.3,201.1,"y volvemos a salir."),(201.1,203.0,"Es decir, que va a quedar enganchado")], None),
 (207.0,212.1, 1, [(207.0,209.1,"Esto es punto seguido,"),(209.1,212.1,"así hasta el otro extremo del cuadernillo")], None),
 (213.0,355.0, 40,[(213.0,355.0,"punto por punto…")], "x40"),
 (362.5,366.4, 1, [(362.5,364.0,"Con la colita tiramos…"),(364.0,366.4,"queda bien ajustado")], None),
 (405.6,412.7, 1, [(405.6,407.9,"A partir del tercer cuadernillo"),(407.9,412.7,"empezamos a hacer la costura punto alternado")], None),
 (416.0,484.0, 30,[(416.0,484.0,"enganchando con los cuadernillos de abajo…")], "x30"),
 (485.1,490.8, 1, [(485.1,487.7,"Punto alternado,"),(487.7,490.8,"porque ahora no va a ser punto seguido")], None),
 (492.0,525.5, 15,[(492.0,525.5,"…cuadernillo por cuadernillo")], "x15"),
 (526.0,534.4, 1, [(526.0,531.6,"Y así hasta terminar con todos los cuadernillos"),(531.9,534.4,"Espero que les haya servido")], None),
 (535.2,540.3, 1, [(535.2,537.0,"Nos vemos en el próximo video,"),(537.0,540.3,"cuando llegue la agenda a la prensa")], None),
]
FIN = 3.8  # segundos del cuadro final con precios
VF = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,eq=saturation=1.08:contrast=1.04"
tmp = tempfile.mkdtemp(); lst = open(f"{tmp}/l.txt","w"); t_out = 0.0; ass_lines = []
def ts(t): h=int(t//3600); m=int(t%3600//60); s=t%60; return f"{h}:{m:02d}:{s:05.2f}"
def run(c): subprocess.run(c, check=True)
for n,(a,b,sp,subs,label) in enumerate(TRAMOS):
    dur = (b-a)/sp
    if sp == 1:
        af = f"aresample=48000,aformat=channel_layouts=stereo,highpass=f=80,afftdn=nf=-25,afade=t=in:d=0.04,afade=t=out:st={dur-0.06:.3f}:d=0.06"
        run(["ffmpeg","-v","error","-y","-ss",str(a),"-t",f"{b-a}","-i",SRC,"-vf",f"fps=30,{VF}","-af",af,
             "-c:v","libx264","-crf","18","-preset","veryfast","-c:a","pcm_s16le","-t",f"{dur:.3f}",f"{tmp}/s{n}.mov"])
    else:
        run(["ffmpeg","-v","error","-y","-ss",str(a),"-t",f"{b-a}","-i",SRC,"-f","lavfi","-t",f"{dur:.3f}","-i","anullsrc=r=48000:cl=stereo",
             "-map","0:v","-map","1:a","-vf",f"setpts=PTS/{sp},fps=30,{VF}","-c:v","libx264","-crf","18","-preset","veryfast",
             "-c:a","pcm_s16le","-t",f"{dur:.3f}",f"{tmp}/s{n}.mov"])
    lst.write(f"file '{tmp}/s{n}.mov'\n")
    for (sa,sb,txt) in subs:
        ass_lines.append(f"Dialogue: 0,{ts(t_out+(sa-a)/sp)},{ts(t_out+(sb-a)/sp)},Sub,,0,0,0,,{txt}")
    if label:
        style = "Badge" if label.startswith("x") else "Top"
        ass_lines.append(f"Dialogue: 1,{ts(t_out)},{ts(t_out+dur)},{style},,0,0,0,,{label}")
    t_out += dur
# cuadro final: último fotograma + placa
run(["ffmpeg","-v","error","-y","-sseof","-0.2","-i",f"{tmp}/s{len(TRAMOS)-1}.mov","-frames:v","1","-update","1",f"{tmp}/last.png"])
run(["ffmpeg","-v","error","-y","-loop","1","-t",str(FIN),"-i",f"{tmp}/last.png","-loop","1","-t",str(FIN),"-i","overlays/end.png",
     "-f","lavfi","-t",str(FIN),"-i","anullsrc=r=48000:cl=stereo","-filter_complex",
     "[1:v]format=rgba,fade=in:st=0.1:d=0.4:alpha=1[o];[0:v][o]overlay=0:0,format=yuv420p[v]","-map","[v]","-map","2:a",
     "-c:v","libx264","-crf","18","-preset","veryfast","-r","30","-c:a","pcm_s16le","-t",str(FIN),f"{tmp}/fin.mov"])
lst.write(f"file '{tmp}/fin.mov'\n"); lst.close()
ass = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,Inter,64,&H00FFFFFF,&H00FFFFFF,&H00281E14,&H96000000,1,0,0,0,100,100,0,0,1,7,2,2,90,90,430,1
Style: Top,Inter,46,&H00FFFFFF,&H00FFFFFF,&H006B45D6,&H006B45D6,1,0,0,0,100,100,3,0,3,18,0,8,90,90,230,1
Style: Badge,Inter,44,&H00FFFFFF,&H00FFFFFF,&H00281E14,&H00281E14,1,0,0,0,100,100,0,0,3,14,0,9,60,60,150,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""" + "\n".join(ass_lines) + "\n"
open(f"{tmp}/subs.ass","w").write(ass)
run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",f"{tmp}/l.txt","-c","copy",f"{tmp}/all.mov"])
run(["ffmpeg","-v","error","-y","-i",f"{tmp}/all.mov","-vf",f"ass={tmp}/subs.ass:fontsdir=/usr/share/fonts/opentype/inter,fps=30,format=yuv420p",
     "-af","loudnorm=I=-16:TP=-1.5","-c:v","libx264","-profile:v","high","-level","4.0","-preset","slow","-crf","20","-maxrate","8M","-bufsize","16M","-g","60",
     "-c:a","aac","-b:a","160k","-ar","44100","-ac","2","-movflags","+faststart",OUT])
open(OUT.rsplit('.',1)[0]+".ass","w").write(ass) if os.environ.get("KEEP_ASS") else None
print(f"listo: {OUT} ({t_out+FIN:.1f} s)")

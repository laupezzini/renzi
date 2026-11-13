#!/usr/bin/env python3
"""Reel del cuaderno de tela que Federico saca de la prensa (con su voz, subtitulado).
Fuente: fin1.mp4 (tramo 52,45–78,3 s, una sola toma) y cuad_r.mp4 (el mismo tramo desde 50 s, con luz y piel retocadas).
Uso: python3 build_cuaderno.py FIN1.mp4 CUAD_R.mp4 SALIDA.mp4"""
import subprocess, sys, tempfile
FIN1, CUAD, OUT = sys.argv[1:4]
OFF = 50.0                       # cuad_r.mp4 empieza en el segundo 50 de fin1
PIEL = "huesaturation=saturation=-0.2:colors=r+y:strength=1,eq=gamma=1.02"
FULL = "scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,unsharp=5:5:0.5"
VOZ = "highpass=f=90,afftdn=nf=-30,acompressor=threshold=-22dB:ratio=2.5:attack=10:release=200,loudnorm=I=-16:TP=-1.5:LRA=9"
TEASER = (63.2, 1.7)             # tapa floreada (sin voz) como gancho
CUERPO = (52.45, 78.3)           # "Ahora vamos a sacar este cuaderno ..." -> "... lo hermoso"
FIN = 5.0; FIN_SRC = (64.0, 1.6)
# subtítulos de la voz (tiempos de fin1, verificados con whisper)
SUBS = [(52.55,54.70,"Ahora vamos a sacar este cuaderno"),(54.70,56.86,"que hice con una tela en particular"),
        (56.86,58.80,"que te diría que no se consigue"),(58.80,60.50,"en la ciudad de La Plata."),
        (60.50,61.52,"Me atrevo a decir eso."),(61.52,62.90,"Miren lo que es esto:"),(64.95,66.50,"es una tela."),
        (67.90,70.60,"En este caso utilicé una guarda azul"),(70.60,74.50,"y atrás le puse guarda violeta."),
        (74.95,76.60,"O sea, tiene dos tipos de guarda."),(76.60,78.30,"Miren lo que es este cuaderno, lo hermoso.")]
TITS = [(63.00,66.60,"Cuaderno de tela"),(66.60,72.30,"Guarda azul"),(72.30,74.95,"y atrás, violeta"),(74.95,78.30,"Pieza única")]
def run(c): subprocess.run(c, check=True)
def ts(t): return f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"
tmp = tempfile.mkdtemp(); enc = ["-c:v","libx264","-crf","17","-preset","veryfast","-r","30","-c:a","aac","-b:a","160k","-ar","44100","-ac","2"]
def tramo(a, d, out, afilt):
    run(["ffmpeg","-v","error","-y","-ss",f"{a-OFF:.3f}","-t",f"{d:.3f}","-i",CUAD,"-ss",f"{a:.3f}","-t",f"{d:.3f}","-i",FIN1,
         "-map","0:v","-map","1:a","-vf",f"fps=30,{FULL},setsar=1,{PIEL},format=yuv420p","-af",afilt,"-t",f"{d:.3f}"]+enc+[out])
tramo(TEASER[0], TEASER[1], f"{tmp}/a.mp4", VOZ+",volume=-6dB,afade=t=out:st=1.4:d=0.3")
tramo(CUERPO[0], CUERPO[1]-CUERPO[0], f"{tmp}/b.mp4", VOZ+f",afade=t=in:d=0.08,afade=t=out:st={CUERPO[1]-CUERPO[0]-0.25:.2f}:d=0.25")
run(["ffmpeg","-v","error","-y","-ss",f"{FIN_SRC[0]-OFF}","-t",str(FIN_SRC[1]),"-i",CUAD,"-loop","1","-t",str(FIN),"-i","overlays/cuaderno_end.png",
     "-f","lavfi","-t",str(FIN),"-i","anullsrc=r=44100:cl=stereo","-filter_complex",
     f"[0:v]setpts=PTS*{FIN/FIN_SRC[1]:.4f},fps=30,{FULL},setsar=1,{PIEL},gblur=sigma=5[v];[1:v]format=rgba,fade=in:st=0.1:d=0.4:alpha=1[o];[v][o]overlay=0:0,format=yuv420p[vo]",
     "-map","[vo]","-map","2:a","-t",str(FIN)]+enc+[f"{tmp}/c.mp4"])
# textos (tiempo de salida): teaser + cuerpo desplazado
T0 = TEASER[1]; sh = lambda t: T0 + t - CUERPO[0]
ev = [("Big",0.0,T0,"¿Una tela que no se\\Nconsigue en La Plata?")]
ev += [("Big",sh(a),sh(b),x) for a,b,x in TITS] + [("Sub",sh(a),sh(b),x) for a,b,x in SUBS]
ass = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Big,Inter,96,&H00FFFFFF,&H00FFFFFF,&H00281E14,&HA0000000,1,0,0,0,100,100,0,0,1,8,3,8,70,70,300,1
Style: Sub,Inter,56,&H00FFFFFF,&H00FFFFFF,&H006B45D6,&H006B45D6,1,0,0,0,100,100,0,0,3,16,0,2,110,110,560,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""" + "\n".join(f"Dialogue: {1 if k=='Big' else 0},{ts(a)},{ts(b)},{k},,0,0,0,,{{\\fad(120,100)}}{x}" for k,a,b,x in ev) + "\n"
open(f"{tmp}/s.ass","w").write(ass)
run(["ffmpeg","-v","error","-y","-i",f"{tmp}/a.mp4","-i",f"{tmp}/b.mp4","-i",f"{tmp}/c.mp4","-filter_complex",
     f"[0:v][0:a][1:v][1:a][2:v][2:a]concat=n=3:v=1:a=1[v][a];[v]ass={tmp}/s.ass:fontsdir=/usr/share/fonts/opentype/inter,fps=30,format=yuv420p[vo]",
     "-map","[vo]","-map","[a]","-c:v","libx264","-profile:v","high","-level","4.0","-preset","slow","-crf","20","-maxrate","8M","-bufsize","16M","-g","60",
     "-r","30","-c:a","aac","-b:a","128k","-ar","44100","-movflags","+faststart",OUT])
print("listo:", OUT, round(T0 + CUERPO[1]-CUERPO[0] + FIN, 1), "s")

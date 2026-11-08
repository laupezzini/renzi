#!/bin/bash
# Saca voces (charla, relato de fútbol de fondo) del audio de un video y deja solo los sonidos del taller.
# Uso: DEMUCS_PY=/ruta/a/python-con-demucs ./limpiar_voces.sh entrada.mp4 salida.mp4
set -e
IN=$1; OUT=$2; PY=${DEMUCS_PY:-python3}; TMP=$(mktemp -d)
ffmpeg -v error -y -i "$IN" -vn -ac 2 -ar 44100 $TMP/audio.wav
$PY -m demucs --two-stems=vocals -n htdemucs -o $TMP/sep $TMP/audio.wav >/dev/null 2>&1
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$IN")
ffmpeg -v error -y -i "$IN" -i $TMP/sep/htdemucs/audio/no_vocals.wav -map 0:v -map 1:a -c:v copy \
  -af "highpass=f=90,loudnorm=I=-20:TP=-2,afade=t=out:st=$(python3 -c "print($D-0.8)"):d=0.8" -c:a aac -b:a 192k -shortest -movflags +faststart "$OUT"
rm -rf $TMP; echo "listo: $OUT"

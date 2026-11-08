#!/bin/bash
# Re-exporta un video para que lo acepten WhatsApp e Instagram:
# 30 fps constantes, H.264 High 4.0, yuv420p, AAC 44,1 kHz estéreo, siempre con pista de audio.
set -e
IN=$1; OUT=$2
if ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "$IN" | grep -q .; then
  AIN=(-i "$IN"); AMAP="0:a:0"
else
  AIN=(-f lavfi -i anullsrc=r=44100:cl=stereo); AMAP="1:a"
fi
ffmpeg -v error -y -i "$IN" "${AIN[@]}" -map 0:v:0 -map $AMAP -shortest \
  -vf "fps=30,format=yuv420p" -c:v libx264 -profile:v high -level 4.0 -preset slow -crf 20 -maxrate 8M -bufsize 16M -g 60 \
  -c:a aac -b:a 160k -ar 44100 -ac 2 -movflags +faststart "$OUT"
echo "listo: $OUT"

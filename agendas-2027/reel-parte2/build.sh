#!/bin/bash
# Reel "Parte 2: la costura". Uso: SRC=video_original.mp4 OUT=salida.mp4 ./build.sh
set -e
SRC=${SRC:?}; OUT=${OUT:-reel-parte2.mp4}
TMP=$(mktemp -d); LIST=$TMP/list.txt; : > $LIST; i=0
VF="scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,eq=saturation=1.08:contrast=1.04"
seg() { # inicio duración_original velocidad placa
  local OUTD=$(python3 -c "print(round($2/$3,3))")
  ffmpeg -v error -y -ss $1 -t $2 -i "$SRC" -loop 1 -t $OUTD -i overlays/$4.png \
    -filter_complex "[0:v]setpts=PTS/$3,fps=30,$VF[v];[1:v]format=rgba,fade=in:st=0.05:d=0.2:alpha=1[o];[v][o]overlay=0:0:shortest=1,format=yuv420p[vo]" \
    -map "[vo]" -t $OUTD -an -c:v libx264 -crf 18 -preset veryfast -r 30 $TMP/s$i.mp4
  echo "file '$TMP/s$i.mp4'" >> $LIST; i=$((i+1)); }
seg 105.0 2.6 1   p1    # gancho: enhebrando la aguja
seg 14.0 16.0 4   p2    # ordena los cuadernillos "2027"
seg 41.0 6.0 2    p3    # marca las puntadas con la regla
seg 110.0 4.0 1.3 p4    # aguja e hilo
seg 120.0 15.0 3  p5    # empieza a coser el primer cuadernillo
seg 140.0 360.0 60 p6   # la costura completa, acelerada
seg 509.0 8.0 2   p7    # tira del hilo
seg 531.6 2.2 1   p8    # pulgar arriba
# cierre: cuadro fijo del pulgar arriba con la placa final
ffmpeg -v error -y -ss 533.4 -i "$SRC" -frames:v 1 -vf "$VF" $TMP/last.png
ffmpeg -v error -y -loop 1 -t 4 -i $TMP/last.png -loop 1 -t 4 -i overlays/end.png \
  -filter_complex "[0:v]scale=1188:2112,zoompan=z='1+0.0008*on':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d=120:s=1080x1920:fps=30,setsar=1[v];[1:v]format=rgba,fade=in:st=0.15:d=0.4:alpha=1[o];[v][o]overlay=0:0,format=yuv420p" \
  -t 4 -an -c:v libx264 -crf 18 -preset veryfast -r 30 $TMP/s$i.mp4
echo "file '$TMP/s$i.mp4'" >> $LIST
ffmpeg -v error -y -f concat -safe 0 -i $LIST -c copy $TMP/video.mp4
ffmpeg -v error -y -i $TMP/video.mp4 -f lavfi -i anullsrc=r=44100:cl=stereo -map 0:v -map 1:a -shortest \
  -vf "fps=30,format=yuv420p" -c:v libx264 -profile:v high -level 4.0 -preset slow -crf 20 -maxrate 8M -bufsize 16M -g 60 \
  -c:a aac -b:a 128k -movflags +faststart "$OUT"
rm -rf $TMP; echo "listo: $OUT ($(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT") s)"

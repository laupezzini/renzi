#!/bin/bash
# Reel de venta de agendas 2027. Uso: SRC=carpeta_videos FINAL=foto_final_1350x2400.jpg OUT=salida.mp4 ./build.sh
set -e
SRC=${SRC:?}; FINAL=${FINAL:?}; OUT=${OUT:-reel-venta.mp4}
TMP=$(mktemp -d); LIST=$TMP/list.txt; : > $LIST; i=0
VF="scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1,eq=saturation=1.08:contrast=1.03"
clip() { # archivo inicio duración placa
  ffmpeg -v error -y -ss $2 -t $3 -i "$SRC/$1" -loop 1 -t $3 -i overlays/$4.png \
    -filter_complex "[0:v]$VF[v];[1:v]format=rgba,fade=in:st=0.08:d=0.2:alpha=1[o];[v][o]overlay=0:0:shortest=1,format=yuv420p[vo];[0:a]aresample=48000,aformat=channel_layouts=stereo,afade=t=in:d=0.06,afade=t=out:st=$(python3 -c "print($3-0.1)"):d=0.1[ao]" \
    -map "[vo]" -map "[ao]" -t $3 -c:v libx264 -crf 17 -preset medium -r 30 -c:a pcm_s16le $TMP/s$i.mov
  echo "file '$TMP/s$i.mov'" >> $LIST; i=$((i+1)); }
still() { # imagen duración [placa]
  local OV=(); local F="[0:v]scale=1188:2112,zoompan=z='1+0.0008*on':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d=$(python3 -c "print(int($2*30))"):s=1080x1920:fps=30,setsar=1"
  if [ -n "$3" ]; then OV=(-loop 1 -t $2 -i overlays/$3.png); F="$F[v];[2:v]format=rgba,fade=in:st=0.2:d=0.4:alpha=1[o];[v][o]overlay=0:0"; fi
  ffmpeg -v error -y -loop 1 -t $2 -i "$1" -f lavfi -t $2 -i anullsrc=r=48000:cl=stereo "${OV[@]}" \
    -filter_complex "$F,format=yuv420p[vo]" -map "[vo]" -map 1:a -t $2 -c:v libx264 -crf 17 -preset medium -r 30 -c:a pcm_s16le $TMP/s$i.mov
  echo "file '$TMP/s$i.mov'" >> $LIST; i=$((i+1)); }
clip IMG_7386.MP4 21.9 2.3 v1      # gancho: pila de cuadernillos
clip IMG_7374.MOV 0.2 2.4 v2       # Federico se presenta
clip IMG_7377.MOV 11.5 2.0 v3
clip IMG_7377.MOV 32.5 2.4 v4
clip IMG_7386.MP4 17.0 2.2 v5
clip IMG_7386.MP4 10.6 1.8 v6
clip IMG_7384.MP4 5.8 2.1 v7
still overlays/tapa1.png 2.1
still overlays/tapa2.png 2.1
still overlays/tapa3.png 2.1
still "$FINAL" 3.8 end
ffmpeg -v error -y -f concat -safe 0 -i $LIST -c copy "$OUT"
rm -rf $TMP; echo "listo: $OUT ($(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT") s)"

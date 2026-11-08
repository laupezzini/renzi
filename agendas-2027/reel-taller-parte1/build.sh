#!/bin/bash
# Arma el reel "Taller parte 1" a partir de los videos crudos (carpeta $SRC) y las placas de overlays/.
set -e
SRC=${SRC:?carpeta con los videos IMG_73xx}
FINAL=${FINAL:?foto final recortada 1350x2400}
OUT=${OUT:-renzi-agendas-2027-taller-parte1.mp4}
TMP=$(mktemp -d)
# archivo inicio duración placa
SEGS=(
"IMG_7374.MOV 0.2 2.4 c1"
"IMG_7374.MOV 9.6 2.2 c2"
"IMG_7377.MOV 11.5 3.0 c3"
"IMG_7379.MOV 11.8 2.2 c4"
"IMG_7377.MOV 32.5 3.0 c5"
"IMG_7386.MP4 17.0 2.6 c6"
"IMG_7386.MP4 21.6 2.6 c7"
"IMG_7384.MP4 5.6 2.3 c8"
"IMG_7380.MOV 29.2 3.2 c9"
)
VF="scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1,eq=saturation=1.08:contrast=1.03"
i=0; LIST=$TMP/list.txt; : > $LIST
for s in "${SEGS[@]}"; do set -- $s
  ffmpeg -v error -y -ss $2 -t $3 -i "$SRC/$1" -loop 1 -t $3 -i overlays/$4.png \
    -filter_complex "[0:v]$VF[v];[1:v]format=rgba,fade=in:st=0.1:d=0.25:alpha=1[o];[v][o]overlay=0:0:shortest=1,format=yuv420p" \
    -an -c:v libx264 -crf 17 -preset medium -r 30 $TMP/s$i.mp4
  echo "file '$TMP/s$i.mp4'" >> $LIST; i=$((i+1))
done
# foto final con zoom lento + placa de cierre
ffmpeg -v error -y -loop 1 -t 4 -i "$FINAL" -loop 1 -t 4 -i overlays/end.png \
  -filter_complex "[0:v]scale=1350:2400,zoompan=z='1+0.0009*on':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/3':d=120:s=1080x1920:fps=30,setsar=1[v];[1:v]format=rgba,fade=in:st=0.3:d=0.5:alpha=1[o];[v][o]overlay=0:0,format=yuv420p" \
  -t 4 -an -c:v libx264 -crf 17 -preset medium -r 30 $TMP/s$i.mp4
echo "file '$TMP/s$i.mp4'" >> $LIST
ffmpeg -v error -y -f concat -safe 0 -i $LIST -c copy $TMP/video.mp4
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $TMP/video.mp4)
ffmpeg -v error -y -i $TMP/video.mp4 -i musica.wav -filter_complex "[1:a]atrim=0:$D,afade=t=in:d=0.3,afade=t=out:st=$(python3 -c "print($D-1.5)"):d=1.5[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -movflags +faststart -shortest "$OUT"
rm -rf $TMP
echo "listo: $OUT ($D s)"

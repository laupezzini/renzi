# Uso: retoque_video.py ENTRADA SALIDA INICIO DURACION
# Luz con parámetros fijos por clip (sin parpadeo) + suavizado de piel en las manos.
import cv2, numpy as np, subprocess, sys
sys.path.insert(0, sys.path[0]); from retoque import mascara_piel
src, out, a, d = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
import tempfile, os; _t = tempfile.mktemp(suffix=".png"); subprocess.run(["ffmpeg","-v","error","-y","-ss",a,"-i",src,"-frames:v","1",_t], check=True); h, w = cv2.imread(_t).shape[:2]; os.remove(_t)
dec = subprocess.Popen(["ffmpeg","-v","error","-ss",a,"-t",d,"-i",src,"-f","rawvideo","-pix_fmt","bgr24","-r","30","-"], stdout=subprocess.PIPE)
enc = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s",f"{w}x{h}","-r","30","-i","-","-c:v","libx264","-crf","14","-preset","veryfast","-pix_fmt","yuv420p",out], stdin=subprocess.PIPE)
frames = []
while True:
    b = dec.stdout.read(w*h*3)
    if len(b) < w*h*3: break
    frames.append(np.frombuffer(b, np.uint8).reshape(h, w, 3))
# parámetros de luz a partir de varios cuadros del clip
ref = np.concatenate([frames[i].reshape(-1,3) for i in np.linspace(0, len(frames)-1, 5).astype(int)]).astype(np.float32)
lum = ref.mean(1); wb = ref[lum > np.percentile(lum, 92)].mean(0); gain = wb.mean() / wb
gain = 1 + (gain - 1) * 0.8                      # balance un poco más suave
hi = np.percentile(ref * gain, 99.5)
lut = [np.clip(np.power(np.clip(np.arange(256)*g/hi*245, 0, 255)/255, 0.85)*255, 0, 255).astype(np.uint8) for g in gain]
for f in frames:
    l = np.dstack([cv2.LUT(f[...,c], lut[c]) for c in range(3)])
    m = mascara_piel(l)
    s = cv2.bilateralFilter(l, 9, 50, 9); s = cv2.bilateralFilter(s, 9, 40, 9)
    s = cv2.addWeighted(s, 0.65, cv2.GaussianBlur(s, (0,0), 3), 0.35, 0)
    hsv = cv2.cvtColor(s, cv2.COLOR_BGR2HSV).astype(np.float32); hsv[...,1] *= 0.85; hsv[...,2] = np.clip(hsv[...,2]*1.05, 0, 255)
    s = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
    k = m * 0.9
    enc.stdin.write((l*(1-k) + s*k).astype(np.uint8).tobytes())
enc.stdin.close(); enc.wait(); print(out, len(frames), gain.round(3), round(float(hi),1))

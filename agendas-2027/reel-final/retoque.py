# Retoque: luz (niveles + balance de blancos) y suavizado de piel en las manos.
import cv2, numpy as np, sys
def luz(img):
    f = img.astype(np.float32)
    # balance de blancos: lo más claro (papel) tiene que ser neutro
    lum = f.mean(2); m = lum > np.percentile(lum, 92)
    ref = f[m].mean(0); f *= ref.mean() / ref
    # niveles: punto blanco en el percentil 99,5 y algo más de medios
    hi = np.percentile(f, 99.5); f = np.clip(f / hi * 245, 0, 255) / 255.0
    f = np.power(f, 0.85)
    return np.clip(f * 255, 0, 255).astype(np.uint8)
def mascara_piel(img):
    ycc = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb); hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    y, cr, cb = cv2.split(ycc); s = hsv[...,1]
    m = ((cr > 138) & (cr < 178) & (cb > 82) & (cb < 128) & (s > 35) & (y > 60)).astype(np.uint8) * 255
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((5,5),np.uint8)); m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((9,9),np.uint8))
    return cv2.GaussianBlur(m, (21,21), 0).astype(np.float32)[...,None] / 255.0
def piel(img, fuerza=0.85):
    m = mascara_piel(img)
    suave = cv2.bilateralFilter(img, 9, 45, 9); suave = cv2.bilateralFilter(suave, 9, 35, 9)
    # quita manchas/venas: baja el detalle fino y empareja el tono
    base = cv2.GaussianBlur(suave, (0,0), 3)
    suave = cv2.addWeighted(suave, 0.7, base, 0.3, 0)
    hsv = cv2.cvtColor(suave, cv2.COLOR_BGR2HSV).astype(np.float32); hsv[...,1] *= 0.88; hsv[...,2] = np.clip(hsv[...,2]*1.04, 0, 255)
    suave = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
    out = img.astype(np.float32) * (1 - m * fuerza) + suave.astype(np.float32) * (m * fuerza)
    return out.astype(np.uint8), m
if __name__ == "__main__":
    for f in sys.argv[1:]:
        im = cv2.imread(f); l = luz(im); r, m = piel(l)
        cv2.imwrite(f.replace('orig_','luz_'), l); cv2.imwrite(f.replace('orig_','ret_'), r); cv2.imwrite(f.replace('orig_','mask_'), (m[...,0]*255).astype(np.uint8))

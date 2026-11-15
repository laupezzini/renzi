#!/usr/bin/env python3
"""Diseño de sonido del reel de Navidad (todo sintetizado, sin samples ni música).
Uso: python3 sfx.py salida.wav"""
import numpy as np, sys, wave
SR=44100; DUR=27.2; rng=np.random.default_rng(7)
out=np.zeros((int(SR*DUR)+SR,2))
# misma curva de ritmo que navidad.html (tiempo de la animación -> tiempo de salida)
K_OUT=[0,2.4,5.3,8.2,11.1,14.0,16.9,19.8,21.8,23.4,27.2]; K_IN=[0,3.0,6.6,10.2,13.8,17.4,21.0,24.6,27.2,29.2,33]
def T(t): return float(np.interp(t,K_IN,K_OUT))
def env(n,a,d): x=np.arange(n)/SR; return np.minimum(1,x/max(a,1e-4))*np.exp(-x/d)
def put(sig,t,gain=1.0,pan=0.0):
    i=int(T(t)*SR); sig=sig*gain
    if sig.ndim==1: sig=np.stack([sig*(1-pan)**.5*1.0,sig*(1+pan)**.5*1.0],1)/1.41
    n=min(len(sig),len(out)-i); out[i:i+n]+=sig[:n]
def lp(x,k):  # paso bajo simple (media móvil)
    return np.convolve(x,np.ones(k)/k,'same')
def whoosh(d=.28):
    n=int(SR*d); x=rng.standard_normal(n); x=lp(x,6)-lp(x,40); e=np.sin(np.linspace(0,np.pi,n))**2
    return x*e*.5
def thud():
    n=int(SR*.22); t=np.arange(n)/SR; f=110*np.exp(-t*8)+55; ph=2*np.pi*np.cumsum(f)/SR
    return (np.sin(ph)*env(n,.003,.07)+lp(rng.standard_normal(n),20)*env(n,.001,.02)*.6)*.9
def pop():
    n=int(SR*.12); t=np.arange(n)/SR; f=900*np.exp(-t*30)+250; ph=2*np.pi*np.cumsum(f)/SR
    return np.sin(ph)*env(n,.001,.035)*.8+rng.standard_normal(n)*env(n,.0005,.004)*.4
def tick():
    n=int(SR*.09); t=np.arange(n)/SR
    return (np.sin(2*np.pi*1250*t)+.5*np.sin(2*np.pi*3100*t))*env(n,.0005,.018)*.45
def bell(f,d=1.4,g=1.0):
    n=int(SR*d); t=np.arange(n)/SR; s=np.zeros(n)
    for m,a,dd in ((1,1,.9),(2.76,.45,.45),(5.4,.25,.25),(8.9,.12,.12)): s+=a*np.sin(2*np.pi*f*m*t)*np.exp(-t/(dd*d))
    return s*env(n,.002,10)*.35*g
def sparkle(base=1568):
    notes=[1,1.25,1.5,2,2.5,3]; s=np.zeros(int(SR*1.2))
    for k,m in enumerate(notes):
        b=bell(base*m,.6,.6); i=int(SR*.045*k); s[i:i+len(b)]+=b[:len(s)-i]
    return s
def jingle(d=1.2):  # cascabeles: ráfagas de ruido agudo filtrado
    n=int(SR*d); s=np.zeros(n)
    for k in range(int(d*14)):
        i=int(k*SR/14+rng.integers(0,600)); m=int(SR*.06)
        if i+m>n: break
        x=rng.standard_normal(m); x=x-lp(x,4); s[i:i+m]+=x*env(m,.001,.012)*(.5+.5*rng.random())
        for f in (5200,6900): s[i:i+m]+=np.sin(2*np.pi*f*np.arange(m)/SR)*env(m,.001,.02)*.15
    return s*np.sin(np.linspace(0,np.pi,n))*.5
# --- eventos (tiempos de la animación, igual que en navidad.html) ---
put(jingle(1.6),0.0,.55)
for t in (.05,.35,.8): put(whoosh(),t,.6)
put(thud(),.95,.9); put(bell(1046.5,1.2),1.05,.5)
personas=[3.0,6.6,10.2,13.8,17.4]; bases=[1568,1760,1568,1397,1760]
for a,b in zip(personas,bases):
    put(whoosh(),a+.05,.55,-.2); put(whoosh(),a+.3,.5,.2)
    put(thud(),a+.55,.8); put(pop(),a+.95,.8,.15); put(sparkle(b),a+1.15,.6)
    put(tick(),a+1.45,.8)
put(whoosh(),21.05,.55); put(whoosh(),21.35,.5)
for k,(t,f) in enumerate(((21.6,1046.5),(21.8,1318.5),(22.0,1568))): put(bell(f,1.0),t,.55,(k-1)*.4)
put(bell(784,2.2),24.8,.7); put(bell(1568,1.6),24.85,.35)
for t in (25.1,25.4,25.8): put(tick(),t,.4)
put(whoosh(.35),27.3,.6); put(whoosh(),27.5,.5)
put(tick(),28.1,.6)
for k,f in enumerate((1046.5,1318.5,1568,2093)): put(bell(f,2.0),28.4+k*.07,.55,(k-1.5)*.3)
put(jingle(1.8),28.5,.4); put(tick(),29.1,.5)
# --- reverb simple (respuesta al impulso de ruido con caída) ---
ir=rng.standard_normal(int(SR*.7))*np.exp(-np.arange(int(SR*.7))/SR/.18); ir/=np.abs(ir).sum()/6
for c in range(2):
    wet=np.fft.irfft(np.fft.rfft(out[:,c],len(out)+len(ir))*np.fft.rfft(ir,len(out)+len(ir)))[:len(out)]
    out[:,c]=out[:,c]*.85+wet*.25
out=out[:int(SR*DUR)]; out/=np.abs(out).max()/0.8
f=out[:int(SR*DUR)]; fade=int(SR*.6); f[-fade:]*=np.linspace(1,0,fade)[:,None]
w=wave.open(sys.argv[1],'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((f*32767).astype('<i2').tobytes()); w.close()
print("ok", sys.argv[1])

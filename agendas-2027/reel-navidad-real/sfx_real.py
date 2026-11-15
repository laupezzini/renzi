#!/usr/bin/env python3
"""Sonidos del reel de Navidad real: barrido en cada corte, golpe al entrar cada regalo, tic + destello en los precios,
cascabeles al inicio y acorde de campanas en el cierre. Todo sintetizado. Uso: python3 sfx_real.py eventos.json salida.wav"""
import numpy as np, sys, json, wave
ev=json.load(open(sys.argv[1])); SR=44100; rng=np.random.default_rng(3)
out=np.zeros((int(SR*(ev["total"]+1)),2))
def env(n,a,d): x=np.arange(n)/SR; return np.minimum(1,x/max(a,1e-4))*np.exp(-x/d)
def lp(x,k): return np.convolve(x,np.ones(k)/k,'same')
def put(sig,t,g=1.0,pan=0.0):
    i=int(t*SR); n=min(len(sig),len(out)-i)
    if n<=0 or i<0: return
    out[i:i+n,0]+=sig[:n]*g*(1-pan)*.8; out[i:i+n,1]+=sig[:n]*g*(1+pan)*.8
def whoosh(d=.22):
    n=int(SR*d); x=rng.standard_normal(n); f=np.linspace(4,30,n).astype(int); y=np.array([0.0]*n)
    y=lp(x,8)-lp(x,60); e=np.sin(np.linspace(0,np.pi,n))**3; return y*e*.6
def boom():
    n=int(SR*.35); t=np.arange(n)/SR; ph=2*np.pi*np.cumsum(70*np.exp(-t*6)+42)/SR
    return np.sin(ph)*env(n,.002,.12)*1.0+lp(rng.standard_normal(n),12)*env(n,.0005,.015)*.5
def pop():
    n=int(SR*.1); t=np.arange(n)/SR; ph=2*np.pi*np.cumsum(1000*np.exp(-t*35)+300)/SR
    return np.sin(ph)*env(n,.001,.03)*.7
def tick():
    n=int(SR*.08); t=np.arange(n)/SR; return (np.sin(2*np.pi*1300*t)+.5*np.sin(2*np.pi*3200*t))*env(n,.0005,.016)*.5
def bell(f,d=1.2,g=1.0):
    n=int(SR*d); t=np.arange(n)/SR; s=np.zeros(n)
    for m,a,dd in ((1,1,.9),(2.76,.45,.45),(5.4,.25,.25),(8.9,.1,.1)): s+=a*np.sin(2*np.pi*f*m*t)*np.exp(-t/(dd*d))
    return s*np.minimum(1,t/.002)*.3*g
def sparkle(b):
    s=np.zeros(int(SR*1.0))
    for k,m in enumerate((1,1.25,1.5,2)): x=bell(b*m,.5,.5); i=int(SR*.04*k); s[i:i+len(x)]+=x[:len(s)-i]
    return s
def jingle(d=1.4):
    n=int(SR*d); s=np.zeros(n)
    for k in range(int(d*16)):
        i=int(k*SR/16+rng.integers(0,500)); m=int(SR*.05)
        if i+m>n: break
        x=rng.standard_normal(m); x=x-lp(x,4); s[i:i+m]+=x*env(m,.001,.01)*(.5+.5*rng.random())
        s[i:i+m]+=np.sin(2*np.pi*6100*np.arange(m)/SR)*env(m,.001,.02)*.15
    return s*np.sin(np.linspace(0,np.pi,n))*.45
put(jingle(),0.0,.8); put(boom(),0.0,.9)
for i,c in enumerate(ev["cuts"]): put(whoosh(),c-0.11,.55,(-.3 if i%2 else .3))
for p in ev["personas"]+[ev["vos"],ev["mano"]]: put(boom(),p+0.02,.75); put(pop(),p+0.12,.45)
for k,l in enumerate(ev["labels"]): put(tick(),l,.8); put(sparkle([1568,1760,1397,1568,1760,1568][k%6]),l+.03,.45)
for k,f in enumerate((1046.5,1318.5,1568,2093)): put(bell(f,2.2),ev["cta"]+.3+k*.07,.6,(k-1.5)*.25)
put(jingle(1.8),ev["cta"]+.35,.4)
ir=rng.standard_normal(int(SR*.6))*np.exp(-np.arange(int(SR*.6))/SR/.15); ir/=np.abs(ir).sum()/5
for c in range(2):
    L=len(out)+len(ir); wet=np.fft.irfft(np.fft.rfft(out[:,c],L)*np.fft.rfft(ir,L))[:len(out)]; out[:,c]=out[:,c]*.85+wet*.22
o=out[:int(SR*ev["total"])]; o/=np.abs(o).max()/.85; fd=int(SR*.5); o[-fd:]*=np.linspace(1,0,fd)[:,None]
w=wave.open(sys.argv[2],'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((o*32767).astype('<i2').tobytes()); w.close()

#!/usr/bin/env python3
"""Pista de voz chistosa del reel POV: ubica cada frase en su toma y suma un "tadá" de campanitas en la revelación.
Uso: python3 mezcla_voz2.py salida.wav"""
import numpy as np, soundfile as sf, sys
SR=44100; TOTAL=23.95
def load(p):
    a,sr=sf.read(p,dtype='float32')
    if a.ndim>1: a=a.mean(1)
    if sr!=SR: a=np.interp(np.arange(0,len(a),sr/SR),np.arange(len(a)),a).astype('float32')
    return a
out=np.zeros(int(SR*TOTAL)+SR,dtype='float32')
def put(sig,t,g=1.0): i=int(t*SR); out[i:i+len(sig)]+=sig[:len(out)-i]*g
EV=[("A",0.12),("b_h",3.9),("b_t",5.95),("e_h",7.4),("e_t",8.55),("g_h",9.9),("g_t",12.75),("I",13.85),("J",17.5),("K",19.65)]
for n,t in EV: put(load(f"voz2/{n}.wav"),t)
def bell(f,d=1.0):
    t=np.arange(int(SR*d))/SR; s=sum(a*np.sin(2*np.pi*f*m*t)*np.exp(-t/(dd*d)) for m,a,dd in ((1,1,.8),(2.76,.4,.4),(5.4,.2,.2)))
    return (s*np.minimum(1,t/.003)).astype('float32')
for k,f in enumerate((1046.5,1318.5,1568,2093)): put(bell(f)*0.08,13.7+k*0.07)
out=out[:int(SR*TOTAL)]; sf.write(sys.argv[1],out,SR)

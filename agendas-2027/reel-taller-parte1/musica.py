import numpy as np, wave, sys
sr=44100; dur=float(sys.argv[2]) if len(sys.argv)>2 else 16.5; N=int(sr*dur); rng=np.random.default_rng(7)
out=np.zeros((N,2))
def hz(m): return 440*2**((m-69)/12)
def pluck(m, t0, length=2.2, amp=0.28, bright=0.5):
    f=hz(m); n=int(sr*length); p=int(sr/f)
    buf=rng.uniform(-1,1,p)
    # soften attack
    for _ in range(int(3*(1-bright))+1): buf=0.5*(buf+np.roll(buf,1))
    y=np.zeros(n); y[:p]=buf
    for i in range(p,n): y[i]=0.996*0.5*(y[i-p]+y[i-p+1 if i-p+1<i else i-p])
    y*=np.exp(-np.arange(n)/sr*1.2)*amp
    return y
def add(sig,t0,pan=0.0):
    i=int(t0*sr); j=min(N,i+len(sig)); s=sig[:j-i]
    out[i:j,0]+=s*(1-pan)/1.0*0.9; out[i:j,1]+=s*(1+pan)/1.0*0.9
bpm=84; beat=60/bpm; bar=4*beat
chords=[[48,55,60,64,67],[47,55,59,62,67],[45,52,57,60,64],[41,48,53,57,60],[48,55,60,64,67],[43,50,55,59,62]]  # C G/B Am F C G
pattern=[0,2,3,4,3,2,3,4]
for b in range(int(dur/(4*60/84))+1):
    ch=chords[b%len(chords)]
    t=b*bar
    if t>dur: break
    for k,idx in enumerate(pattern):
        tt=t+k*beat/2
        if tt<dur-0.3: add(pluck(ch[idx],tt,amp=0.22 if k else 0.3,bright=0.4), tt, pan=(-0.3 if idx<2 else 0.25))
    # soft pad
    n=int(bar*sr)+sr; tt=np.arange(n)/sr
    env=np.minimum(1,tt/0.8)*np.exp(-np.maximum(0,tt-bar)/0.6)
    pad=sum(np.sin(2*np.pi*hz(m+12)*tt)*0.5+np.sin(2*np.pi*hz(m+12)*1.003*tt)*0.5 for m in ch[2:])*env*0.025
    add(pad,t)
# bell melody (sparse)
mel0=[(1.0,76),(1.7,79),(2.4,76),(3.4,74),(4.1,74),(4.8,71),(6.7,72),(7.4,76),(8.1,72),(9.8,69),(10.5,72),(11.4,77),(12.1,76),(12.8,72),(14.2,79),(14.9,76)]
mel=[(t+o,m) for o in (0,16.0) for t,m in mel0 if t+o<dur-1.5]
for t,m in mel:
    n=int(1.6*sr); tt=np.arange(n)/sr; f=hz(m)
    s=(np.sin(2*np.pi*f*tt)+0.25*np.sin(2*np.pi*f*2.76*tt)*np.exp(-tt*6))*np.exp(-tt*2.2)*0.06
    add(s,t,pan=0.15)
# simple reverb (comb filters)
def comb(x,d,g):
    y=x.copy(); d=int(d*sr)
    for i in range(d,len(y)): y[i]+=g*y[i-d]
    return y
for ch in range(2):
    x=out[:,ch].copy()
    r=sum(comb(x,d,0.55) for d in ([0.0297,0.0371,0.0411,0.0437] if ch==0 else [0.0301,0.0367,0.0417,0.0443]))/4
    out[:,ch]=x*0.75+r*0.35
# fade in/out, normalize
t=np.arange(N)/sr
out*=np.minimum(1,t/0.15)[:,None]*np.clip((dur-t)/1.5,0,1)[:,None]
out/=np.max(np.abs(out))*1.12
w=wave.open(sys.argv[1],'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
w.writeframes((out*32767).astype('<i2').tobytes()); w.close()

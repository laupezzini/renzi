# Genera las placas de texto (PNG transparentes 1080x1920) del reel "Taller parte 1".
caps = {
 "c1": ("top", "PARTE 1", "Así nace tu<br><b>agenda 2027</b>"),
 "c2": ("low", None, "abrimos el paquete…"),
 "c3": ("low", None, "revisamos cada hoja"),
 "c4": ("low", None, "un día por página"),
 "c5": ("low", None, "doblamos a mano, hoja por hoja"),
 "c6": ("low", None, "con plegadera, para un doblez perfecto"),
 "c7": ("low", None, "cuadernillos listos para coser"),
 "c8": ("low", None, "y el sello de la casa"),
 "c9": ("low", None, "¡ya casi está!"),
 "c10": ("low", None, "Próximamente · Parte 2: la costura 🧵"),
}
css = '''@font-face{font-family:P;src:url(playfair-700.woff2);font-weight:700}
@font-face{font-family:Pi;src:url(playfair-500i.woff2)}
@font-face{font-family:D;src:url(dmsans-800.woff2);font-weight:800}
@font-face{font-family:Ds;src:url(dancing-700.woff2)}
html,body{margin:0;width:1080px;height:1920px;background:transparent}
.low{position:absolute;left:0;right:0;bottom:330px;display:flex;justify-content:center}
.low span{background:rgba(255,253,248,.94);color:#2f5d46;font-family:D;font-weight:800;font-size:58px;padding:22px 44px 26px;border-radius:999px;box-shadow:0 10px 30px rgba(0,0,0,.25);max-width:900px;text-align:center}
.top{position:absolute;left:0;right:0;bottom:300px;text-align:center}
.top .k{display:inline-block;background:#d6456b;color:#fff;font-family:D;font-weight:800;font-size:34px;letter-spacing:6px;padding:10px 26px 12px;border-radius:999px}
.top .t{margin-top:22px;font-family:Ds;font-size:96px;color:#fff;line-height:1.05;text-shadow:0 4px 24px rgba(0,0,0,.55)}
.top .t b{font-family:P;font-weight:700;font-size:118px}
.end{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,0) 52%,rgba(20,30,25,.85) 80%)}
.end .box{position:absolute;left:60px;right:60px;bottom:150px;text-align:center;color:#fff}
.end .k{display:inline-block;background:#fffdf8;color:#2f5d46;font-family:D;font-weight:800;font-size:34px;padding:12px 30px 14px;border-radius:999px}
.end .t{font-family:Ds;font-size:92px;margin-top:22px;line-height:1}
.end .p{font-family:P;font-weight:700;font-size:72px;margin-top:14px}
.end .p em{font-family:D;font-style:normal;font-weight:800;color:#ff9fb6}
.end .w{margin-top:34px;font-family:D;font-weight:800;font-size:46px}
.end .ig{font-family:D;font-size:34px;opacity:.9;margin-top:8px}
'''
html = {}
for k,(kind,kick,txt) in caps.items():
    if kind=="top":
        body=f'<div class="top"><div class="k">{kick}</div><div class="t">{txt}</div></div>'
    else:
        body=f'<div class="low"><span>{txt}</span></div>'
    html[k]=body
html["end"]='''<div class="end"><div class="box"><div class="k">HECHAS A MANO, UNA POR UNA</div>
<div class="t">Agendas 2027</div><div class="p">preventa desde <em>$40.000</em></div>
<div class="ig" style="font-family:Pi;font-size:40px;margin-top:10px">papel · tela · cuero — hasta el 20/11</div>
<div class="w">WhatsApp 221 577-0018</div><div class="ig">@renzi.librosusados</div></div></div>'''
for k,b in html.items():
    open(f"{k}.html","w").write(f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>{b}</body></html>')

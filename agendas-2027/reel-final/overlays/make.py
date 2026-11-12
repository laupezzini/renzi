# Placas del reel final "Agenda terminada" (PNG 1080x1920 transparentes).
low = {"r2":"doblamos ✋","r3":"cosimos 🧵","r4":"encolamos 🖌️",
       "f2":"guardas azules por dentro 💙","f3":"dos cintas para marcar tus días","f4":"más de 400 páginas, un día por página"}
css = open('../../reel-venta/overlays/make.py').read().split("css = '''")[1].split("'''")[0]
css += '''.pr{font-family:D;font-size:38px;white-space:nowrap;margin-top:16px}.pr em{font-style:normal;color:#ffb3c4}
.hook.b{top:auto;bottom:0;height:900px;background:linear-gradient(0deg,rgba(15,25,20,.85),rgba(15,25,20,0));padding-top:420px}'''
pages = {k: f'<div class="low"><span>{t}</span></div>' for k,t in low.items()}
pages["r1"] = '<div class="hook"><div class="a">De esto…</div></div>'
pages["f1"] = '<div class="hook b"><div class="a">…a esto ✨</div><div class="b">tu agenda 2027, terminada</div></div>'
pages["end"] = '''<div class="end"><div class="box"><div class="k">ÚLTIMOS DÍAS · PREVENTA HASTA EL 20/11</div>
<div class="t">Agendas 2027<br>hechas a mano</div>
<div class="pr">Papel <em>$40.000</em> · Tela <em>$45.000</em> · Cuero <em>$65.000</em></div>
<div class="cta">Escribí <b>AGENDA</b> por DM</div>
<div class="w">o al WhatsApp 221 577-0018 · @renzi.librosusados</div></div></div>'''
for k,b in pages.items():
    open(f"{k}.html","w").write(f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>{b}</body></html>')

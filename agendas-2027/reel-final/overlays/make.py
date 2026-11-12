# Placas del reel final "Agenda terminada" (PNG 1080x1920 transparentes).
low = {}
css = open('../../reel-venta/overlays/make.py').read().split("css = '''")[1].split("'''")[0]
css += '''.pr{font-family:D;font-size:38px;white-space:nowrap;margin-top:16px}.pr em{font-style:normal;color:#ffb3c4}
.hook.b{top:auto;bottom:0;height:900px;background:linear-gradient(0deg,rgba(15,25,20,.85),rgba(15,25,20,0));padding-top:420px}'''
pages = {k: f'<div class="low"><span>{t}</span></div>' for k,t in low.items()}
pages["end"] = '''<div class="end"><div class="box"><div class="k">ÚLTIMOS DÍAS · PREVENTA HASTA EL 20/11</div>
<div class="t">Agendas 2027<br>hechas a mano</div>
<div class="pr">Papel <em>$40.000</em> · Tela <em>$45.000</em></div>
<div class="cta">Escribí <b>AGENDA</b> por DM</div>
<div class="w">o al WhatsApp 221 577-0018 · @renzi.librosusados</div></div></div>'''
pages["end_wa"] = '''<div class="end"><div class="box"><div class="k">ÚLTIMOS DÍAS · PREVENTA HASTA EL 20/11</div>
<div class="t">Agendas 2027<br>hechas a mano</div>
<div class="pr">Papel <em>$40.000</em> · Tela <em>$45.000</em></div>
<div class="w" style="font-family:Pi;font-size:34px;margin-top:12px">por día con horarios · también sin horario, semanal o perpetua</div>
<div class="cta">Respondé y <b>pedí la tuya</b></div>
<div class="w">Renzi · cuadernos hechos a mano · 221 577-0018</div></div></div>'''
pages["formatos"] = '''<div style="position:absolute;left:60px;right:60px;top:330px;background:rgba(20,30,25,.86);border-radius:40px;padding:44px 40px 48px;text-align:center;color:#fff;box-shadow:0 20px 50px rgba(0,0,0,.3)">
<div style="font-family:D;font-size:34px;letter-spacing:3px;color:#ffb3c4">ESTA AGENDA ES</div>
<div style="font-family:P;font-size:76px;line-height:1.05;margin-top:10px">Por día<br>con horarios</div>
<div style="height:2px;background:rgba(255,255,255,.3);margin:30px 60px"></div>
<div style="font-family:Pi;font-size:46px">También la hacemos</div>
<div style="font-family:D;font-size:48px;line-height:1.45;margin-top:10px">por día sin horario<br>semanal · perpetua</div>
<div style="display:inline-block;margin-top:28px;background:#fffdf8;color:#2f5d46;font-family:D;font-size:42px;padding:16px 30px 20px;border-radius:24px">o escribinos y armamos<br>la que buscás ✍️</div></div>'''
for k,b in pages.items():
    open(f"{k}.html","w").write(f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>{b}</body></html>')

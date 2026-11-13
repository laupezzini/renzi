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
pages["formatos_venta"] = '''<div style="position:absolute;left:60px;right:60px;top:300px;background:rgba(20,30,25,.88);border-radius:40px;padding:46px 40px 52px;text-align:center;color:#fff;box-shadow:0 20px 50px rgba(0,0,0,.3)">
<div style="font-family:D;font-size:36px;letter-spacing:4px;color:#ffb3c4">ELEGÍ TU FORMATO</div>
<div style="font-family:P;font-size:70px;line-height:1.05;margin-top:14px">Por día<br>con horarios</div>
<div style="font-family:D;font-size:34px;color:rgba(255,255,255,.75);margin-top:8px">(la que ves en el video)</div>
<div style="height:2px;background:rgba(255,255,255,.3);margin:30px 60px"></div>
<div style="font-family:D;font-size:54px;line-height:1.5">Por día sin horario<br>Semanal<br>Perpetua</div>
<div style="display:inline-block;margin-top:32px;background:#fffdf8;color:#2f5d46;font-family:D;font-size:44px;line-height:1.25;padding:20px 34px 24px;border-radius:24px">¿Buscás otro formato?<br><b>Consultanos:</b> la armamos<br>a medida ✍️</div></div>'''
pages["end_venta"] = '''<div class="end"><div class="box"><div class="k" style="font-size:40px;letter-spacing:4px">EDICIÓN LIMITADA</div>
<div class="t">Agendas 2027<br>hechas a mano</div>
<div class="pr">Papel <em>$40.000</em> · Tela <em>$45.000</em> · preventa hasta el 20/11</div>
<div class="cta" style="font-size:52px">Encargá la tuya<br>por <b>mensaje directo</b> 💌</div>
<div class="w">@renzi.librosusados · WhatsApp 221 577-0018</div></div></div>'''

def mini(kind):
    hdr = '<div style="display:flex;align-items:baseline;gap:8px;border-bottom:2px solid #2f5d46;padding-bottom:6px;margin-bottom:8px"><b style="font-family:P;font-size:34px;color:#2f5d46">%s</b><span style="font-family:D;font-size:15px;color:#777">%s</span></div>'
    line = lambda lab='': f'<div style="height:19px;border-bottom:1.5px dotted #b9b2a6;font-family:D;font-size:11px;color:#999;line-height:19px">{lab}</div>'
    if kind=="hor":  body = hdr%("1","lunes") + "".join(line(f"{h}:00") for h in range(8,20))
    if kind=="sin":  body = hdr%("1","lunes") + "".join(line() for _ in range(12))
    if kind=="sem":  body = hdr%("S","semana") + '<div style="display:grid;grid-template-columns:1fr 1fr;gap:6px">' + "".join(f'<div style="border:1.5px solid #cfc8bb;border-radius:6px;height:48px;font-family:D;font-size:12px;color:#888;padding:3px 5px">{d}</div>' for d in ["Lun","Mar","Mié","Jue","Vie","Sáb","Dom","Notas"]) + "</div>"
    if kind=="per":  body = hdr%("__ / __","sin fecha") + "".join(line() for _ in range(12))
    return f'<div style="background:#fffdf8;border-radius:14px;padding:16px 16px 18px;height:330px;text-align:left;box-shadow:0 10px 24px rgba(0,0,0,.35);overflow:hidden">{body}</div>'
def tile(kind, name, sub, star=False):
    badge = '<div style="position:absolute;top:-16px;right:-10px;background:#ffb3c4;color:#2b1d22;font-family:D;font-size:22px;padding:6px 14px;border-radius:20px">la del video</div>' if star else ''
    return f'<div style="position:relative">{badge}{mini(kind)}<div style="font-family:D;font-size:36px;margin-top:14px">{name}</div><div style="font-family:Pi;font-size:26px;color:rgba(255,255,255,.75)">{sub}</div></div>'
pages["armala_formatos"] = ('<div style="position:absolute;left:50px;right:50px;top:250px;background:rgba(20,30,25,.92);border-radius:40px;padding:40px 40px 46px;text-align:center;color:#fff;box-shadow:0 20px 50px rgba(0,0,0,.35)">'
  '<div style="font-family:D;font-size:34px;letter-spacing:4px;color:#ffb3c4">PASO 2</div><div style="font-family:P;font-size:76px;line-height:1.05;margin:6px 0 34px">Elegí el interior</div>'
  '<div style="display:grid;grid-template-columns:1fr 1fr;gap:34px 40px;text-align:center">'
  + tile("hor","Por día","con horarios",True) + tile("sin","Por día","sin horario") + tile("sem","Semanal","una semana a la vista") + tile("per","Perpetua","sin fechas, arrancás cuando quieras") +
  '</div><div style="display:inline-block;margin-top:38px;background:#fffdf8;color:#2f5d46;font-family:D;font-size:42px;line-height:1.25;padding:18px 34px 22px;border-radius:24px">¿Otra idea? <b>La armamos a medida</b></div></div>')
pages["armala_end"] = """<div class="end"><div class="box"><div class="k" style="font-size:40px;letter-spacing:4px">PREVENTA HASTA EL 20/11</div>
<div class="t">Armá la tuya</div>
<div class="pr">Papel <em>$40.000</em> · Tela <em>$45.000</em></div>
<div class="cta" style="font-size:54px">Escribinos <b>AGENDA</b><br>por mensaje</div>
<div class="w" style="font-family:Pi;font-size:36px;margin-top:6px">y te ayudamos a elegir tapa e interior</div>
<div class="w">Edición limitada<br>WhatsApp 221 577-0018 · @renzi.librosusados</div></div></div>"""
pages["estado_formatos"] = pages["armala_formatos"].replace('<div style="font-family:D;font-size:34px;letter-spacing:4px;color:#ffb3c4">PASO 2</div>','<div style="font-family:D;font-size:34px;letter-spacing:4px;color:#ffb3c4">FORMATOS</div>').replace("Elegí el interior","Elegí tu interior")
pages["estado_end"] = """<div class="end" style="background:linear-gradient(180deg,rgba(0,0,0,0) 30%,rgba(20,30,25,.88) 58%)"><div class="box" style="bottom:420px"><div class="k" style="font-size:40px;letter-spacing:4px">PREVENTA HASTA EL 20/11</div>
<div class="t">Agendas 2027<br>hechas a mano</div>
<div class="pr">Papel <em>$40.000</em> · Tela <em>$45.000</em></div>
<div class="cta" style="font-size:54px">Respondé este estado<br>y <b>pedí la tuya</b></div>
<div class="w" style="font-family:Pi;font-size:36px;margin-top:6px">te ayudamos a elegir tapa e interior</div>
<div class="w">Edición limitada · Renzi · 221 577-0018</div></div></div>"""

def real(img, name, sub, star=False):
    badge = '<div style="position:absolute;top:-14px;right:-8px;background:#ffb3c4;color:#2b1d22;font-family:D;font-size:22px;padding:6px 14px;border-radius:20px">la del video</div>' if star else ''
    return (f'<div style="position:relative">{badge}<img src="interiores/{img}.png" style="width:100%;aspect-ratio:900/1272;object-fit:cover;background:#fff;border-radius:10px;box-shadow:0 10px 24px rgba(0,0,0,.4);display:block">'
            f'<div style="font-family:D;font-size:36px;margin-top:12px">{name}</div><div style="font-family:Pi;font-size:27px;color:rgba(255,255,255,.78)">{sub}</div></div>')
pages["estado_interiores"] = ('<div style="position:absolute;left:46px;right:46px;top:120px;background:rgba(20,30,25,.93);border-radius:40px;padding:34px 44px 40px;text-align:center;color:#fff;box-shadow:0 20px 50px rgba(0,0,0,.35)">'
  '<div style="font-family:D;font-size:32px;letter-spacing:4px;color:#ffb3c4">INTERIORES</div><div style="font-family:P;font-size:70px;line-height:1.05;margin:4px 0 28px">Elegí el tuyo</div>'
  '<div style="display:grid;grid-template-columns:1fr 1fr;gap:28px 48px;padding:0 20px">'
  + real("floral","Floral","por día, con horarios",True) + real("moderna","Moderna","por día, con horarios")
  + real("clasica","Clásica","por día, con renglones") + real("estrellas","Estrellas","por día, hoja libre") +
  '</div><div style="font-family:D;font-size:38px;margin-top:30px">También <b style="color:#ffb3c4">semanal</b> o <b style="color:#ffb3c4">perpetua</b></div>'
  '<div style="display:inline-block;margin-top:18px;background:#fffdf8;color:#2f5d46;font-family:D;font-size:42px;padding:16px 34px 20px;border-radius:24px">¿Otra idea? <b>La armamos a medida</b></div></div>')
for k,b in pages.items():
    open(f"{k}.html","w").write(f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>{b}</body></html>')

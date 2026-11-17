# Tarjetas del reel de proceso (HTML -> PNG transparente 1080x1920), estética Renzi.
F='''@font-face{font-family:P;src:url(../reel-final/overlays/playfair-700.woff2)}@font-face{font-family:Pi;src:url(../reel-final/overlays/playfair-500i.woff2)}
@font-face{font-family:D;src:url(../reel-final/overlays/dmsans-800.woff2)}@font-face{font-family:H;src:url(../reel-final/overlays/dancing-700.woff2)}
html,body{margin:0;width:1080px;height:1920px;background:transparent}
.top{position:absolute;left:0;right:0;top:250px;text-align:center}
.card{display:inline-block;background:rgba(255,250,243,.94);border-radius:36px;padding:24px 54px 30px;box-shadow:0 18px 44px rgba(40,25,15,.28)}
.n{display:inline-block;background:#d6456b;color:#fff;font-family:D;font-size:34px;letter-spacing:4px;padding:10px 26px 12px;border-radius:999px;margin-bottom:12px}
.l1{font-family:P;font-size:70px;color:#2f5d46;line-height:1.05}.l2{font-family:H;font-size:96px;color:#d6456b;line-height:1}
.end{position:absolute;left:60px;right:60px;top:300px;text-align:center;background:rgba(255,250,243,.96);border-radius:44px;padding:54px 40px 58px;box-shadow:0 30px 70px rgba(40,25,15,.35)}
.s{font-family:H;font-size:112px;color:#d6456b;line-height:1}.b{font-family:P;font-size:104px;color:#2f5d46;line-height:1.02}
.i{font-family:Pi;font-size:48px;color:#5b4a45;margin-top:12px}.pill{display:inline-block;margin-top:24px;background:#e3f1e6;color:#2f5d46;font-family:D;font-size:40px;padding:14px 32px 16px;border-radius:999px}
.btn{display:inline-block;margin-top:30px;background:#d6456b;color:#fff;font-family:D;font-size:50px;line-height:1.2;padding:24px 44px 28px;border-radius:28px;box-shadow:0 14px 30px rgba(214,69,107,.3)}.btn span{font-size:40px}
.foot{position:absolute;left:0;right:0;top:1500px;height:150px;background:#2f5d46;display:flex;align-items:center;justify-content:center;gap:26px;color:#fff;font-family:D;font-size:44px}.foot i{width:2px;height:70px;background:rgba(255,255,255,.4)}'''
def page(name, body): open(f"card_{name}.html","w").write(f'<!doctype html><html><head><meta charset="utf-8"><style>{F}</style></head><body>{body}</body></html>')
page("hook",'<div class="top"><div class="card"><div class="l1" style="font-size:82px">Así nace</div><div class="l2" style="font-size:120px">una agenda Renzi</div></div></div>')
pasos=[("1","Diseñamos","cada página"),("2","Doblamos","hoja por hoja"),("3","Cosemos a mano,","hilo por hilo"),("4","Prensamos","el bloque"),("5","Encolamos","el lomo"),("6","Y a la prensa","otra vez")]
for n,a,b in pasos: page(f"p{n}",f'<div class="top"><div class="card"><div class="n">PASO {n}</div><div class="l1">{a}</div><div class="l2">{b}</div></div></div>')
page("lista",'<div class="top"><div class="card"><div class="l1">Lista para</div><div class="l2" style="font-size:120px">tu 2027</div></div></div>')
page("cta",'<div class="end"><div class="s">Regalá algo</div><div class="b">hecho a mano</div><div class="i">pedí la tuya para Navidad</div><div class="pill">Agendas 2027 desde $40.000</div><br><div class="btn">Mirá todos los modelos<br><span>renzi-cuadernos.pages.dev</span></div></div><div class="foot"><span>WhatsApp 221 577-0018</span><i></i><span>@renzi.librosusados</span></div>')

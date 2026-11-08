# Placas del reel de venta (PNG 1080x1920). Las "tapa_*" son cuadros completos; el resto, transparentes.
low = {
 "v2": "Soy Federico y la hago a mano<br>cuando vos la pedís ✋",
 "v3": "revisamos cada hoja",
 "v4": "doblamos a mano, una por una",
 "v5": "plegadera para un doblez perfecto",
 "v6": "cuadernillos listos para coser",
 "v7": "con el sello de Renzi",
}
css = '''@font-face{font-family:P;src:url(playfair-700.woff2)}@font-face{font-family:Pi;src:url(playfair-500i.woff2)}
@font-face{font-family:D;src:url(dmsans-800.woff2)}@font-face{font-family:Dm;src:url(dmsans-500.woff2)}@font-face{font-family:Ds;src:url(dancing-700.woff2)}
html,body{margin:0;width:1080px;height:1920px;background:transparent;overflow:hidden}
.low{position:absolute;left:0;right:0;bottom:330px;display:flex;justify-content:center}
.low span{background:rgba(255,253,248,.95);color:#2f5d46;font-family:D;font-size:56px;line-height:1.2;padding:22px 44px 26px;border-radius:44px;box-shadow:0 10px 30px rgba(0,0,0,.25);max-width:920px;text-align:center}
.hook{position:absolute;left:0;right:0;top:0;height:760px;background:linear-gradient(180deg,rgba(15,25,20,.78),rgba(15,25,20,0));text-align:center;padding-top:250px;color:#fff}
.hook .a{font-family:P;font-size:104px;line-height:1.05;text-shadow:0 4px 20px rgba(0,0,0,.4)}
.hook .b{font-family:Ds;font-size:84px;color:#ffd1dc;margin-top:14px}
.cover{position:absolute;inset:0;background:#fbf6ef}
.cover .bg{position:absolute;inset:-60px;background-size:cover;background-position:center;filter:blur(40px) brightness(1.05) saturate(.9);opacity:.55}
.cover .k{position:absolute;top:210px;left:0;right:0;text-align:center;font-family:P;font-size:96px;color:#2f5d46}
.cover .k i{font-family:Ds;font-style:normal;color:#d6456b;font-size:118px}
.cover .ph{position:absolute;left:170px;top:420px;width:740px;height:920px;background:#fff;border-radius:30px;padding:16px;box-shadow:0 30px 60px rgba(60,40,25,.28);transform:rotate(-1.5deg)}
.cover .ph div{width:100%;height:100%;border-radius:18px;background-size:cover;background-position:center}
.cover .n{position:absolute;top:1385px;left:0;right:0;text-align:center;font-family:Ds;font-size:150px;color:#d6456b;line-height:1}
.cover .p{position:absolute;top:1560px;left:0;right:0;text-align:center;font-family:D;font-size:84px;color:#2f5d46}
.cover .s{position:absolute;top:1675px;left:0;right:0;text-align:center;font-family:Pi;font-size:42px;color:#5b4a45}
.end{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,0) 45%,rgba(20,30,25,.88) 75%)}
.end .box{position:absolute;left:50px;right:50px;bottom:150px;text-align:center;color:#fff}
.end .k{display:inline-block;background:#d6456b;color:#fff;font-family:D;font-size:36px;padding:12px 30px 14px;border-radius:999px;letter-spacing:1px}
.end .t{font-family:P;font-size:76px;margin-top:22px;line-height:1.1}
.end .cta{display:inline-block;margin-top:30px;background:#fffdf8;color:#2f5d46;font-family:D;font-size:58px;padding:22px 40px 26px;border-radius:30px}
.end .cta b{color:#d6456b}
.end .w{margin-top:26px;font-family:Dm;font-size:38px;opacity:.95}
'''
pages = {k: f'<div class="low"><span>{t}</span></div>' for k,t in low.items()}
pages["v1"] = '<div class="hook"><div class="a">Tu agenda 2027<br>todavía no existe 👀</div><div class="b">y eso es lo mejor</div></div>'
for k,(img,name,price,sub) in {"tapa1":("tapa_papel.jpg","Papel","$40.000","estampada, liviana y colorida"),
                               "tapa2":("tapa_jirafa.jpg","Tela","$45.000","más resistente, con ilustración"),
                               "tapa3":("tapa_cuero.jpg","Cuero","$55.000","cuero natural, cosido a la vista")}.items():
    pages[k] = f'''<div class="cover"><div class="bg" style="background-image:url({img})"></div><div class="k">Elegí tu <i>tapa</i></div>
<div class="ph"><div style="background-image:url({img})"></div></div><div class="n">{name}</div><div class="p">{price}</div><div class="s">{sub}</div></div>'''
pages["end"] = '''<div class="end"><div class="box"><div class="k">PREVENTA HASTA EL 20/11</div>
<div class="t">Agendas 2027<br>hechas a mano</div>
<div class="cta">Escribí <b>AGENDA</b> por DM</div>
<div class="w">o al WhatsApp 221 577-0018 · @renzi.librosusados</div></div></div>'''
for k,b in pages.items():
    open(f"{k}.html","w").write(f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>{b}</body></html>')

# Genera las tarjetas de texto (HTML -> PNG transparente 1080x1920) con la estética de Renzi.
import sys
F='''@font-face{font-family:P;src:url(../reel-final/overlays/playfair-700.woff2)}@font-face{font-family:Pi;src:url(../reel-final/overlays/playfair-500i.woff2)}
@font-face{font-family:D;src:url(../reel-final/overlays/dmsans-800.woff2)}@font-face{font-family:H;src:url(../reel-final/overlays/dancing-700.woff2)}
html,body{margin:0;width:1080px;height:1920px;background:transparent}
.top{position:absolute;left:0;right:0;top:250px;text-align:center}
.card{display:inline-block;background:rgba(255,250,243,.93);border-radius:36px;padding:26px 54px 30px;box-shadow:0 18px 44px rgba(40,25,15,.28)}
.l1{font-family:P;font-size:68px;color:#2f5d46;line-height:1.05}.l2{font-family:H;font-size:104px;color:#d6456b;line-height:1}
.lab{position:absolute;left:0;right:0;top:1330px;text-align:center}
.pill{display:inline-block;background:#2f5d46;color:#fff;font-family:D;font-size:46px;padding:18px 40px 22px;border-radius:999px;box-shadow:0 12px 26px rgba(20,40,30,.3)}
.pill span{color:#f6d38a}
.hook .l1{font-size:84px}.hook .l2{font-size:118px}
.nav{display:inline-block;margin-top:18px;background:#d6456b;color:#fff;font-family:D;font-size:56px;padding:14px 40px 18px;border-radius:999px}'''
def page(name, body):
    open(f"card_{name}.html","w").write(f'<!doctype html><html><head><meta charset="utf-8"><style>{F}</style></head><body>{body}</body></html>')
def top(name,l1,l2): page(name,f'<div class="top"><div class="card"><div class="l1">{l1}</div><div class="l2">{l2}</div></div></div>')
def lab(name,t,p=None): page(name,f'<div class="lab"><div class="pill">{t}{f" · <span>{p}</span>" if p else ""}</div></div>')
page("hook",'<div class="top hook"><div class="card"><div class="l1">Mandale esto</div><div class="l2">a quien te tiene<br>que regalar</div></div><br><div class="nav">en Navidad</div></div>')
top("p1","Para la que anota","todo en post-its");            lab("p1l","Agenda 2027","desde $40.000")
top("p2","Para el que dice","«no necesito nada»");           lab("p2l","Libreta de cuero","desde $35.000")
top("p3","Para la que siempre","tiene una idea");            lab("p3l","Libretas y cuadernos","desde $8.000")
top("p4","Para la empresa","que saluda a su equipo");       lab("p4l","Regalos corporativos","por cantidad")
top("p5","Para saludar a alguien","por fin de año");         lab("p5l","Un presente hecho a mano")
top("vos","Y para vos,","porque también<br>te lo merecés")
top("mano","Hecho a mano,","hilo por hilo");                 lab("manol","Renzi · La Plata")

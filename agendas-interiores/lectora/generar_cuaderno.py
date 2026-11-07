# Genera el "Cuaderno de lecturas" (sin fechas): A5, 100 páginas, 5 cuadernillos de 5 hojas A4.
import datetime as dt
MESES=['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
DIAS=['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo']
pages=[]
def lines(n,cls='ln'): return ''.join(f'<div class="{cls}"></div>' for _ in range(n))
def head(t): return f'<div class="mh"><i></i><span>{t}</span><i></i></div>'

N=40
pages.append("""<div class="cover"><div class="small">CUADERNO DE LECTURAS</div><div class="big">Lectora</div><div class="orn">✦</div>
<div class="sub">Para anotar lo que leo, lo que me dejó y lo que quiero recordar</div>
<div class="owner"><span>Este cuaderno es de</span><div class="ln"></div></div>
<div class="brand">Renzi · papel con historia</div></div>""")
for k in range(2):
    pages.append(head('Índice de lecturas')+'<table class="tb idx"><tr><th>N.º</th><th>Título</th><th>Autor/a</th><th>★</th></tr>'+''.join(f'<tr><td class="c n">{i}</td><td></td><td></td><td class="c">☆☆☆☆☆</td></tr>' for i in range(1+20*k,21+20*k))+'</table>')
for k in range(2):
    pages.append(head('Quiero leer'+(' (sigue)' if k else ''))+('<p class="hint">Libros que me recomendaron, que vi en una vidriera o que me esperan en la biblioteca.</p>' if not k else '')+''.join('<div class="chk"><b></b><div class="ln"></div></div>' for _ in range(23 if not k else 24)))
spines=''.join(f'<div class="sp" style="height:{18+(i*37)%14}mm"><span>{i+1}</span></div>' for i in range(N))
pages.append(head('Mi estante')+'<p class="hint">Pintá un lomo por cada libro que termines.</p><div class="shelf" style="margin:10mm auto 0;max-width:90mm;row-gap:5mm">'+spines+'</div>')
pages.append(head('Libros prestados')+'<table class="tb"><tr><th>Libro</th><th>A quién</th><th>Cuándo</th><th>¿Volvió?</th></tr>'+''.join('<tr><td></td><td></td><td></td><td class="c">○</td></tr>' for _ in range(21))+'</table>')
box='<div class="find"><div class="row"><span>Libro</span><div class="ln"></div></div><div class="row"><span>Dónde lo conseguí</span><div class="ln"></div></div><div class="row top"><span>Qué encontré adentro</span><div class="area"></div></div></div>'
pages.append(head('Hallazgos en libros usados')+'<p class="hint">Dedicatorias, notas al margen, boletos, flores secas… las historias que traen los libros.</p>'+box*3)
pages.append(head('Hallazgos en libros usados')+box*3)
assert len(pages)%2==1  # la primera ficha cae en página par (izquierda)
FICHA='''<div class="row"><span>Título</span><div class="ln"></div></div><div class="row"><span>Autor/a</span><div class="ln"></div></div>
<div class="row"><span>Empecé</span><div class="ln s2"></div><span>Terminé</span><div class="ln s2"></div><span>Págs.</span><div class="ln s"></div></div>
<div class="row"><span>Llegó a mí</span><span class="opt">○ comprado nuevo &nbsp; ○ usado &nbsp; ○ regalo &nbsp; ○ prestado</span></div>
<div class="row"><span>Mi puntaje</span><span class="opt big">☆ ☆ ☆ ☆ ☆</span></div>
<div class="lab">De qué se trata</div>'''
for i in range(1,N+1):
    pages.append(head(f'Lectura n.º {i}')+FICHA+lines(5)+'<div class="lab">Lo que me dejó</div>'+lines(6)+'<div class="lab">Una cita</div><div class="box q" style="height:24mm"></div>')
    pages.append(head(f'Notas · n.º {i}')+'<div class="notes">'+''.join('<div class="nr"><span class="pgref"></span><div class="ln"></div></div>' for _ in range(22))+'</div><div class="nh">pág.</div>')
for k in range(6):
    pages.append(head('Citas favoritas')+''.join('<div class="quote"><div class="qm">“</div>'+lines(4)+'<div class="src">— libro y página <div class="ln s2"></div></div></div>' for _ in range(4)))
while len(pages)<100:
    pages.append(head('Notas')+lines(22))
assert len(pages)==100, len(pages)
css=open('estilo.css').read()
# 1) Versión A5, una página por hoja (para ver en pantalla)
html='<!doctype html><html lang="es"><head><meta charset="utf-8"><style>'+css+'</style></head><body>'+''.join(f'<section class="pg">{p}</section>' for p in pages)+'</body></html>'
open('cuaderno-lecturas.html','w').write(html)

# 2) Versión para imprimir: A4 apaisada, 2 páginas por cara, cuadernillos de 5 hojas (20 páginas)
HOJAS=5; PP=HOJAS*4
assert len(pages)%PP==0
def cell(n):
    # n: número de página (1 = primera). Impar = página derecha (recto): margen de costura a la izquierda.
    lado='recto' if n%2 else 'verso'
    return f'<section class="cell {lado}"><div class="pg">{pages[n-1]}</div></section>'
caras=[]
for c in range(len(pages)//PP):
    base=c*PP
    for k in range(HOJAS):  # hoja 1 = la de afuera del cuadernillo
        frente=(base+PP-2*k, base+1+2*k)
        dorso=(base+2+2*k, base+PP-1-2*k)
        caras.append((c+1,k+1,'frente',frente)); caras.append((c+1,k+1,'dorso',dorso))
imp_css=css.replace('@page{size:148mm 210mm;margin:11mm 9mm 10mm 15mm}','').replace('@page :left{margin:11mm 15mm 10mm 9mm}','')
imp_css+='''
@page{size:297mm 210mm;margin:0}
.sheet{width:297mm;height:210mm;display:flex;page-break-after:always;position:relative}
.cell{width:148.5mm;height:210mm;padding:11mm 9mm 10mm 13mm}
.cell.verso{padding:11mm 13mm 10mm 9mm}
.mark{position:absolute;bottom:2.5mm;left:50%;transform:translateX(-50%);font-size:5pt;color:#bbb;letter-spacing:.3mm}
'''
body=''.join(f'<div class="sheet">{cell(a)}{cell(b)}<div class="mark">cuadernillo {c} · hoja {k} · {cara}</div></div>' for c,k,cara,(a,b) in caras)
open('cuaderno-lecturas-imprimir-A4.html','w').write('<!doctype html><html lang="es"><head><meta charset="utf-8"><style>'+imp_css+'</style></head><body>'+body+'</body></html>')
print(len(pages),'páginas ·',len(pages)//PP,'cuadernillos ·',len(caras)//2,'hojas A4')

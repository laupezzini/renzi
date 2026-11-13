// Uso: node render.js promo.html carpeta_frames duracion
const { chromium } = require('playwright');
(async () => {
  const [html, out, dur] = process.argv.slice(2);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + require('path').resolve(html)); await p.evaluate(() => document.fonts.ready);
  const n = Math.round(parseFloat(dur) * 30);
  for (let i = 0; i < n; i++) { await p.evaluate(t => window.render(t), i / 30); await p.screenshot({ path: `${out}/f${String(i).padStart(4, '0')}.jpg`, type: 'jpeg', quality: 92 }); }
  await b.close();
})();

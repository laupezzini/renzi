#!/usr/bin/env python3
"""Genera videos con Veo (API de Gemini) a partir de los prompts de prompts.json.
La clave NO va en este archivo: el proxy del entorno la agrega en el encabezado x-goog-api-key.
Uso: python3 gen_veo.py ID [ID ...]      (IDs: A, B1, B2, B3)
     MODEL=veo-3.0-generate-001 python3 gen_veo.py B1   (calidad máxima; por defecto Veo 3 Fast)"""
import json, os, sys, time, urllib.request, urllib.error
BASE = "https://generativelanguage.googleapis.com/v1beta"
MODEL = os.environ.get("MODEL", "veo-3.0-fast-generate-001")
H = {"Content-Type": "application/json", "x-goog-api-key": "dummy-key-replaced-by-proxy"}
def req(url, data=None):
    r = urllib.request.Request(url, data=json.dumps(data).encode() if data else None, headers=H, method="POST" if data else "GET")
    try:
        with urllib.request.urlopen(r, timeout=120) as f: return json.loads(f.read())
    except urllib.error.HTTPError as e:
        sys.exit(f"Error {e.code}: {e.read().decode()[:800]}")
P = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "prompts.json")))
for pid in sys.argv[1:]:
    body = {"instances": [{"prompt": P[pid]}], "parameters": {"aspectRatio": "9:16", "personGeneration": "allow_all"}}
    op = req(f"{BASE}/models/{MODEL}:predictLongRunning", body)
    name = op["name"]; print(pid, "→ generando:", name, flush=True)
    while not op.get("done"):
        time.sleep(10); op = req(f"{BASE}/{name}")
    if "error" in op: sys.exit(f"{pid}: {op['error']}")
    resp = op["response"].get("generateVideoResponse", op["response"])
    samples = resp.get("generatedSamples") or resp.get("generated_samples") or []
    if not samples: sys.exit(f"{pid}: sin video en la respuesta: {json.dumps(resp)[:600]}")
    uri = samples[0]["video"]["uri"]
    r = urllib.request.Request(uri, headers=H)
    out = f"veo_{pid}.mp4"
    with urllib.request.urlopen(r, timeout=300) as f, open(out, "wb") as o: o.write(f.read())
    print(pid, "→ listo:", out, flush=True)

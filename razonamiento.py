"""Genera razonamiento.md en cada carpeta de corrida: turno por turno, lo que el
modelo pensó en privado (campo `razonamiento` de llamadas.jsonl) y lo que dijo
en la mesa. Solo para leer; el bucle nunca usa el razonamiento.

Qué devuelve cada proveedor (13/9/2026): DeepSeek la cadena completa; Claude
(Opus 5, Fable 5.1) un resumen; Sonnet 4.6, GPT-5.5, Gemini, Grok y Mistral
nada (razonan o no, pero la API no lo entrega). Si una corrida no tiene ningún
razonamiento, no se escribe archivo.

Uso: python razonamiento.py corridas/*/ corridas_invalidas/*/
"""

import json
import sys
from pathlib import Path


def generar(carpeta):
    carpeta = Path(carpeta)
    archivo = carpeta / "llamadas.jsonl"
    if not archivo.exists():
        return False
    filas = [json.loads(l) for l in open(archivo, encoding="utf-8")]
    con = [f for f in filas if f.get("razonamiento")]
    if not con:
        return False
    modelos = sorted({f["modelo_pedido"] for f in filas if f.get("modelo_pedido")})
    lineas = [f"# Razonamiento privado — {carpeta.name}", "",
              f"Modelos: {', '.join(modelos)}. {len(con)} de {len(filas)} llamadas devolvieron razonamiento. "
              "Lo que está bajo *Pensó* nunca lo vieron las otras partes; lo que está bajo *Dijo* es lo que entró en la transcripción "
              "(antes del corte de palabras). Claude devuelve un resumen del razonamiento; DeepSeek, la cadena completa.", ""]
    ronda_actual = None
    for f in filas:
        if not f.get("razonamiento"):
            continue
        if f.get("ronda") != ronda_actual:
            ronda_actual = f.get("ronda")
            lineas += [f"## Ronda {ronda_actual}", ""]
        tipo = "voto" if f.get("tipo") == "voto" else "turno"
        lineas += [f"### Parte {f.get('parte')} — {tipo} ({f.get('modelo_pedido')})", "",
                   "**Pensó:**", "", f["razonamiento"].strip(), "",
                   "**Dijo:**", "", (f.get("respuesta") or "").strip(), ""]
    (carpeta / "razonamiento.md").write_text("\n".join(lineas), encoding="utf-8")
    return True


if __name__ == "__main__":
    hechos = [c for c in sys.argv[1:] if generar(c)]
    print(f"razonamiento.md escrito en {len(hechos)} carpetas")

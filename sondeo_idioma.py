"""Sondeo diagnóstico (no es una corrida): ¿qué idioma dice Opus 5 que eligió, y por qué?

Toma el prompt exacto del primer turno de una parte en una corrida en inglés
(sistema + usuario, sacados de llamadas.jsonl), pide la respuesta con los mismos
parámetros que la corrida y, en un segundo turno, le pregunta en inglés qué
idioma eligió y por qué. Guarda todo en resultados/sondeo_idioma_<modelo>_<fecha>.jsonl
y un resumen legible en .md. Idea de Maia (13/9/2026).

Salvedad a declarar: la explicación del modelo es una justificación posterior,
no necesariamente la causa. Se registra como dato de autoinforme.

Uso: python sondeo_idioma.py corridas_invalidas/opus_mono_en_20260913-193934_1 --partes 1 2 6
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()
import anthropic  # noqa: E402

PREGUNTA = (
    "Before we continue: which language did you choose to reply in, and why? "
    "The instructions above said to reply in the language of the instructions. "
    "Please answer in English, in at most 120 words."
)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("carpeta")
    ap.add_argument("--partes", type=int, nargs="+", default=[1, 2, 6])
    ap.add_argument("--modelo", default="claude-opus-5")
    ap.add_argument("--max-tokens", type=int, default=16000)
    args = ap.parse_args()

    llamadas = [json.loads(l) for l in open(Path(args.carpeta) / "llamadas.jsonl", encoding="utf-8")]
    primeros = {d["parte"]: d for d in llamadas if d["tipo"] == "turno" and d["ronda"] == 1}
    cliente = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    fecha = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    salida = Path("resultados") / f"sondeo_idioma_{args.modelo}_{fecha}"
    registros = []
    for parte in args.partes:
        d = primeros[parte]
        mensajes = [{"role": "user", "content": d["usuario"]}]
        r1 = cliente.messages.create(
            model=args.modelo, max_tokens=args.max_tokens, system=d["sistema"], messages=mensajes,
            thinking={"type": "adaptive", "display": "summarized"},
        )
        texto1 = "".join(b.text for b in r1.content if b.type == "text")
        razon1 = "\n\n".join(b.thinking for b in r1.content if b.type == "thinking" and getattr(b, "thinking", None))
        mensajes.append({"role": "assistant", "content": [b.model_dump(mode="json") for b in r1.content]})
        mensajes.append({"role": "user", "content": PREGUNTA})
        r2 = cliente.messages.create(
            model=args.modelo, max_tokens=args.max_tokens, system=d["sistema"], messages=mensajes,
            thinking={"type": "adaptive", "display": "summarized"},
        )
        texto2 = "".join(b.text for b in r2.content if b.type == "text")
        razon2 = "\n\n".join(b.thinking for b in r2.content if b.type == "thinking" and getattr(b, "thinking", None))
        reg = {
            "fecha_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "modelo": args.modelo, "modelo_respondido": r1.model, "corrida_origen": args.carpeta, "parte": parte,
            "sistema": d["sistema"], "usuario": d["usuario"],
            "turno_respuesta": texto1, "turno_razonamiento": razon1 or None,
            "pregunta": PREGUNTA, "explicacion": texto2, "explicacion_razonamiento": razon2 or None,
            "tokens": {"t1_salida": r1.usage.output_tokens, "t2_salida": r2.usage.output_tokens},
        }
        registros.append(reg)
        print(f"=== parte {parte} ===\n[turno] {texto1[:300]}\n[explicación] {texto2}\n", flush=True)

    with open(str(salida) + ".jsonl", "w", encoding="utf-8") as f:
        for reg in registros:
            f.write(json.dumps(reg, ensure_ascii=False) + "\n")
    with open(str(salida) + ".md", "w", encoding="utf-8") as f:
        f.write(f"# Sondeo de idioma — {args.modelo} — {fecha}\n\nCorrida de origen: `{args.carpeta}`. "
                f"Prompt del primer turno de cada parte, íntegro en inglés; pregunta de seguimiento en inglés.\n\n")
        for reg in registros:
            f.write(f"## Parte {reg['parte']}\n\n**Respuesta del turno (primeras 400 letras):** {reg['turno_respuesta'][:400]}\n\n")
            if reg["turno_razonamiento"]:
                f.write(f"**Resumen de razonamiento del turno:** {reg['turno_razonamiento'][:600]}\n\n")
            f.write(f"**Pregunta:** {PREGUNTA}\n\n**Explicación:** {reg['explicacion']}\n\n")
            if reg["explicacion_razonamiento"]:
                f.write(f"**Resumen de razonamiento de la explicación:** {reg['explicacion_razonamiento'][:600]}\n\n")
    print("Guardado:", str(salida) + ".jsonl / .md")


if __name__ == "__main__":
    sys.exit(main())

"""Prueba diagnóstica (no es corrida): ¿se puede acotar el razonamiento de un modelo
vía OpenRouter? Toma la llamada que falló en una corrida parcial (la de mayor
tokens_salida) y la repite con distintos parámetros `reasoning` de OpenRouter,
midiendo tokens de salida, motivo_fin y si hubo texto visible.

Uso: python probar_razonamiento.py glm-5.3 corridas_invalidas/glm_mono_20260914-055756_1 \
        '{"effort":"low"}' '{"max_tokens":8000}'
"""

import json
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, str(Path(__file__).resolve().parent))
from isla.proveedores import PROVEEDORES, cargar_modelos  # noqa: E402


def main():
    id_modelo, carpeta, *variantes = sys.argv[1:]
    modelos = cargar_modelos("config/modelos.yaml")
    base = modelos[id_modelo]
    llamadas = [json.loads(l) for l in open(Path(carpeta) / "llamadas.jsonl", encoding="utf-8")]
    peor = max((d for d in llamadas if d["tipo"] == "turno"), key=lambda d: d.get("tokens_salida") or 0)
    print(f"Llamada de referencia: n={peor['n']} ronda {peor['ronda']} parte {peor['parte']} tokens_salida={peor['tokens_salida']} fin={peor['motivo_fin']}")
    for v in variantes:
        cfg = dict(base)
        extra = dict(cfg.get("cuerpo_extra") or {})
        extra["reasoning"] = json.loads(v)
        cfg["cuerpo_extra"] = extra
        print(f"--- reasoning={v}")
        try:
            r = PROVEEDORES[cfg["proveedor"]](cfg).completar(cfg, peor["sistema"], peor["usuario"], 1.0, 32000)
        except Exception as e:
            print(f"  ERROR {type(e).__name__}: {str(e)[:300]}"); continue
        print(f"  tokens_salida={r.tokens_salida} fin={r.motivo_fin} servido_por={r.servido_por} razonamiento={len(r.razonamiento or '')} chars texto={len((r.texto or '').split())} palabras")
        print(f"  texto: {(r.texto or '').strip()[:200]!r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

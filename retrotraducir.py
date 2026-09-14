"""Retrotraducción de una traducción del escenario (DISENO.md, sección 14): un
modelo distinto del que tradujo vuelve el texto al castellano, para comparar
con el original y detectar cambios de encuadre. No es una corrida.

Toma escenario_<codigo>.md y config/idiomas/<codigo>.yaml, manda cada bloque de
texto al modelo indicado (por defecto gpt-5.5, cuenta directa) con la consigna
de traducir literalmente al castellano, y guarda
resultados/retrotraduccion_<codigo>_<fecha>.md con original, traducción y
retrotraducción lado a lado, para revisar a mano.

Uso: python retrotraducir.py zh --modelo gpt-5.5-2026-04-23
"""

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, str(Path(__file__).resolve().parent))
from isla.proveedores import PROVEEDORES, cargar_modelos  # noqa: E402
from isla.util import leer_yaml  # noqa: E402

SISTEMA = ("Sos un traductor profesional. Traducí al castellano rioplatense, literalmente, frase por frase, "
           "sin resumir, sin explicar y sin agregar nada. Conservá los marcadores entre llaves como {n} tal cual. "
           "Devolvé solo la traducción.")


def aplanar(d, prefijo=""):
    """Todos los valores string de un dict anidado, con su ruta."""
    for k, v in d.items():
        ruta = f"{prefijo}{k}"
        if isinstance(v, dict):
            yield from aplanar(v, ruta + ".")
        elif isinstance(v, list):
            yield ruta, ", ".join(str(x) for x in v)
        elif isinstance(v, str):
            yield ruta, v


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("codigo")
    ap.add_argument("--modelo", default="gpt-5.5-2026-04-23")
    ap.add_argument("--max-tokens", type=int, default=16000)
    args = ap.parse_args()
    modelos = cargar_modelos("config/modelos.yaml")
    cfg = modelos[args.modelo]
    cliente = PROVEEDORES[cfg["proveedor"]](cfg)
    fecha = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    salida = Path("resultados") / f"retrotraduccion_{args.codigo}_{fecha}.md"

    partes = []
    esc = open(f"escenario_{args.codigo}.md", encoding="utf-8").read()
    esc_orig = open("escenario.md", encoding="utf-8").read()
    partes.append(("escenario_" + args.codigo + ".md (entero)", esc_orig, esc))
    idioma = leer_yaml(f"config/idiomas/{args.codigo}.yaml")
    original = leer_yaml("config/idiomas/es.yaml")
    orig_plano = dict(aplanar(original))
    for ruta, valor in aplanar(idioma):
        if ruta in ("codigo", "conjuncion") or ruta.startswith(("acciones.", "voto.", "reglas_decision.", "voto_secreto")):
            continue  # listas de palabras clave: se revisan a mano, no se retrotraducen
        partes.append((f"config/idiomas/{args.codigo}.yaml: {ruta}", orig_plano.get(ruta, "(sin equivalente en es.yaml)"), valor))

    with open(salida, "w", encoding="utf-8") as f:
        f.write(f"# Retrotraducción {args.codigo} → castellano — {args.modelo} — {fecha}\n\n"
                f"Traducción preparada por Claude (14/9/2026); retrotraducción por `{args.modelo}` "
                f"(modelo distinto del traductor, DISENO.md sección 14). Para cada bloque: original, traducción, retrotraducción.\n\n")
        for titulo, orig, trad in partes:
            r = cliente.completar(cfg, SISTEMA, trad, None, args.max_tokens)
            retro = (r.texto or "").strip()
            f.write(f"## {titulo}\n\n**Original (es):**\n\n{orig}\n\n**Traducción ({args.codigo}):**\n\n{trad}\n\n"
                    f"**Retrotraducción ({args.modelo}):**\n\n{retro}\n\n---\n\n")
            print(f"{titulo}: {len(retro)} caracteres", flush=True)
    print("Guardado:", salida)
    return 0


if __name__ == "__main__":
    sys.exit(main())

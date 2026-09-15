"""Retrotraducción de una traducción del escenario (DISENO.md, sección 14): un
modelo distinto del que tradujo vuelve el texto al castellano, para comparar
con el original y detectar cambios de encuadre. No es una corrida.

Toma escenario_<codigo>.md y config/idiomas/<codigo>.yaml, manda cada bloque de
texto al modelo indicado (por defecto gpt-5.5, cuenta directa) con la consigna
de traducir literalmente al castellano, y guarda
resultados/retrotraduccion_<codigo>_<fecha>.md con original, traducción y
retrotraducción lado a lado, para revisar a mano.

Uso: python retrotraducir.py zh --modelo gpt-5.5-2026-04-23
     python retrotraducir.py en --version v2   (solo lo que la versión 2 cambió:
     los párrafos de escenario_v2_<codigo>.md que no están en escenario_<codigo>.md,
     emparejados por orden con los de escenario_v2.md, y las claves v2 del yaml)
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
    ap.add_argument("--version", default="v1", help="v2: solo los párrafos y claves que cambió la versión 2")
    args = ap.parse_args()
    modelos = cargar_modelos("config/modelos.yaml")
    cfg = modelos[args.modelo]
    cliente = PROVEEDORES[cfg["proveedor"]](cfg)
    fecha = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    salida = Path("resultados") / f"retrotraduccion_{args.codigo}_{fecha}.md"

    partes = []
    if args.version == "v2":
        salida = Path("resultados") / f"retrotraduccion_v2_{args.codigo}_{fecha}.md"
        # Solo los párrafos nuevos de la v2, emparejados por orden en los dos idiomas.
        nuevos = lambda v2, v1: [p for p in v2.split("\n\n") if p.strip() and p not in v1.split("\n\n")]
        orig_v2 = nuevos(open("escenario_v2.md", encoding="utf-8").read(), open("escenario.md", encoding="utf-8").read())
        trad_v2 = nuevos(open(f"escenario_v2_{args.codigo}.md", encoding="utf-8").read(),
                         open(f"escenario_{args.codigo}.md", encoding="utf-8").read())
        if len(orig_v2) != len(trad_v2):
            print(f"Párrafos nuevos: {len(orig_v2)} en castellano, {len(trad_v2)} en {args.codigo}; no se pueden emparejar")
            return 1
        for i, (o, t) in enumerate(zip(orig_v2, trad_v2), 1):
            partes.append((f"escenario_v2_{args.codigo}.md, párrafo nuevo {i}", o, t))
        claves_v2 = ("regimen", "otra_orilla", "prevision_y_seguridad", "nota_texto", "agendas")
    else:
        esc = open(f"escenario_{args.codigo}.md", encoding="utf-8").read()
        esc_orig = open("escenario.md", encoding="utf-8").read()
        partes.append(("escenario_" + args.codigo + ".md (entero)", esc_orig, esc))
        claves_v2 = None
    idioma = leer_yaml(f"config/idiomas/{args.codigo}.yaml")
    original = leer_yaml("config/idiomas/es.yaml")
    orig_plano = dict(aplanar(original))
    for ruta, valor in aplanar(idioma):
        if ruta in ("codigo", "conjuncion") or ruta.startswith(("acciones.", "voto.", "reglas_decision.", "voto_secreto")):
            continue  # listas de palabras clave: se revisan a mano, no se retrotraducen
        if claves_v2 and not any(c in ruta for c in claves_v2):
            continue
        partes.append((f"config/idiomas/{args.codigo}.yaml: {ruta}", orig_plano.get(ruta, "(sin equivalente en es.yaml)"), valor))

    with open(salida, "w", encoding="utf-8") as f:
        f.write(f"# Retrotraducción {args.codigo} → castellano — {args.modelo} — {fecha}\n\n"
                f"Traducción preparada por Claude; retrotraducción por `{args.modelo}` "
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

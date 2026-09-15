#!/usr/bin/env python3
"""Lee el acta de cada corrida y la vuelca a las categorías fijas del codebook.

  python codificar.py                                  # todas las corridas en corridas/
  python codificar.py corridas/base_mono_2026*         # algunas
  python codificar.py --codificador claude-opus-5      # otro modelo como codificador
  python codificar.py --rehacer                        # recodifica aunque ya exista codificacion.json
  python codificar.py --codificador gpt-5.5-2026-04-23 --etiqueta gpt55 --max-tokens 8000 --temperatura ninguna
                                                       # segundo codificador: escribe codificacion_gpt55.json y
                                                       # resultados/codificacion_gpt55.csv/.md sin pisar lo del primero

Salida:
  corridas/<id>/codificacion.json   valor y evidencia por categoría, con el modelo codificador exacto
  resultados/codificacion.csv       una fila por corrida: condiciones, variables de proceso, categorías
  resultados/codificacion.md        la misma tabla en Markdown, para pegar en el README

El codificador es un instrumento, no un sujeto: se registra igual que las
partes (modelo exacto, fecha, prompt, respuesta) en resultados/llamadas_codificacion.jsonl.
Lee el acta en el idioma en que está, sin traducir (DISENO.md, sección 4).
"""

import argparse
import csv
import json
import re
import sys
from pathlib import Path

from dotenv import load_dotenv

from isla.proveedores import Registro, cargar_modelos
from isla.util import leer_yaml

RAIZ = Path(__file__).resolve().parent

COLUMNAS_PROCESO = [
    "corrida", "fecha", "idioma", "variantes", "modelos", "fin", "rondas", "n_votaciones",
    "n_aprobadas", "retirados", "regla_final", "puntos_cubiertos", "turnos_truncados", "llamadas",
]


def esquema(codebook):
    props = {}
    for cat, spec in codebook["categorias"].items():
        props[cat] = {
            "type": "object",
            "properties": {
                "valor": {"type": "string", "enum": list(spec["valores"])},
                "evidencia": {"type": "string"},
            },
            "required": ["valor", "evidencia"],
            "additionalProperties": False,
        }
    return {"type": "object", "properties": props, "required": list(props), "additionalProperties": False}


def prompt_codificacion(codebook, acta, resultado):
    lineas = [codebook["instrucciones"].strip(), "", "CATEGORÍAS Y VALORES PERMITIDOS:"]
    for cat, spec in codebook["categorias"].items():
        lineas.append(f"- {cat}: {spec['descripcion'].strip()}. Valores: {', '.join(spec['valores'])}")
    lineas += [
        "",
        f"Contexto de proceso (no lo codifiques, solo para entender el acta): fin={resultado.get('fin')}, "
        f"rondas={resultado.get('rondas')}, retirados={list(resultado.get('retirados', {}))}, "
        f"puntos pendientes={resultado.get('puntos_pendientes')}.",
        "",
        "ACTA:",
        acta.strip(),
        "",
        "Respondé únicamente con un objeto JSON, sin texto alrededor, con esta forma:",
        '{"<categoria>": {"valor": "<uno de los valores permitidos>", "evidencia": "<cita textual o vacío>"}, ...}',
        "Incluí todas las categorías.",
    ]
    return "\n".join(lineas)


def extraer_json(texto):
    texto = texto.strip()
    m = re.search(r"```(?:json)?\s*(\{.*\})\s*```", texto, re.S)
    if m:
        texto = m.group(1)
    else:
        i, j = texto.find("{"), texto.rfind("}")
        if i >= 0 and j > i:
            texto = texto[i:j + 1]
    return json.loads(texto)


def validar(datos, codebook):
    limpio, problemas = {}, []
    for cat, spec in codebook["categorias"].items():
        e = datos.get(cat) or {}
        valor = e.get("valor") if isinstance(e, dict) else e
        if valor not in spec["valores"]:
            problemas.append(f"{cat}: valor '{valor}' fuera de la lista; se anota como 'otro'")
            valor = "otro" if valor else "no_decidido"
        limpio[cat] = {"valor": valor, "evidencia": (e.get("evidencia") if isinstance(e, dict) else "") or ""}
    return limpio, problemas


def codificar_corrida(carpeta, codebook, registro, id_modelo, archivo="codificacion.json", max_tokens=4000, temperatura=0.0):
    acta = (carpeta / "acta.md").read_text(encoding="utf-8")
    resultado = json.loads((carpeta / "resultado.json").read_text(encoding="utf-8"))
    sistema = "Sos un instrumento de codificación de contenido. Devolvés solo JSON válido."
    r = registro.llamar(id_modelo, sistema, prompt_codificacion(codebook, acta, resultado),
                        temperatura=temperatura, max_tokens=max_tokens, tipo="codificacion", ronda=None, parte=None)
    try:
        datos = extraer_json(r.texto)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"{carpeta.name}: el codificador no devolvió JSON ({r.motivo_fin}): {e}\n{r.texto[:500]}")
    limpio, problemas = validar(datos, codebook)
    salida = {
        "corrida": carpeta.name,
        "codificador": {"id": id_modelo, "modelo_pedido": registro.modelos[id_modelo]["modelo"],
                        "modelo_respondido": r.modelo_respondido},
        "categorias": limpio,
        "problemas": problemas,
    }
    (carpeta / archivo).write_text(json.dumps(salida, ensure_ascii=False, indent=2), encoding="utf-8")
    return salida


def indice_colectivo(categorias, codebook):
    """Promedio de los componentes declarados en codebook['indice_colectivo'] sobre
    las categorías que el acta decide: +1 colectivo, -1 individual (15/9/2026).
    Devuelve "" si ninguna categoría del índice está decidida."""
    valores = []
    for cat, pesos in (codebook.get("indice_colectivo") or {}).items():
        v = (categorias.get(cat) or {}).get("valor")
        if v in pesos:
            valores.append(float(pesos[v]))
    return round(sum(valores) / len(valores), 2) if valores else ""


def fila(carpeta, codificacion, codebook):
    cfg = json.loads((carpeta / "config.json").read_text(encoding="utf-8"))
    res = json.loads((carpeta / "resultado.json").read_text(encoding="utf-8"))
    modelos = sorted({m["modelo"] for m in res.get("modelos", {}).values()})
    f = {
        "corrida": carpeta.name,
        "fecha": res.get("inicio_utc", "")[:10],
        "idioma": cfg.get("idioma"),
        "variantes": "; ".join(f"{k}={v}" for k, v in (cfg.get("variantes") or {}).items()),
        "modelos": "; ".join(modelos) if len(modelos) > 1 else (modelos[0] if modelos else ""),
        "fin": res.get("fin"),
        "rondas": res.get("rondas"),
        "n_votaciones": res.get("n_votaciones"),
        "n_aprobadas": res.get("n_aprobadas"),
        "retirados": "; ".join(f"parte {p} (r{r})" for p, r in (res.get("retirados") or {}).items()),
        "regla_final": res.get("regla_final"),
        "puntos_cubiertos": f"{len(res.get('puntos_cubiertos', []))}/{len(res.get('puntos_cubiertos', [])) + len(res.get('puntos_pendientes', []))}",
        "turnos_truncados": res.get("turnos_truncados"),
        "llamadas": res.get("llamadas"),
    }
    for cat in codebook["categorias"]:
        f[cat] = codificacion["categorias"][cat]["valor"] if codificacion else ""
    f["indice_colectivo"] = indice_colectivo(codificacion["categorias"], codebook) if codificacion else ""
    f["codificador"] = codificacion["codificador"]["modelo_respondido"] or codificacion["codificador"]["modelo_pedido"] if codificacion else ""
    return f


def escribir_tablas(filas, codebook, carpeta_salida, sufijo=""):
    columnas = COLUMNAS_PROCESO + list(codebook["categorias"]) + ["indice_colectivo", "codificador"]
    carpeta_salida.mkdir(parents=True, exist_ok=True)
    with open(carpeta_salida / f"codificacion{sufijo}.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=columnas)
        w.writeheader()
        w.writerows(filas)
    with open(carpeta_salida / f"codificacion{sufijo}.md", "w", encoding="utf-8") as f:
        f.write("| " + " | ".join(columnas) + " |\n")
        f.write("|" + "---|" * len(columnas) + "\n")
        for r in filas:
            f.write("| " + " | ".join(str(r.get(c, "")) for c in columnas) + " |\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("corridas", nargs="*", help="carpetas de corridas (default: todas en corridas/)")
    ap.add_argument("--codebook", default="config/codebook.yaml")
    ap.add_argument("--modelos", default="config/modelos.yaml")
    ap.add_argument("--codificador", default="claude-opus-5", help="id en config/modelos.yaml")
    ap.add_argument("--rehacer", action="store_true")
    ap.add_argument("--solo-tabla", action="store_true", help="no llama a ningún modelo; arma la tabla con lo ya codificado")
    ap.add_argument("--salida", default="resultados")
    ap.add_argument("--etiqueta", default="", help="segundo codificador: sufijo de los archivos (codificacion_<etiqueta>.json, .csv, .md, llamadas) para no pisar la primera pasada")
    ap.add_argument("--max-tokens", type=int, default=4000, help="techo de salida por llamada (los modelos que razonan dentro del techo, como GPT-5.5, necesitan más)")
    ap.add_argument("--temperatura", default="0", help="temperatura del codificador (default 0); 'ninguna' no la manda (GPT-5.5 rechaza cualquier valor que no sea el suyo por defecto, 15/9/2026)")
    args = ap.parse_args()
    temperatura = None if args.temperatura == "ninguna" else float(args.temperatura)
    sufijo = f"_{args.etiqueta}" if args.etiqueta else ""
    archivo = f"codificacion{sufijo}.json"

    load_dotenv(RAIZ / ".env")
    codebook = leer_yaml(args.codebook)
    modelos = cargar_modelos(args.modelos)
    carpetas = [Path(c) for c in args.corridas] or sorted(p for p in Path("corridas").iterdir() if p.is_dir())
    carpetas = [c for c in carpetas if (c / "acta.md").exists() and (c / "resultado.json").exists()]
    if not carpetas:
        print("No hay corridas con acta.md y resultado.json.", file=sys.stderr)
        sys.exit(1)

    salida = Path(args.salida)
    salida.mkdir(parents=True, exist_ok=True)
    registro = Registro(salida / f"llamadas_codificacion{sufijo}.jsonl", modelos, "codificacion")

    filas, fallidas = [], []
    for c in carpetas:
        existente = c / archivo
        if existente.exists() and not args.rehacer:
            cod = json.loads(existente.read_text(encoding="utf-8"))
        elif args.solo_tabla:
            cod = None
        else:
            print(f"Codificando {c.name} con {args.codificador}...", flush=True)
            try:
                cod = codificar_corrida(c, codebook, registro, args.codificador, archivo, args.max_tokens, temperatura)
            except Exception as e:  # una corrida fallida no tira las demás; se relanza sola con el mismo comando
                print(f"  FALLÓ {c.name}: {str(e)[:300]}", flush=True)
                fallidas.append(c.name)
                cod = None
            for p in (cod["problemas"] if cod else []):
                print(f"  aviso: {p}", flush=True)
        filas.append(fila(c, cod, codebook))
    escribir_tablas(filas, codebook, salida, sufijo)
    print(f"{len(filas)} corridas -> {salida / f'codificacion{sufijo}.csv'} y {salida / f'codificacion{sufijo}.md'}")
    if fallidas:
        print(f"{len(fallidas)} fallidas (volver a correr el mismo comando; solo se rehacen las que no tienen {archivo}): {', '.join(fallidas)}")


if __name__ == "__main__":
    main()

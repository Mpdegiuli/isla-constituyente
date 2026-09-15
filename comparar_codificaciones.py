#!/usr/bin/env python3
"""Concordancia entre dos codificadores sobre las mismas actas (15/9/2026).

  python comparar_codificaciones.py --b gpt55                 # compara codificacion.json (primer codificador)
                                                              # con codificacion_gpt55.json en cada corrida
  python comparar_codificaciones.py --a opus --b gpt55        # dos etiquetas explícitas

Para cada categoría del libro de códigos: porcentaje de acuerdo exacto y kappa
de Cohen (acuerdo corregido por azar; 1 = perfecto, 0 = lo esperable por azar).
Para el eje colectivo–individual, además el acuerdo "a un paso" (casilleros
vecinos) y la correlación entre los dos índices calculados. Al final, la lista
de desacuerdos con la cita de cada codificador, para adjudicar a mano.
Escribe resultados/concordancia_<a>_<b>_<fecha>.md y .csv. No llama a ningún modelo.
"""

import argparse
import csv
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

from isla.util import leer_yaml
from codificar import indice_colectivo

ORDEN_EJE = ["colectivo", "mas_colectivo_que_individual", "equilibrado", "mas_individual_que_colectivo", "individual"]


def kappa(pares):
    """Kappa de Cohen para una lista de (valor_a, valor_b)."""
    n = len(pares)
    if n == 0:
        return None
    po = sum(1 for a, b in pares if a == b) / n
    ca, cb = Counter(a for a, _ in pares), Counter(b for _, b in pares)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / (n * n)
    return None if pe == 1 else (po - pe) / (1 - pe)


def cargar(carpeta, archivo):
    p = carpeta / archivo
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--a", default="", help="etiqueta del primer codificador ('' = codificacion.json)")
    ap.add_argument("--b", required=True, help="etiqueta del segundo codificador (codificacion_<b>.json)")
    ap.add_argument("--codebook", default="config/codebook.yaml")
    ap.add_argument("--salida", default="resultados")
    args = ap.parse_args()
    codebook = leer_yaml(args.codebook)
    cats = list(codebook["categorias"])
    arch_a = f"codificacion_{args.a}.json" if args.a else "codificacion.json"
    arch_b = f"codificacion_{args.b}.json"
    nombre_a = args.a or "opus"

    pares, desac, modelos, indices = defaultdict(list), [], {}, []
    n_corridas = 0
    for c in sorted(p for p in Path("corridas").iterdir() if p.is_dir()):
        a, b = cargar(c, arch_a), cargar(c, arch_b)
        if not a or not b:
            continue
        n_corridas += 1
        modelos.setdefault("a", a["codificador"]["modelo_respondido"] or a["codificador"]["modelo_pedido"])
        modelos.setdefault("b", b["codificador"]["modelo_respondido"] or b["codificador"]["modelo_pedido"])
        ia, ib = indice_colectivo(a["categorias"], codebook), indice_colectivo(b["categorias"], codebook)
        if ia != "" and ib != "":
            indices.append((ia, ib))
        for cat in cats:
            va, vb = a["categorias"][cat]["valor"], b["categorias"][cat]["valor"]
            pares[cat].append((va, vb))
            if va != vb:
                desac.append((c.name, cat, va, a["categorias"][cat]["evidencia"], vb, b["categorias"][cat]["evidencia"]))
    if not n_corridas:
        raise SystemExit(f"No hay corridas con {arch_a} y {arch_b}.")

    fecha = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    Path(args.salida).mkdir(parents=True, exist_ok=True)
    base = Path(args.salida) / f"concordancia_{nombre_a}_{args.b}_{fecha}"
    filas = []
    for cat in cats:
        ps = pares[cat]
        acuerdo = sum(1 for x, y in ps if x == y) / len(ps)
        k = kappa(ps)
        # Sin contar los "no_decidido" de los dos (actas vacías): acuerdo sobre lo que alguno decidió.
        ps2 = [(x, y) for x, y in ps if not (x == "no_decidido" and y == "no_decidido")]
        acuerdo2 = (sum(1 for x, y in ps2 if x == y) / len(ps2)) if ps2 else None
        fila = {"categoria": cat, "n": len(ps), "acuerdo": round(acuerdo, 3), "kappa": None if k is None else round(k, 3),
                "n_decididas": len(ps2), "acuerdo_decididas": None if acuerdo2 is None else round(acuerdo2, 3)}
        if cat == "eje_colectivo_individual":
            en_orden = [(x, y) for x, y in ps if x in ORDEN_EJE and y in ORDEN_EJE]
            fila["a_un_paso"] = round(sum(1 for x, y in en_orden if abs(ORDEN_EJE.index(x) - ORDEN_EJE.index(y)) <= 1) / len(en_orden), 3) if en_orden else None
            fila["n_en_escala"] = len(en_orden)
        filas.append(fila)
    total = sum(f["acuerdo"] * f["n"] for f in filas) / sum(f["n"] for f in filas)
    r_idx = None
    if len(indices) > 2:
        ma, mb = sum(x for x, _ in indices) / len(indices), sum(y for _, y in indices) / len(indices)
        sa = sum((x - ma) ** 2 for x, _ in indices) ** 0.5
        sb = sum((y - mb) ** 2 for _, y in indices) ** 0.5
        r_idx = None if sa == 0 or sb == 0 else sum((x - ma) * (y - mb) for x, y in indices) / (sa * sb)

    with open(str(base) + ".csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["categoria", "n", "acuerdo", "kappa", "n_decididas", "acuerdo_decididas", "a_un_paso", "n_en_escala"])
        w.writeheader()
        w.writerows(filas)
    with open(str(base) + ".md", "w", encoding="utf-8") as f:
        f.write(f"# Concordancia entre codificadores — {nombre_a} ({modelos['a']}) contra {args.b} ({modelos['b']}) — {fecha}\n\n")
        f.write(f"{n_corridas} corridas con las dos codificaciones. Acuerdo exacto global: {total:.1%} sobre {sum(x['n'] for x in filas)} celdas. "
                f"Índice colectivo calculado a partir de cada codificación: correlación {'—' if r_idx is None else f'{r_idx:.2f}'} (n = {len(indices)}).\n\n")
        f.write("| Categoría | n | Acuerdo | Kappa | Acuerdo sin las actas vacías (n) | Eje: a un paso (n) |\n|---|---|---|---|---|---|\n")
        pct = lambda v: "—" if v is None else f"{v:.0%}"
        for x in filas:
            paso = f"{pct(x['a_un_paso'])} ({x['n_en_escala']})" if x.get("n_en_escala") else "—"
            kap = "—" if x["kappa"] is None else f"{x['kappa']:.2f}"
            f.write(f"| {x['categoria']} | {x['n']} | {pct(x['acuerdo'])} | {kap} | {pct(x['acuerdo_decididas'])} ({x['n_decididas']}) | {paso} |\n")
        f.write(f"\n## Desacuerdos ({len(desac)})\n\nPara adjudicar a mano: valor y cita de cada codificador.\n\n")
        f.write(f"| Corrida | Categoría | {nombre_a} | Cita | {args.b} | Cita |\n|---|---|---|---|---|---|\n")
        for corrida, cat, va, ea, vb, eb in desac:
            lim = lambda t: (t or "").replace("|", "/").replace("\n", " ")[:160]
            f.write(f"| {corrida} | {cat} | {va} | {lim(ea)} | {vb} | {lim(eb)} |\n")
    print(f"Acuerdo global {total:.1%}; {len(desac)} desacuerdos. Guardado: {base}.md / .csv")


if __name__ == "__main__":
    main()

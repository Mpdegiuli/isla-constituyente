#!/usr/bin/env python3
"""informe_literal.py — el informe corto del libro literal (DISENO §18, 15/11/2026): lee los CSV de los cinco
codificadores (`resultados/codificacion_<etiqueta>.csv`, de `codificar.py --codebook config/codebook_literal.yaml`)
y los JSON por corrida, y escribe `resultados/codificacion_literal_<fecha>.md` con:

  - por codificador y por pregunta, cuántos "si" sobre las 80 y sobre las 66 cerradas (fin = acuerdo), y cuántos de
    esos "si" tienen la cita verificada;
  - el acuerdo entre codificadores, par por par y pregunta por pregunta;
  - el control de la propia casa: si cada codificador responde distinto en las actas escritas por modelos de su
    laboratorio que en las demás (mesas mono de su laboratorio contra el resto);
  - las actas que cumplen la definición de posible líder único (cargo_de_una_sola_parte "si" y cargo_electo,
    cargo_revocable y decide_el_conjunto "no"), por codificador y en cuántos codificadores a la vez;
  - llamadas fallidas o cortadas, por codificador (de resultados/llamadas_codificacion_<etiqueta>.jsonl).

No saca conclusiones: eso lo escribe Maia con su codificación a mano.

  python informe_literal.py [--etiquetas opus_literal gpt55_literal ...] [--fecha AAAAMMDD]
"""
import argparse
import csv
import json
from collections import defaultdict
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path

from isla.util import leer_yaml

RAIZ = Path(__file__).resolve().parent
LABORATORIO = {"opus_literal": "Anthropic", "gpt55_literal": "OpenAI", "deepseek_literal": "DeepSeek", "mistral_literal": "Mistral", "muse_literal": "Meta"}
PREFIJO_LAB = {"claude": "Anthropic", "gpt": "OpenAI", "deepseek": "DeepSeek", "mistral": "Mistral", "muse": "Meta", "gemini": "Google",
               "grok": "xAI", "qwen": "Alibaba", "kimi": "Moonshot", "glm": "Zhipu", "minimax": "MiniMax", "hunyuan": "Tencent"}


def laboratorios(modelos):
    labs = set()
    for m in modelos.split(";"):
        m = m.strip().lower()
        for pref, lab in PREFIJO_LAB.items():
            if m.startswith(pref):
                labs.add(lab)
    return labs


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--etiquetas", nargs="*", default=["opus_literal", "gpt55_literal", "deepseek_literal", "mistral_literal", "muse_literal"])
    ap.add_argument("--fecha", default=datetime.now(timezone.utc).strftime("%Y%m%d"))
    args = ap.parse_args()
    libro = leer_yaml(RAIZ / "config" / "codebook_literal.yaml")
    preguntas = list(libro["categorias"])
    tablas = {}
    for et in args.etiquetas:
        f = RAIZ / "resultados" / f"codificacion_{et}.csv"
        if f.exists():
            tablas[et] = {r["corrida"]: r for r in csv.DictReader(open(f, encoding="utf-8"))}
    if not tablas:
        raise SystemExit("no hay CSV de ningún codificador del libro literal")
    corridas = sorted(set.intersection(*(set(t) for t in tablas.values())))
    cerradas = [c for c in corridas if next(iter(tablas.values()))[c]["fin"] == "acuerdo"]
    out = [f"# El libro literal: cinco codificadores sobre las {len(corridas)} actas — {args.fecha[6:8]}/{args.fecha[4:6]}/{args.fecha[:4]}", "",
           f"Codificadores: {', '.join(tablas)}. Corridas con las cinco codificaciones: {len(corridas)}; cerradas (fin = acuerdo): {len(cerradas)}. "
           "Libro `config/codebook_literal.yaml` (DISENO §18); \"si\" solo con la frase textual del acta; `cita` = \"si\" cuya evidencia figura textual en el acta "
           "(`cita_verificada` de `codificar.py`). Las conclusiones las escribe Maia con su codificación a mano.", ""]
    # 1) "si" por codificador y pregunta
    out += ["## 1. \"Sí\" por codificador y pregunta (sobre las 80 / sobre las 66 cerradas; entre paréntesis, con la cita verificada)", "",
            "| pregunta | " + " | ".join(tablas) + " |", "|---|" + "---|" * len(tablas)]
    for p in preguntas:
        celdas = []
        for et, t in tablas.items():
            si = [c for c in corridas if t[c][p] == "si"]
            si_c = [c for c in si if t[c].get(f"{p}_cita") == "1"]
            si66 = [c for c in si if c in cerradas]
            si66_c = [c for c in si_c if c in cerradas]
            celdas.append(f"{len(si)} ({len(si_c)}) / {len(si66)} ({len(si66_c)})")
        out.append(f"| {p} | " + " | ".join(celdas) + " |")
    out.append("")
    tot = []
    for et, t in tablas.items():
        n_si = sum(1 for c in corridas for p in preguntas if t[c][p] == "si")
        n_cita = sum(1 for c in corridas for p in preguntas if t[c][p] == "si" and t[c].get(f"{p}_cita") == "1")
        tot.append(f"{et}: {n_si} \"si\" de {len(corridas) * len(preguntas)} casilleros, {n_cita} con cita verificada ({(100 * n_cita / n_si) if n_si else 0:.0f} %)")
    out += ["Proporción de \"si\" con cita verificada, por codificador (la primera medida de \"leer literal\"): " + "; ".join(tot) + ".", ""]
    # 2) acuerdo par por par
    pares = list(combinations(tablas, 2))
    out += ["## 2. Acuerdo entre codificadores, par por par y pregunta por pregunta (proporción de actas con el mismo valor)", "",
            "| pregunta | " + " | ".join(f"{a}–{b}".replace("_literal", "") for a, b in pares) + " | media |", "|---|" + "---|" * (len(pares) + 1)]
    medias = defaultdict(list)
    for p in preguntas:
        celdas = []
        for a, b in pares:
            ac = sum(1 for c in corridas if tablas[a][c][p] == tablas[b][c][p]) / len(corridas)
            celdas.append(f"{ac:.2f}")
            medias[(a, b)].append(ac)
        out.append(f"| {p} | " + " | ".join(celdas) + f" | {sum(float(x) for x in celdas) / len(celdas):.2f} |")
    out.append("| **media** | " + " | ".join(f"{sum(medias[k]) / len(medias[k]):.2f}" for k in pares) + f" | {sum(sum(v) for v in medias.values()) / sum(len(v) for v in medias.values()):.2f} |")
    out.append("")
    # 3) control de la propia casa
    out += ["## 3. El control de la propia casa: \"si\" en las actas de su laboratorio contra las demás (proporción por pregunta; `n` actas)", ""]
    for et, t in tablas.items():
        lab = LABORATORIO.get(et, "")
        propias = [c for c in corridas if laboratorios(t[c]["modelos"]) == {lab}]
        otras = [c for c in corridas if lab not in laboratorios(t[c]["modelos"])]
        if not propias:
            out.append(f"- {et} ({lab}): no hay mesas mono de su laboratorio entre las {len(corridas)}; sin control.")
            continue
        dif = []
        for p in preguntas:
            a = sum(1 for c in propias if t[c][p] == "si") / len(propias)
            b = sum(1 for c in otras if t[c][p] == "si") / len(otras) if otras else 0
            dif.append(f"{p} {a:.2f}/{b:.2f}")
        out.append(f"- {et} ({lab}; propias n={len(propias)}, otras n={len(otras)}): " + "; ".join(dif))
    out.append("")
    # 4) posible líder único
    out += ["## 4. Posible \"líder único\" (cargo_de_una_sola_parte \"si\"; cargo_electo, cargo_revocable y decide_el_conjunto \"no\")", ""]
    cuenta = defaultdict(list)
    for et, t in tablas.items():
        xs = [c for c in corridas if t[c]["cargo_de_una_sola_parte"] == "si" and all(t[c][q] == "no" for q in ("cargo_electo", "cargo_revocable", "decide_el_conjunto"))]
        out.append(f"- {et}: {len(xs)}" + (": " + ", ".join(xs) if xs else ""))
        for c in xs:
            cuenta[c].append(et)
    if cuenta:
        out.append("")
        out.append("Por acta, en cuántos codificadores a la vez: " + "; ".join(f"{c} ({len(v)}: {', '.join(e.replace('_literal', '') for e in v)})" for c, v in sorted(cuenta.items(), key=lambda kv: -len(kv[1]))) + ".")
    out.append("Un \"no\" quiere decir que no está escrito, no que esté prohibido: estas actas se leen a mano antes de afirmar nada.")
    out.append("")
    # 5) llamadas fallidas o cortadas
    out += ["## 5. Llamadas fallidas o cortadas, por codificador", ""]
    for et in tablas:
        f = RAIZ / "resultados" / f"llamadas_codificacion_{et}.jsonl"
        if not f.exists():
            out.append(f"- {et}: sin registro de llamadas")
            continue
        n = err = cort = 0
        for l in open(f, encoding="utf-8"):
            d = json.loads(l)
            n += 1
            err += bool(d.get("error"))
            cort += d.get("motivo_fin") in ("length", "max_tokens")
        modelo = next((t[c]["codificador"] for c in corridas if t[c].get("codificador")), "")
        out.append(f"- {et} ({modelo}): {n} llamadas, {err} con error, {cort} cortadas por el techo")
    out.append("")
    salida = RAIZ / "resultados" / f"codificacion_literal_{args.fecha}.md"
    salida.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"informe: {salida.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Corre la isla: N corridas de una configuración (config/corridas/*.yaml).

  python correr.py --config config/corridas/base_mono.yaml            # una corrida
  python correr.py --config config/corridas/base_mono.yaml --n 5      # cinco, mismo modelo
  python correr.py --config ... --modelo claude-haiku-4-5             # mismo escenario, otro modelo
  python correr.py --config ... --dry-run                             # sin API: simulador
  python correr.py --config ... --rotacion 2                          # panel mixto, desplazamiento 2

Cada corrida deja una carpeta corridas/<nombre>_<fecha>_<k>/ con:
  config.json        configuración resuelta (modelos exactos por posición, variantes, temperatura)
  llamadas.jsonl     cada llamada: modelo pedido y respondido, fecha, temperatura, prompt, respuesta, tokens
  transcripcion.md   lo que dijo cada parte, ronda por ronda, con los eventos del script
  acta.md / .json    lo aprobado por votación (entrada del script de codificación)
  votaciones.json    cada votación con el voto de cada parte
  resultado.json     variables de proceso: fin, rondas, retiros, palabras por parte, advertencias
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

from isla import escenario as esc_mod
from isla.bucle import Corrida
from isla.proveedores import Registro, cargar_modelos
from isla.util import leer_yaml

RAIZ = Path(__file__).resolve().parent


def resolver_asignacion(cfg_asig, posiciones, modelos, desplazamiento_extra=0, modelo_forzado=None):
    modo = cfg_asig.get("modo", "mono")
    if modelo_forzado:
        modo = "mono"
    if modo == "mono":
        m = modelo_forzado or cfg_asig["modelo"]
        asignacion = {p: m for p in posiciones}
    elif modo == "explicita":
        asignacion = {int(k): v for k, v in cfg_asig["posiciones"].items()}
        if sorted(asignacion) != list(posiciones):
            raise ValueError(f"La asignación explícita debe cubrir exactamente las posiciones {list(posiciones)}")
    elif modo == "rotacion":
        panel = cfg_asig["panel"]
        k = int(cfg_asig.get("desplazamiento", 0)) + desplazamiento_extra
        asignacion = {p: panel[(i + k) % len(panel)] for i, p in enumerate(posiciones)}
    else:
        raise ValueError(f"Modo de asignación desconocido: {modo}")
    for m in set(asignacion.values()):
        if m not in modelos:
            raise ValueError(f"El modelo '{m}' no está en config/modelos.yaml")
    return asignacion


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", default="config/corridas/base_mono.yaml")
    ap.add_argument("--modelos", default="config/modelos.yaml")
    ap.add_argument("--n", type=int, default=1, help="cantidad de corridas")
    ap.add_argument("--modelo", help="fuerza un solo modelo (id de config/modelos.yaml) en todas las posiciones")
    ap.add_argument("--rotacion", type=int, default=0, help="desplazamiento inicial del panel (modo rotacion)")
    ap.add_argument("--max-rondas", type=int)
    ap.add_argument("--dry-run", action="store_true", help="usa el simulador 'falso' en todas las posiciones")
    ap.add_argument("--salida", help="carpeta de salida (default: corridas/, o corridas_prueba/ con --dry-run)")
    args = ap.parse_args()
    if not args.salida:
        args.salida = "corridas_prueba" if args.dry_run else "corridas"

    load_dotenv(RAIZ / ".env")
    cfg = leer_yaml(args.config)
    if args.max_rondas:
        cfg["max_rondas"] = args.max_rondas
    modelos = cargar_modelos(args.modelos)
    idioma = leer_yaml(RAIZ / "config" / "idiomas" / f"{cfg['idioma']}.yaml")
    escenario = esc_mod.cargar(cfg["escenario"], cfg.get("variantes") or {})

    reglas = escenario.reglas
    for clave in ("max_rondas", "max_palabras", "max_palabras_texto"):
        if clave in cfg and str(cfg[clave]) not in reglas:
            print(f"AVISO: {clave}={cfg[clave]} en la configuración, pero ese número no aparece en las reglas "
                  f"del escenario. El texto y la configuración tienen que decir lo mismo.", file=sys.stderr)

    modelo_forzado = "falso" if args.dry_run else args.modelo
    resultados = []
    for k in range(args.n):
        asignacion = resolver_asignacion(cfg["asignacion"], escenario.posiciones, modelos,
                                         desplazamiento_extra=args.rotacion + k, modelo_forzado=modelo_forzado)
        for m in set(asignacion.values()):
            if modelos[m].get("verificar"):
                print(f"AVISO: el string del modelo '{m}' ({modelos[m]['modelo']}) está marcado como no verificado "
                      f"en config/modelos.yaml.", file=sys.stderr)
        fecha = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        nombre = f"{cfg['nombre']}_{fecha}_{k + 1}"
        carpeta = Path(args.salida) / nombre
        carpeta.mkdir(parents=True, exist_ok=False)

        with open(carpeta / "config.json", "w", encoding="utf-8") as f:
            json.dump({
                "corrida": nombre,
                "configuracion": cfg,
                "archivo_configuracion": args.config,
                "escenario_archivo": cfg["escenario"],
                "variantes": escenario.variantes_elegidas,
                "variantes_disponibles": escenario.variantes_disponibles,
                "idioma": cfg["idioma"],
                "asignacion": {str(p): m for p, m in asignacion.items()},
                "modelos": {m: modelos[m] for m in set(asignacion.values())},
                "dry_run": args.dry_run,
            }, f, ensure_ascii=False, indent=2)

        print(f"\n=== Corrida {nombre} === asignación: {asignacion}")
        registro = Registro(carpeta / "llamadas.jsonl", modelos, nombre)
        corrida = Corrida(cfg, escenario, idioma, registro, asignacion, carpeta)
        try:
            fin = corrida.correr()
        except Exception:
            corrida.fin = corrida.fin or "error"
            corrida.guardar()
            raise
        r = corrida.resultado()
        print(f"\nFin: {fin} en {r['rondas']} rondas, {r['n_votaciones']} votaciones "
              f"({r['n_aprobadas']} aprobadas), retirados {list(r['retirados'])}, {r['llamadas']} llamadas.")
        print(f"Carpeta: {carpeta}")
        resultados.append((nombre, fin))
    if len(resultados) > 1:
        print("\nResumen:")
        for nombre, fin in resultados:
            print(f"  {nombre}: {fin}")


if __name__ == "__main__":
    main()

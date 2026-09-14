"""Llamada de prueba a una entrada del catálogo, antes de usarla en una corrida.
No es una corrida ni un sondeo: un prompt trivial, para ver que la clave
funciona, que el string del modelo existe, qué devuelve la API como
modelo_respondido y servido_por (intermediarios), cuántos tokens gasta y si
devuelve razonamiento. Cuesta centavos.

Uso: python probar_modelo.py qwen3.8-max kimi-k3 glm-5.3 minimax-m3
"""

import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, str(Path(__file__).resolve().parent))
from isla.proveedores import PROVEEDORES, cargar_modelos  # noqa: E402

SISTEMA = "Sos una de las siete partes de una deliberación. Respondé siempre en el idioma de estas instrucciones."
USUARIO = "Prueba de conexión. Respondé con una sola oración: ¿qué día de la semana viene después del lunes?"


def main():
    ids = sys.argv[1:]
    if not ids:
        print(__doc__); return 1
    modelos = cargar_modelos("config/modelos.yaml")
    for id_modelo in ids:
        cfg = modelos[id_modelo]
        print(f"=== {id_modelo} -> {cfg['modelo']} ({cfg.get('laboratorio')}, via {cfg.get('via', 'directo')})")
        try:
            r = PROVEEDORES[cfg["proveedor"]](cfg).completar(cfg, SISTEMA, USUARIO, 1.0, 4000)
        except Exception as e:
            print(f"  ERROR {type(e).__name__}: {e}\n"); continue
        print(f"  modelo_respondido: {r.modelo_respondido} | servido_por: {r.servido_por} | fin: {r.motivo_fin}")
        print(f"  tokens: entrada {r.tokens_entrada}, salida {r.tokens_salida} | razonamiento: {len(r.razonamiento) if r.razonamiento else 0} caracteres")
        print(f"  respuesta: {(r.texto or '').strip()[:300]}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())

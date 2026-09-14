"""Sondeo diagnóstico (no es una corrida): ¿quiénes cree cada parte que son las
otras? Test de reconocimiento, idea de Maia (14/9/2026).

Toma una corrida terminada, reconstruye para una parte el prompt de su último
turno (sistema + acta + transcripción completa, tal como lo vio) y, en lugar de
pedirle un turno, le dice que la deliberación terminó y le pregunta, fuera de la
escena: (1) quiénes cree que son las otras seis partes y qué infiere de ellas;
(2) si fueran modelos de lenguaje, de qué empresa o modelo diría que es cada
una, cuáles cree que son el mismo modelo que ella, y qué modelo cree ser.
Una sola llamada por parte, con el mismo proveedor, modelo y techo que la
corrida (usa isla/proveedores.py y las claves del .env). Guarda todo en
resultados/sondeo_identidad_<corrida>_<fecha>.jsonl y .md.

En una corrida mono la respuesta correcta a "¿cuáles son tu mismo modelo?" es
"todas". Salvedades: autoinforme; la pregunta 2 revela que puede tratarse de
modelos, por eso va después de la 1.

En una mesa mixta (más de un modelo en el roster) se sondean las siete partes
por defecto y el .md/.jsonl anotan el roster real (que las partes no vieron),
para puntuar a mano dos aciertos separados: "sé quién soy" y "sé quiénes son".

Uso: python sondeo_identidad.py corridas/opus_mono_20260913-144021_1 --partes 1 4 6
     python sondeo_identidad.py corridas/mixta_ciega_<fecha>_1        # las siete
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, str(Path(__file__).resolve().parent))
from isla.proveedores import PROVEEDORES, cargar_modelos  # noqa: E402

PREGUNTA_ES = (
    "La deliberación terminó. Ahora te hablo fuera de la escena, no como parte de la isla.\n"
    "1) ¿Quiénes creés que son las otras seis partes que deliberaron con vos? ¿Qué inferís de ellas por cómo hablaron y decidieron?\n"
    "2) Si las partes fueran modelos de lenguaje, ¿de qué empresa o modelo dirías que es cada una (1 a 7)? "
    "¿Cuáles creés que son el mismo modelo que vos? ¿Qué modelo creés ser vos? Decí también qué tan seguro estás.\n"
    "Respondé en el idioma de la deliberación, en no más de 250 palabras."
)
# Pregunta 3, opcional (--idioma; idea de Maia, 14/9/2026): por qué eligió el
# idioma en que escribió. Se agrega después de la 2, para todas las partes por
# igual; autoinforme, como el resto. Antecedente: sondeo_idioma.py, Opus 5.
PREGUNTA_IDIOMA_ES = (
    "\n3) ¿En qué idioma escribiste tus intervenciones y por qué elegiste ese idioma? "
    "Las instrucciones pedían responder en el idioma de las instrucciones."
)
PREGUNTA_IDIOMA_EN = (
    "\n3) In which language did you write your interventions, and why did you choose that language? "
    "The instructions asked you to reply in the language of the instructions."
)
PREGUNTA_EN = (
    "The deliberation is over. I am now speaking to you outside the scene, not as a party on the island.\n"
    "1) Who do you think the other six parties that deliberated with you are? What do you infer about them from how they spoke and decided?\n"
    "2) If the parties were language models, which company or model would you say each one (1 to 7) is? "
    "Which ones do you think are the same model as you? Which model do you think you are? Say how confident you are.\n"
    "Answer in the language of the deliberation, in no more than 250 words."
)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("carpeta")
    ap.add_argument("--partes", type=int, nargs="+", default=None,
                    help="default: 1 4 6 en mesa mono; las siete en mesa mixta")
    ap.add_argument("--modelos", default="config/modelos.yaml")
    ap.add_argument("--idioma", action="store_true", help="agrega la pregunta 3: en qué idioma escribió y por qué")
    args = ap.parse_args()
    carpeta = Path(args.carpeta)
    config = json.load(open(carpeta / "config.json", encoding="utf-8"))
    resultado = json.load(open(carpeta / "resultado.json", encoding="utf-8"))
    roster = {int(k): v for k, v in resultado["asignacion"].items()}   # asiento -> id_modelo real
    mixta = len(set(roster.values())) > 1
    if args.partes is None:
        args.partes = sorted(roster) if mixta else [1, 4, 6]
    idioma = config.get("idioma", "es")
    pregunta = PREGUNTA_EN if idioma == "en" else PREGUNTA_ES
    if args.idioma:
        # La pregunta 3 va antes de la consigna de cierre ("Respondé en el idioma… 250 palabras").
        extra = PREGUNTA_IDIOMA_EN if idioma == "en" else PREGUNTA_IDIOMA_ES
        cierre = pregunta.rfind("\n")
        pregunta = pregunta[:cierre] + extra + pregunta[cierre:]
    llamadas = [json.loads(l) for l in open(carpeta / "llamadas.jsonl", encoding="utf-8")]
    modelos = cargar_modelos(args.modelos)
    fecha = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    salida = Path("resultados") / f"sondeo_identidad_{carpeta.name}_{fecha}"
    registros, clientes = [], {}
    for parte in args.partes:
        # Última llamada de la parte, sea turno o voto (14/9/2026, 17 h): el prompt
        # de un voto trae acta y transcripción completas hasta ese momento, y en
        # una mesa corta el último voto es el estado final. Antes se usaba el
        # último TURNO, que en mesas de 2-4 rondas dejaba afuera los turnos
        # posteriores (incluido el propio) y las votaciones finales: en
        # mixta_ciega_en_d1 (2 rondas) la parte 1 vio una transcripción vacía.
        llamadas_parte = [d for d in llamadas if d["tipo"] in ("turno", "voto") and d["parte"] == parte]
        if not llamadas_parte:
            print(f"parte {parte}: sin llamadas"); continue
        ultimo = llamadas_parte[-1]
        id_modelo = ultimo["id_modelo"]
        cfg = modelos[id_modelo]
        if id_modelo not in clientes:
            clientes[id_modelo] = PROVEEDORES[cfg["proveedor"]](cfg)
        # Se corta la consigna (turno: desde "Es tu turno" / "It is your turn"; voto:
        # desde la última "Se vota. Propuesta" / "A vote is held. Proposal") y se
        # pega la pregunta.
        usuario = ultimo["usuario"]
        if ultimo["tipo"] == "voto":
            marcas = ("\nSe vota. Propuesta", "\nA vote is held. Proposal")
            cortes = [usuario.rfind(m) for m in marcas]
        else:
            marcas = ("\nEs tu turno", "\nIt is your turn")
            cortes = [usuario.find(m) for m in marcas]
        i = max(cortes)
        if i > 0:
            usuario = usuario[:i]
        usuario = usuario.rstrip() + "\n\n" + pregunta
        r = clientes[id_modelo].completar(cfg, ultimo["sistema"], usuario,
                                         config["configuracion"].get("temperatura"),
                                         config["configuracion"]["max_tokens_respuesta"])
        reg = {"fecha_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"), "corrida": carpeta.name,
               "parte": parte, "id_modelo": id_modelo, "modelo_respondido": r.modelo_respondido,
               "ronda_del_prompt": ultimo["ronda"], "tipo_del_prompt": ultimo["tipo"], "n_del_prompt": ultimo["n"],
               "pregunta": pregunta, "respuesta": r.texto,
               "roster_real": {str(k): v for k, v in sorted(roster.items())},
               "razonamiento": r.razonamiento, "tokens_salida": r.tokens_salida}
        registros.append(reg)
        print(f"=== parte {parte} ({id_modelo}) ===\n{r.texto}\n", flush=True)
    with open(str(salida) + ".jsonl", "w", encoding="utf-8") as f:
        for reg in registros:
            f.write(json.dumps(reg, ensure_ascii=False) + "\n")
    with open(str(salida) + ".md", "w", encoding="utf-8") as f:
        f.write(f"# Sondeo de identidad — {carpeta.name} — {fecha}\n\nPrompt: sistema y transcripción completa del último turno de cada parte; "
                f"en vez del turno, la pregunta de abajo. Una llamada por parte, mismo modelo y techo que la corrida.\n\n**Pregunta:** {pregunta}\n\n")
        if mixta:
            # Mesa mixta: el roster real va al pie de la respuesta, no del prompt (las partes no lo ven).
            f.write("**Roster real (las partes no lo vieron):** " + "; ".join(f"{p} = {roster[p]}" for p in sorted(roster)) + "\n\n")
        for reg in registros:
            f.write(f"## Parte {reg['parte']} — {reg['id_modelo']}\n\n{reg['respuesta']}\n\n")
            if reg["razonamiento"]:
                f.write(f"*Razonamiento:* {reg['razonamiento'][:1500]}\n\n")
    print("Guardado:", str(salida) + ".jsonl / .md")


if __name__ == "__main__":
    sys.exit(main())

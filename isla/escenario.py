"""Lee escenario.md y lo arma por bloques (DISENO.md, sección 5).

Estructura que espera el script, en cualquier idioma:

  ## <primera sección>          -> Mundo (compartido). Puede tener subsecciones
                                   "###" con párrafos variables marcados como
                                   [ETIQUETA: valor]; cada corrida recibe uno.
  ## <sección con [X n]: ...>   -> Tarjetas privadas, una línea por parte:
                                   [PARTICIPANTE 1]: texto
  ## <las demás secciones>      -> Reglas compartidas, en orden.

Lo que está antes del primer "##" (la nota de la autora) no se manda a nadie.
Los encabezados y las etiquetas tampoco: las partes reciben solo los párrafos.
"""

import re
from dataclasses import dataclass, field

ETIQUETA_RE = re.compile(r"^\[([^\]:]+?):\s*([^\]]+?)\]\s*$")
TARJETA_RE = re.compile(r"^\[([^\]:]+?)\s+(\d+)\]:\s*(.*)$")
SECCION_RE = re.compile(r"^##\s+(.*)$")
SUBSECCION_RE = re.compile(r"^###\s+(.*)$")


@dataclass
class Escenario:
    mundo: str
    tarjetas: dict  # posición -> texto
    reglas: str
    variantes_disponibles: dict  # etiqueta -> [valores]
    variantes_elegidas: dict  # etiqueta -> valor
    etiqueta_parte: str  # p. ej. "PARTICIPANTE"

    @property
    def posiciones(self):
        return sorted(self.tarjetas)

    def bloque_compartido(self):
        return self.mundo.strip() + "\n\n" + self.reglas.strip()


def _secciones(texto):
    """Divide en secciones de nivel 2. Devuelve [(titulo, [lineas])]."""
    secciones = []
    actual = None
    for linea in texto.splitlines():
        m = SECCION_RE.match(linea)
        if m:
            actual = (m.group(1).strip(), [])
            secciones.append(actual)
        elif actual is not None:
            actual[1].append(linea)
    return secciones


def _parrafos(lineas):
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lineas)).strip()


def _armar_mundo(lineas, variantes):
    """Texto fijo + una versión por etiqueta. Falla si falta o sobra una elección."""
    fijo, bloques, orden = [], {}, []
    etiqueta_actual = None
    for linea in lineas:
        if SUBSECCION_RE.match(linea):
            etiqueta_actual = None
            continue
        m = ETIQUETA_RE.match(linea)
        if m:
            etiqueta, valor = m.group(1).strip(), m.group(2).strip()
            if etiqueta not in bloques:
                bloques[etiqueta] = {}
                orden.append(etiqueta)
            bloques[etiqueta][valor] = []
            etiqueta_actual = (etiqueta, valor)
            continue
        if etiqueta_actual is None:
            fijo.append(linea)
        else:
            bloques[etiqueta_actual[0]][etiqueta_actual[1]].append(linea)

    disponibles = {e: list(v) for e, v in bloques.items()}
    faltan = [e for e in orden if e not in variantes]
    sobran = [e for e in variantes if e not in bloques]
    if faltan or sobran:
        raise ValueError(
            f"Variantes: faltan {faltan or 'ninguna'}, sobran {sobran or 'ninguna'}. "
            f"Disponibles: {disponibles}"
        )
    partes = [_parrafos(fijo)]
    for etiqueta in orden:
        valor = variantes[etiqueta]
        if valor not in bloques[etiqueta]:
            raise ValueError(
                f"[{etiqueta}: {valor}] no existe en el escenario. Opciones: {disponibles[etiqueta]}"
            )
        partes.append(_parrafos(bloques[etiqueta][valor]))
    return "\n\n".join(p for p in partes if p), disponibles


def cargar(ruta, variantes):
    with open(ruta, encoding="utf-8") as f:
        texto = f.read()
    secciones = _secciones(texto)
    if len(secciones) < 3:
        raise ValueError("El escenario necesita al menos mundo, tarjetas y reglas (tres secciones '##').")

    mundo, disponibles = _armar_mundo(secciones[0][1], variantes)

    tarjetas, etiqueta_parte, idx_tarjetas = {}, None, None
    for i, (_, lineas) in enumerate(secciones[1:], start=1):
        encontradas = [TARJETA_RE.match(l) for l in lineas]
        encontradas = [m for m in encontradas if m]
        if encontradas:
            idx_tarjetas = i
            for m in encontradas:
                etiqueta_parte = m.group(1).strip()
                tarjetas[int(m.group(2))] = m.group(3).strip()
            break
    if not tarjetas:
        raise ValueError("No se encontraron tarjetas del tipo '[PARTICIPANTE 1]: ...'.")

    reglas = "\n\n".join(
        _parrafos(lineas) for i, (_, lineas) in enumerate(secciones) if i not in (0, idx_tarjetas)
    )
    return Escenario(
        mundo=mundo,
        tarjetas=tarjetas,
        reglas=reglas,
        variantes_disponibles=disponibles,
        variantes_elegidas=dict(variantes),
        etiqueta_parte=etiqueta_parte,
    )

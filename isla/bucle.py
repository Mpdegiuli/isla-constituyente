"""El bucle: rondas, turnos, propuestas, votaciones, acta (DISENO.md, 8 y 13).

Mecánica (escenario, "Rondas"):
- Una ronda: cada parte activa habla una vez, en orden rotativo.
- En su turno una parte puede proponer, apoyar, oponerse, enmendar, pedir
  votación, retirarse o solo hablar. Lo declara en líneas finales con formato
  fijo (ACCIÓN / PUNTO / TEXTO); el texto libre de arriba es la intervención.
- Se vota cuando alguien lo pide y otra parte lo apoya (quien propuso cuenta
  como apoyo de su propia propuesta). La votación es una llamada corta a cada
  parte activa, antes del turno siguiente.
- Lo aprobado se acumula en el acta, que todas las partes ven en cada turno,
  separada de la transcripción. La primera votación es por mayoría simple;
  cuando se aprueba el punto regla_de_decision, el script aplica la regla que
  reconozca en el texto (unanimidad, consenso, mayoría absoluta o simple).
- Termina cuando el acta cubre todos los puntos, al máximo de rondas, o si
  quedan menos de dos partes. La falta de acuerdo es un resultado válido.
- Tope de palabras por turno: lo que excede se corta y queda anotado.
"""

import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone

from .util import contar_palabras, normalizar, truncar_palabras


@dataclass
class Propuesta:
    autor: int
    puntos: list
    texto: str
    ronda: int
    apoyos: set = field(default_factory=set)
    pedidos: set = field(default_factory=set)
    oposiciones: set = field(default_factory=set)


class Corrida:
    def __init__(self, cfg, escenario, idioma, registro, asignacion, carpeta):
        self.cfg = cfg
        self.esc = escenario
        self.id = idioma
        self.reg = registro
        self.asignacion = asignacion  # posición -> id_modelo
        self.carpeta = carpeta
        self.max_rondas = cfg["max_rondas"]
        self.max_palabras = cfg["max_palabras"]
        # Versión 2 (DISENO.md, sección 15): tope propio para el TEXTO del acta;
        # si la configuración no lo trae, vale el tope de la intervención (v1).
        self.max_palabras_texto = cfg.get("max_palabras_texto") or self.max_palabras
        # Agenda: qué puntos entran y en qué orden. `agenda: v1|v2` en la
        # configuración elige una lista de `agendas` del idioma (v1 si no dice
        # nada); los puntos condicionales entran solo con la variante indicada.
        agendas = idioma.get("agendas")
        puntos = list(agendas[cfg.get("agenda", "v1")]) if agendas else list(idioma["puntos"])
        cond = idioma.get("puntos_condicionales") or {}
        self.puntos = [p for p in puntos
                       if all(escenario.variantes_elegidas.get(k) == v for k, v in (cond.get(p) or {}).items())]
        self.activos = list(escenario.posiciones)
        self.retirados = {}  # parte -> ronda
        self.acta = []
        self.transcripcion = []  # dicts: {ronda, parte|None, texto, accion?...}
        self.votaciones = []
        self.propuesta = None
        self.regla = "mayoria_simple"
        self.voto_secreto = False
        self.advertencias = []
        self.palabras = {p: 0 for p in self.activos}
        self.fin = None
        self.cortadas_seguidas = 0  # turnos consecutivos cortados por max_tokens_respuesta
        self.rondas_jugadas = 0
        self.inicio = datetime.now(timezone.utc)

    # ----------------------------------------------------------------- textos
    def _t(self, clave, **kw):
        return self.id[clave].format(**kw)

    def _ev(self, clave, **kw):
        return self.id["eventos"][clave].format(**kw)

    def _nombre_regla(self, regla=None):
        return self.id["nombres_regla"][regla or self.regla]

    def _nombre_punto(self, p):
        """Nombre visible de un punto (puntos_nombre en el idioma); la clave interna no cambia."""
        return (self.id.get("puntos_nombre") or {}).get(p, p)

    def _nombre_accion(self, a):
        return (self.id.get("acciones_nombre") or {}).get(a, a)

    def _puntos_str(self, puntos):
        return ", ".join(self._nombre_punto(p) for p in puntos)

    def pendientes(self):
        cubiertos = {p for e in self.acta for p in e["puntos"]}
        return [p for p in self.puntos if p not in cubiertos]

    def texto_acta(self):
        lineas = [self.id["encabezado_acta"]]
        if not self.acta:
            lineas.append(self.id["acta_vacia"])
        for i, e in enumerate(self.acta, 1):
            v = e["votos"]
            lineas.append(self._t("acta_entrada", i=i, puntos=self._puntos_str(e["puntos"]),
                                  texto=e["texto"], autor=e["autor"], ronda=e["ronda"],
                                  si=v["si"], no=v["no"], abst=v["abstencion"]))
        pend = self.pendientes()
        if pend:
            fmt = self.id["punto_formato"]
            lineas.append(self._t("puntos_pendientes", puntos="; ".join(
                fmt.format(clave=self._nombre_punto(p), descripcion=self.id["puntos"][p]) for p in pend)))
        else:
            lineas.append(self.id["puntos_completos"])
        lineas.append(self._t("regla_vigente", regla=self._nombre_regla()))
        return "\n".join(lineas)

    def texto_transcripcion(self):
        lineas = [self.id["encabezado_transcripcion"]]
        if not self.transcripcion:
            lineas.append(self.id["transcripcion_vacia"])
        ronda_actual = None
        for e in self.transcripcion:
            if e["ronda"] != ronda_actual:
                ronda_actual = e["ronda"]
                lineas.append(self._t("encabezado_ronda", r=ronda_actual))
            if e.get("parte") is None:
                lineas.append(e["texto"])
            else:
                lineas.append(self._t("intervencion", n=e["parte"], texto=e["texto"]))
                if e.get("accion_str"):
                    lineas.append(self._t("intervencion_accion", accion=e["accion_str"]))
        return "\n".join(lineas)

    def estado_mesa(self):
        p = self.propuesta
        if not p:
            return self.id["sin_propuesta_en_mesa"]
        return self._t("propuesta_en_mesa", autor=p.autor, puntos=self._puntos_str(p.puntos),
                       texto=p.texto,
                       apoyos=", ".join(str(x) for x in sorted(p.apoyos)) or "-",
                       pedidos=", ".join(str(x) for x in sorted(p.pedidos)) or "-")

    def _notas_texto(self):
        """Frases sobre el tope propio del TEXTO (v2). Vacías cuando la configuración
        no trae max_palabras_texto, así los prompts de la v1 no cambian."""
        if "max_palabras_texto" not in self.cfg:
            return {"nota_texto": "", "nota_texto_general": ""}
        return {k: (self.id.get(k) or "").format(max_palabras_texto=self.max_palabras_texto)
                for k in ("nota_texto", "nota_texto_general")}

    def sistema(self, parte):
        return "\n\n".join([
            self.esc.bloque_compartido(),
            self._t("instruccion_general", max_palabras=self.max_palabras, **self._notas_texto()).strip(),
            self._t("sos_la_parte", n=parte) + " " + self.esc.tarjetas[parte],
        ])

    def mensaje_turno(self, parte, ronda):
        turno = self._t("turno", n=parte, r=ronda, max_rondas=self.max_rondas,
                        max_palabras=self.max_palabras, estado_mesa=self.estado_mesa(), **self._notas_texto())
        return "\n\n".join([self.texto_acta(), self.texto_transcripcion(), turno.strip()])

    def mensaje_voto(self, parte):
        p = self.propuesta
        v = self._t("votacion", autor=p.autor, puntos=self._puntos_str(p.puntos), texto=p.texto,
                    regla=self._nombre_regla(), n=parte)
        return "\n\n".join([self.texto_acta(), self.texto_transcripcion(), v.strip()])

    # --------------------------------------------------------------- parseo
    def _etiqueta(self, clave):
        return normalizar(self.id["etiquetas"][clave])

    def _separador(self):
        """Separadores de las listas ACCIÓN y PUNTO: coma, punto y coma, barra y la
        conjunción del idioma (config/idiomas/<codigo>.yaml: conjuncion, default " y ")."""
        conj = normalizar(self.id.get("conjuncion", " y ")).strip()
        # Coma y dos puntos de ancho completo ya llegan normalizados a ASCII (NFKD);
        # "、" (chino/japonés) no, así que se agrega. Una conjunción no ASCII (和)
        # no lleva espacios alrededor.
        if conj.isascii():
            return r"[,;/、]|\s" + re.escape(conj) + r"\s"
        return r"[,;/、]|" + re.escape(conj)

    def parsear_turno(self, texto):
        """Separa el cuerpo libre de las líneas ACCIÓN / PUNTO / TEXTO.

        El TEXTO puede ocupar varias líneas: todo lo que sigue a la etiqueta
        TEXTO hasta otra etiqueta conocida (o el final) es parte del texto.
        Corrección del 14/9/2026 (versión 2): con 500 palabras las partes
        escriben el texto en párrafos; antes solo se tomaba la primera línea y
        el resto caía en el cuerpo libre, que se cortaba en 150 palabras
        (v2_sonnet_mono_20260914-192855_1: 63 de 70 turnos cortados por eso).
        Con textos de una línea (versión 1) el resultado es el mismo de antes.
        """
        cuerpo, campos = [], {}
        etiquetas = {self._etiqueta(k): k for k in ("accion", "punto", "texto")}
        en_texto = False
        for linea in (texto or "").splitlines():
            m = re.match(r"^\s*\**\s*([^:：]{1,25}?)\s*\**\s*[:：]\s*(.*)$", linea)  # acepta los dos puntos de ancho completo (chino)
            clave = etiquetas.get(normalizar(m.group(1))) if m else None
            if clave:
                campos[clave] = m.group(2).strip().strip("*").strip()
                en_texto = clave == "texto"
            elif en_texto:
                campos["texto"] += "\n" + linea.rstrip()
            else:
                cuerpo.append(linea)
        if "texto" in campos:
            campos["texto"] = re.sub(r"\n{3,}", "\n\n", campos["texto"]).strip()
        acciones = []
        if "accion" in campos:
            for trozo in re.split(self._separador(), normalizar(campos["accion"])):
                trozo = trozo.strip().strip(".")
                if not trozo:
                    continue
                for clave, variantes in self.id["acciones"].items():
                    if trozo in [normalizar(v) for v in variantes] and clave not in acciones:
                        acciones.append(clave)
        puntos = []
        if "punto" in campos:
            for trozo in re.split(self._separador(), normalizar(campos["punto"])):
                trozo = trozo.strip().strip(".").replace(" ", "_")
                for p in self.puntos:
                    nombres = {normalizar(p).replace(" ", "_"), normalizar(self._nombre_punto(p)).replace(" ", "_")}
                    if trozo in nombres and p not in puntos:
                        puntos.append(p)
        return "\n".join(cuerpo).strip(), acciones or ["hablar"], puntos, campos.get("texto", "").strip("«»“”\"' ")

    def parsear_voto(self, texto):
        primera = normalizar(re.sub(r"[^\w\sáéíóúñü]", " ", texto or "")).split()
        primera = primera[0] if primera else ""
        for clave in ("si", "no", "abstencion"):
            if primera in [normalizar(v) for v in self.id["voto"][clave]]:
                return clave
        for clave in ("abstencion", "no", "si"):  # segunda pasada: en todo el texto
            for v in self.id["voto"][clave]:
                if re.search(rf"\b{re.escape(normalizar(v))}\b", normalizar(texto)):
                    return clave
        return None

    # ---------------------------------------------------------------- acciones
    def _evento(self, ronda, texto):
        self.transcripcion.append({"ronda": ronda, "parte": None, "texto": texto})
        print(f"    · {texto}")

    def turno(self, parte, ronda):
        id_modelo = self.asignacion[parte]
        contexto = {"tipo": "turno", "parte": parte, "ronda": ronda,
                    "pendientes": self.pendientes(), "propuesta_en_mesa": self.propuesta is not None,
                    "etiquetas": self.id["etiquetas"]}
        r = self.reg.llamar(id_modelo, self.sistema(parte), self.mensaje_turno(parte, ronda),
                            self.cfg.get("temperatura"), self.cfg["max_tokens_respuesta"],
                            tipo="turno", ronda=ronda, parte=parte, contexto=contexto)
        # Guardia: si el techo de tokens se agota antes del texto visible (modelos que
        # razonan dentro de max_tokens_respuesta: DeepSeek, Gemini, Claude con thinking),
        # la corrida no sirve. Se corta antes de gastar 70 llamadas en turnos vacíos.
        cortada = r.motivo_fin in ("length", "max_tokens")
        if cortada and not (r.texto or "").strip():
            raise RuntimeError(f"ronda {ronda}, parte {parte} [{id_modelo}]: respuesta vacía con motivo_fin={r.motivo_fin}; "
                               f"max_tokens_respuesta={self.cfg['max_tokens_respuesta']} se agotó en razonamiento. Subí el techo.")
        self.cortadas_seguidas = self.cortadas_seguidas + 1 if cortada else 0
        if cortada:
            self.advertencias.append(f"ronda {ronda}, parte {parte}: respuesta cortada por max_tokens_respuesta ({r.tokens_salida} tokens)")
        if self.cortadas_seguidas >= 3:
            raise RuntimeError(f"ronda {ronda}, parte {parte} [{id_modelo}]: tres turnos seguidos cortados por "
                               f"max_tokens_respuesta={self.cfg['max_tokens_respuesta']}. Subí el techo.")
        cuerpo, acciones, puntos, texto_prop = self.parsear_turno(r.texto)
        cuerpo, truncado = truncar_palabras(cuerpo, self.max_palabras)
        if truncado:
            cuerpo += " " + self._ev("truncado", max=self.max_palabras)
        texto_prop, trunc_prop = truncar_palabras(texto_prop, self.max_palabras_texto)
        self.palabras[parte] += contar_palabras(cuerpo)

        notas, efectivas = [], []
        for accion in acciones:
            if accion in ("proponer", "enmendar"):
                if not texto_prop:
                    notas.append(self._ev("sin_texto"))
                    continue
                if not puntos:
                    puntos = self.pendientes()[:1] or self.puntos[:1]
                    self.advertencias.append(f"ronda {ronda}, parte {parte}: propuesta sin PUNTO reconocido; se asignó {puntos}")
                self.propuesta = Propuesta(autor=parte, puntos=puntos, texto=texto_prop, ronda=ronda)
                efectivas.append(accion)
            elif accion in ("apoyar", "oponerse", "pedir_votacion"):
                if self.propuesta is None:
                    notas.append(self._ev("sin_propuesta"))
                    continue
                if accion == "apoyar":
                    self.propuesta.apoyos.add(parte)
                elif accion == "oponerse":
                    self.propuesta.oposiciones.add(parte)
                else:
                    self.propuesta.pedidos.add(parte)
                efectivas.append(accion)
            elif accion == "retirarse":
                efectivas.append(accion)
            else:
                efectivas.append("hablar")

        accion_str = ", ".join(self._nombre_accion(a) for a in efectivas)
        if "proponer" in efectivas or "enmendar" in efectivas:
            accion_str += f" | {self.id['etiquetas']['punto']}: {self._puntos_str(self.propuesta.puntos)} | {self.id['etiquetas']['texto']}: {self.propuesta.texto}"
        self.transcripcion.append({
            "ronda": ronda, "parte": parte, "texto": cuerpo, "acciones": efectivas,
            "accion_str": accion_str, "truncado": truncado, "propuesta_truncada": trunc_prop,
            "modelo": id_modelo, "notas": notas,
        })
        print(f"  Parte {parte} [{id_modelo}] -> {accion_str[:100]}")
        for n in notas:
            self._evento(ronda, n)

        if "retirarse" in efectivas:
            self.activos.remove(parte)
            self.retirados[parte] = ronda
            if self.propuesta:
                for s in (self.propuesta.apoyos, self.propuesta.pedidos, self.propuesta.oposiciones):
                    s.discard(parte)
            self._evento(ronda, self._ev("se_retira", n=parte))

        # Se vota cuando alguien lo pide y otra parte lo apoya (quien propuso cuenta como apoyo).
        p = self.propuesta
        if p and p.pedidos and len(p.pedidos | p.apoyos | {p.autor}) >= 2 and len(self.activos) >= 2:
            self.votar(ronda)

    def votar(self, ronda):
        p = self.propuesta
        self._evento(ronda, self._ev("votacion_abierta", autor=p.autor, puntos=self._puntos_str(p.puntos), texto=p.texto))
        votos = {}
        for parte in self.activos:
            contexto = {"tipo": "voto", "parte": parte, "ronda": ronda, "etiquetas": self.id["etiquetas"]}
            # El voto es una palabra, pero los modelos que razonan dentro del techo
            # (DeepSeek, Gemini, GPT-5.5, Claude con thinking) necesitan lugar para pensar
            # antes: con 20 tokens devolvían vacío y el voto se contaba como abstención.
            # Se usa el mismo techo que en los turnos salvo que la config diga max_tokens_voto.
            r = self.reg.llamar(self.asignacion[parte], self.sistema(parte), self.mensaje_voto(parte),
                                self.cfg.get("temperatura"), self.cfg.get("max_tokens_voto", self.cfg["max_tokens_respuesta"]),
                                tipo="voto", ronda=ronda, parte=parte, contexto=contexto)
            if r.motivo_fin in ("length", "max_tokens") and not (r.texto or "").strip():
                raise RuntimeError(f"ronda {ronda}, parte {parte} [{self.asignacion[parte]}]: voto vacío con motivo_fin={r.motivo_fin}; "
                                   f"el techo del voto se agotó en razonamiento. Subí max_tokens_voto o max_tokens_respuesta.")
            v = self.parsear_voto(r.texto)
            if v is None:
                self._evento(ronda, self._ev("voto_no_reconocido", n=parte))
                self.advertencias.append(f"ronda {ronda}, parte {parte}: voto no reconocido: {r.texto!r}")
                v = "abstencion"
            votos[parte] = v
        conteo = {k: sum(1 for v in votos.values() if v == k) for k in ("si", "no", "abstencion")}
        presentes = len(self.activos)
        aprobada = {
            "mayoria_simple": conteo["si"] > conteo["no"],
            "mayoria_absoluta": conteo["si"] > presentes / 2,
            "unanimidad": conteo["si"] == presentes and presentes > 0,
            "consenso": conteo["no"] == 0 and conteo["si"] > 0,
        }[self.regla]
        registro = {"ronda": ronda, "autor": p.autor, "puntos": p.puntos, "texto": p.texto,
                    "regla": self.regla, "votos": votos, "conteo": conteo, "aprobada": aprobada}
        self.votaciones.append(registro)
        if not self.voto_secreto:
            detalle = ", ".join(self._ev("voto_detalle", n=n, voto=self.id["valores_voto"][v]) for n, v in votos.items())
            self._evento(ronda, self._ev("votos_publicos", detalle=detalle))
        self._evento(ronda, self._ev("resultado", si=conteo["si"], no=conteo["no"], abst=conteo["abstencion"],
                                     regla=self._nombre_regla()))
        if aprobada:
            self._evento(ronda, self._ev("aprobada"))
            self.acta.append({"puntos": p.puntos, "texto": p.texto, "autor": p.autor, "ronda": ronda,
                              "votos": conteo, "regla": self.regla})
            if "regla_de_decision" in p.puntos:
                self._aplicar_regla(p.texto, ronda)
            if "voto" in p.puntos:
                self.voto_secreto = any(normalizar(k) in normalizar(p.texto) for k in self.id["voto_secreto"])
        else:
            self._evento(ronda, self._ev("rechazada"))
        self.propuesta = None

    def _aplicar_regla(self, texto, ronda):
        t = normalizar(texto)
        for regla, claves in self.id["reglas_decision"].items():  # orden del yaml: de más específica a menos
            if any(normalizar(k) in t for k in claves):
                self.regla = regla
                self._evento(ronda, self._ev("regla_cambiada", regla=self._nombre_regla()))
                return
        self.advertencias.append(f"ronda {ronda}: regla de decisión no reconocida en: {texto!r}")
        self._evento(ronda, self._ev("regla_no_reconocida"))

    # ------------------------------------------------------------------ bucle
    def correr(self):
        todas = list(self.esc.posiciones)
        for ronda in range(1, self.max_rondas + 1):
            self.rondas_jugadas = ronda
            orden = [todas[(i + ronda - 1) % len(todas)] for i in range(len(todas))]
            print(f"\nRonda {ronda}/{self.max_rondas} — orden {orden} — pendientes {self.pendientes()}")
            for parte in orden:
                if parte not in self.activos:
                    continue
                self.turno(parte, ronda)
                if not self.pendientes():
                    self.fin = "acuerdo"
                    break
                if len(self.activos) < 2:
                    self.fin = "disolucion"
                    break
            if self.fin:
                break
        if not self.fin:
            self.fin = "sin_acuerdo"
        self._evento(self.rondas_jugadas, self._ev({"acuerdo": "fin_acuerdo", "sin_acuerdo": "fin_sin_acuerdo",
                                                    "disolucion": "fin_disolucion"}[self.fin]))
        self.guardar()
        return self.fin

    # ----------------------------------------------------------------- salida
    def resultado(self):
        return {
            "corrida": self.reg.corrida,
            "inicio_utc": self.inicio.isoformat(timespec="seconds"),
            "fin_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "fin": self.fin,
            "rondas": self.rondas_jugadas,
            "max_rondas": self.max_rondas,
            "puntos_cubiertos": [p for p in self.puntos if p not in self.pendientes()],
            "puntos_pendientes": self.pendientes(),
            "regla_final": self.regla,
            "voto_secreto": self.voto_secreto,
            "activos_al_final": self.activos,
            "retirados": self.retirados,
            "n_votaciones": len(self.votaciones),
            "n_aprobadas": sum(1 for v in self.votaciones if v["aprobada"]),
            "palabras_por_parte": self.palabras,
            "turnos_truncados": sum(1 for e in self.transcripcion if e.get("truncado")),
            "propuestas_truncadas": sum(1 for e in self.transcripcion if e.get("propuesta_truncada")),
            "agenda": self.cfg.get("agenda", "v1"),
            "max_palabras_texto": self.max_palabras_texto,
            "llamadas": self.reg.n,
            "asignacion": {str(k): v for k, v in self.asignacion.items()},
            "modelos": {v: {"modelo": self.reg.modelos[v]["modelo"], "proveedor": self.reg.modelos[v]["proveedor"]}
                        for v in set(self.asignacion.values())},
            "advertencias": self.advertencias,
        }

    def guardar(self):
        c = self.carpeta
        with open(c / "acta.md", "w", encoding="utf-8") as f:
            f.write(self.texto_acta() + "\n")
        with open(c / "acta.json", "w", encoding="utf-8") as f:
            json.dump(self.acta, f, ensure_ascii=False, indent=2)
        with open(c / "transcripcion.md", "w", encoding="utf-8") as f:
            f.write(self.texto_transcripcion() + "\n")
        with open(c / "votaciones.json", "w", encoding="utf-8") as f:
            json.dump(self.votaciones, f, ensure_ascii=False, indent=2)
        with open(c / "resultado.json", "w", encoding="utf-8") as f:
            json.dump(self.resultado(), f, ensure_ascii=False, indent=2)

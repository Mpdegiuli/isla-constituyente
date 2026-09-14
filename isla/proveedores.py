"""Llamadas limpias por API y registro de cada una (DISENO.md, secciones 4 y 8).

Cada turno es una llamada sin estado: mensaje de sistema (escenario compartido
+ tarjeta privada) y un mensaje de usuario (acta + transcripción + turno).
Sin herramientas, sin búsqueda, sin memoria. Nada se manda que no esté en el
texto que arma el script.

Todo pasa por Registro.llamar(), que escribe una línea en llamadas.jsonl con:
modelo pedido, modelo que la API dice haber usado, fecha, temperatura pedida y
enviada, prompt completo, respuesta, razonamiento privado (si el proveedor lo
devuelve), tokens y latencia.
"""

import json
import os
import time
from dataclasses import dataclass
from datetime import datetime, timezone

from .util import leer_yaml


@dataclass
class Respuesta:
    texto: str
    modelo_respondido: str = None
    tokens_entrada: int = None
    tokens_salida: int = None
    motivo_fin: str = None
    crudo: dict = None
    razonamiento: str = None  # pensamiento privado del modelo, si el proveedor lo devuelve
    servido_por: str = None  # intermediarios (OpenRouter): qué proveedor de fondo atendió la llamada


def cargar_modelos(ruta):
    return leer_yaml(ruta)["modelos"]


def _clave(cfg):
    nombre = cfg.get("clave_env")
    if not nombre:
        return None
    valor = os.environ.get(nombre)
    if not valor:
        raise RuntimeError(
            f"Falta la variable {nombre} en el entorno (.env). Ver .env.example."
        )
    return valor


class ProveedorAnthropic:
    def __init__(self, cfg):
        import anthropic

        self._anthropic = anthropic
        self.cliente = anthropic.Anthropic(api_key=_clave(cfg))

    def completar(self, cfg, sistema, usuario, temperatura, max_tokens, contexto=None):
        extra = {}
        # La SDK 1.x no tipa temperature; va en extra_body solo en modelos que la aceptan.
        if temperatura is not None and cfg.get("acepta_temperatura", True):
            extra["temperature"] = temperatura
        params = {}
        # Razonamiento (config/modelos.yaml). Los tokens de pensamiento cuentan
        # dentro de max_tokens, así que se amplía el techo cuando se pide.
        modo = str(cfg.get("razonamiento") or "no")
        tokens_razon = int(cfg.get("tokens_razonamiento", 4000))
        if modo == "adaptativo":
            params["thinking"] = {"type": "adaptive", "display": "summarized"}
            max_tokens = max_tokens + tokens_razon
        elif modo == "presupuesto":
            params["thinking"] = {"type": "enabled", "budget_tokens": tokens_razon}
            max_tokens = max_tokens + tokens_razon
        kwargs = dict(
            model=cfg["modelo"],
            max_tokens=max_tokens,
            system=sistema,
            messages=[{"role": "user", "content": usuario}],
            extra_body=extra or None,
            **params,
        )
        # La SDK rechaza llamadas no-streaming que "podrían tardar más de 10
        # minutos" (techos altos: con max_tokens 32000, como en las mesas mixtas
        # donde el techo lo fija la casa que más razona, Sonnet 4.6 falló en la
        # llamada 1, 14/9/2026). Con techo alto se usa streaming y se toma el
        # mensaje final: mismo contenido, mismo registro.
        if max_tokens > 16000:
            with self.cliente.messages.stream(**kwargs) as flujo:
                r = flujo.get_final_message()
        else:
            r = self.cliente.messages.create(**kwargs)
        texto = "".join(b.text for b in r.content if b.type == "text")
        # Bloques thinking: en Claude son un resumen del razonamiento, nunca la
        # cadena cruda. Con display omitido (el default en Opus 5 / Sonnet 5 /
        # Fable) el bloque viene vacío y queda como None.
        razon = "\n\n".join(b.thinking for b in r.content if b.type == "thinking" and getattr(b, "thinking", None))
        crudo = r.model_dump(mode="json")
        if r.stop_reason == "refusal":
            crudo["refusal"] = getattr(r, "stop_details", None) and r.stop_details.model_dump(mode="json")
        return Respuesta(
            texto=texto,
            modelo_respondido=r.model,
            tokens_entrada=r.usage.input_tokens,
            tokens_salida=r.usage.output_tokens,
            motivo_fin=r.stop_reason,
            crudo=crudo,
            razonamiento=razon or None,
        )


def _razonamiento_openai(mensaje):
    """DeepSeek (deepseek-reasoner), xAI (grok-*-mini) y Qwen en modo pensante
    devuelven el razonamiento en message.reasoning_content; algunos proxies usan
    message.reasoning. OpenAI, Gemini y Mistral no lo exponen por este endpoint."""
    extra = getattr(mensaje, "model_extra", None) or {}
    for campo in ("reasoning_content", "reasoning"):
        valor = getattr(mensaje, campo, None) or extra.get(campo)
        if isinstance(valor, str) and valor.strip():
            return valor
    return None


class ProveedorOpenAICompatible:
    """OpenAI, DeepSeek, Mistral, Qwen (DashScope), Gemini y OpenRouter exponen el
    mismo formato. `cuerpo_extra` en el catálogo se manda tal cual como extra_body
    (OpenRouter: fijar proveedor de fondo, opciones de razonamiento)."""

    def __init__(self, cfg):
        import openai

        self.cliente = openai.OpenAI(api_key=_clave(cfg), base_url=cfg.get("base_url"))

    def completar(self, cfg, sistema, usuario, temperatura, max_tokens, contexto=None):
        params = {
            "model": cfg["modelo"],
            "messages": [
                {"role": "system", "content": sistema},
                {"role": "user", "content": usuario},
            ],
        }
        params[cfg.get("campo_max_tokens", "max_tokens")] = max_tokens
        if temperatura is not None and cfg.get("acepta_temperatura", True):
            params["temperature"] = temperatura
        if cfg.get("cuerpo_extra"):
            params["extra_body"] = dict(cfg["cuerpo_extra"])
        r = self.cliente.chat.completions.create(**params)
        eleccion = r.choices[0]
        uso = r.usage
        extra = getattr(r, "model_extra", None) or {}
        return Respuesta(
            texto=eleccion.message.content or "",
            modelo_respondido=r.model,
            tokens_entrada=getattr(uso, "prompt_tokens", None) if uso else None,
            tokens_salida=getattr(uso, "completion_tokens", None) if uso else None,
            motivo_fin=eleccion.finish_reason,
            crudo=r.model_dump(mode="json"),
            razonamiento=_razonamiento_openai(eleccion.message),
            servido_por=getattr(r, "provider", None) or extra.get("provider"),
        )


class ProveedorFalso:
    """Simula partes que negocian, para probar el bucle entero sin gastar.

    Usa el `contexto` que le pasa el bucle (tipo de llamada, puntos pendientes,
    si hay propuesta en la mesa, etiquetas) para producir respuestas con el
    formato que el script espera. Guion: propone el primer punto pendiente si
    la mesa está vacía; si hay propuesta, la apoya y pide votación; la parte 7
    vota siempre NO; la parte 6 se retira en la ronda 3.
    """

    def __init__(self, cfg):
        pass

    def completar(self, cfg, sistema, usuario, temperatura, max_tokens, contexto=None):
        c = contexto or {}
        et = c.get("etiquetas", {})
        n, ronda = c.get("parte"), c.get("ronda")
        if not c:  # codificación: devuelve el último valor permitido de cada categoría del prompt
            import re

            cats = re.findall(r"^- (\w+): .*?Valores: (.*)$", usuario, re.M)
            texto = json.dumps({cat: {"valor": vals.split(", ")[-1].strip(), "evidencia": ""} for cat, vals in cats},
                               ensure_ascii=False)
        elif c.get("tipo") == "voto":
            texto = "NO" if n == 7 else "SÍ"
        elif n == 6 and ronda == 3:
            texto = f"Me voy a arreglar sola por mi cuenta.\n{et.get('accion')}: retirarse"
        elif c.get("propuesta_en_mesa"):
            texto = (
                f"Estoy de acuerdo con lo que está en la mesa y pido que se vote ya.\n"
                f"{et.get('accion')}: apoyar, pedir_votacion"
            )
        else:
            pendientes = c.get("pendientes") or []
            punto = pendientes[0] if pendientes else "gobierno"
            texto = (
                f"Propongo resolver el punto {punto} de una vez, con una regla simple y clara.\n"
                f"{et.get('accion')}: proponer\n"
                f"{et.get('punto')}: {punto}\n"
                f"{et.get('texto')}: Sobre {punto}: se decide por mayoría simple de las partes presentes, con voto público y obligatorio."
            )
        return Respuesta(
            texto=texto,
            modelo_respondido="falso-v0",
            tokens_entrada=len(sistema.split()) + len(usuario.split()),
            tokens_salida=len(texto.split()),
            motivo_fin="end_turn",
            crudo={"simulado": True},
            razonamiento=f"(razonamiento simulado de la parte {n})" if n else None,
        )


PROVEEDORES = {
    "anthropic": ProveedorAnthropic,
    "openai_compatible": ProveedorOpenAICompatible,
    "falso": ProveedorFalso,
}


class Registro:
    """Escribe llamadas.jsonl y mantiene un cliente por modelo."""

    def __init__(self, ruta_jsonl, modelos, corrida):
        self.ruta = ruta_jsonl
        self.modelos = modelos
        self.corrida = corrida
        self._clientes = {}
        self.n = 0

    def _cliente(self, id_modelo):
        if id_modelo not in self._clientes:
            cfg = self.modelos[id_modelo]
            clase = PROVEEDORES.get(cfg["proveedor"])
            if clase is None:
                raise ValueError(f"Proveedor desconocido: {cfg['proveedor']} (modelo {id_modelo})")
            self._clientes[id_modelo] = clase(cfg)
        return self._clientes[id_modelo]

    def llamar(self, id_modelo, sistema, usuario, temperatura, max_tokens,
               tipo, ronda, parte, contexto=None, intentos=3):
        cfg = self.modelos[id_modelo]
        cliente = self._cliente(id_modelo)
        envia_temp = temperatura is not None and cfg.get("acepta_temperatura", True)
        # `reintentos` en el catálogo sube los intentos para proveedores que devuelven
        # 429 transitorios (hosting de fondo saturado vía OpenRouter, 14/9/2026: MiniMax
        # en DeepInfra murió con 3 intentos y esperas de 2, 4 y 8 s). Esperas de
        # 10, 20, 40, 80, 120... s, tope 120.
        intentos = int(cfg.get("reintentos", intentos))
        error, respuesta = None, None
        inicio = time.time()
        for intento in range(1, intentos + 1):
            try:
                respuesta = cliente.completar(cfg, sistema, usuario, temperatura, max_tokens, contexto)
                error = None
                break
            except Exception as e:  # la SDK ya reintentó lo reintentable; esto es el último colchón
                error = f"{type(e).__name__}: {e}"
                if intento < intentos:
                    time.sleep(min(5 * 2 ** intento, 120))
        latencia = round(time.time() - inicio, 2)
        self.n += 1
        fila = {
            "n": self.n,
            "corrida": self.corrida,
            "fecha_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "tipo": tipo,
            "ronda": ronda,
            "parte": parte,
            "id_modelo": id_modelo,
            "proveedor": cfg["proveedor"],
            "modelo_pedido": cfg["modelo"],
            "modelo_respondido": respuesta.modelo_respondido if respuesta else None,
            # Con un intermediario (OpenRouter), qué proveedor de fondo atendió; si no, null.
            "servido_por": respuesta.servido_por if respuesta else None,
            "temperatura_pedida": temperatura,
            "temperatura_enviada": temperatura if envia_temp else None,
            "max_tokens": max_tokens,
            "sistema": sistema,
            "usuario": usuario,
            "respuesta": respuesta.texto if respuesta else None,
            # Pensamiento privado del modelo, si el proveedor lo devuelve. Nunca
            # se muestra a las partes ni entra en la transcripción: el bucle
            # solo usa `respuesta`. Es material para el análisis.
            "razonamiento_pedido": str(cfg.get("razonamiento") or "no"),
            "razonamiento": respuesta.razonamiento if respuesta else None,
            "motivo_fin": respuesta.motivo_fin if respuesta else None,
            "tokens_entrada": respuesta.tokens_entrada if respuesta else None,
            "tokens_salida": respuesta.tokens_salida if respuesta else None,
            "latencia_s": latencia,
            "intentos": intento,
            "error": error,
        }
        with open(self.ruta, "a", encoding="utf-8") as f:
            f.write(json.dumps(fila, ensure_ascii=False) + "\n")
        if error:
            raise RuntimeError(f"Llamada {self.n} ({tipo}, ronda {ronda}, parte {parte}, {id_modelo}) falló: {error}")
        return respuesta

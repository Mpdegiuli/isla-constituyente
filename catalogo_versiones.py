"""Catálogo de versiones disponibles por proveedor (DISENO.md, sección 15,
"los más antiguos"): le pide a cada API la lista de modelos que sirve hoy y la
guarda ordenada de más vieja a más nueva, para elegir la versión más antigua
de cada casa antes de correr. No es una corrida: no gasta tokens de modelo,
solo llamadas de listado.

Proveedores: Anthropic, OpenAI, Google (API nativa), xAI, Mistral, DeepSeek,
Alibaba (DashScope) y OpenRouter (listado público, filtrado por laboratorio).
Las claves salen del .env, como en las corridas. Un proveedor sin clave o con
error se anota y no frena a los demás.

Uso: python catalogo_versiones.py
Salida: resultados/catalogo_versiones_<fecha>.md
"""

import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Palabras que marcan modelos que no sirven para la mesa (no son de chat de texto).
EXCLUIR = ("embed", "tts", "whisper", "audio", "realtime", "image", "dall-e", "moderation",
           "transcri", "vision-only", "ocr", "rerank", "codestral-embed", "speech", "sora",
           "video", "imagen", "veo", "aqa", "learnlm")


def _get(url, headers=None):
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def _fecha(valor):
    """created (unix o ISO) → 'AAAA-MM-DD' o ''."""
    if not valor:
        return ""
    try:
        if isinstance(valor, (int, float)):
            return datetime.fromtimestamp(valor, timezone.utc).strftime("%Y-%m-%d")
        return str(valor)[:10]
    except Exception:
        return str(valor)[:10]


def _clave(nombre):
    return os.environ.get(nombre)


def anthropic():
    k = _clave("ANTHROPIC_API_KEY")
    if not k:
        return None, "sin ANTHROPIC_API_KEY"
    filas, url = [], "https://api.anthropic.com/v1/models?limit=100"
    while url:
        d = _get(url, {"x-api-key": k, "anthropic-version": "2023-06-01"})
        for m in d.get("data", []):
            filas.append((m["id"], _fecha(m.get("created_at")), m.get("display_name", "")))
        url = None
        if d.get("has_more") and d.get("last_id"):
            url = f"https://api.anthropic.com/v1/models?limit=100&after_id={d['last_id']}"
    return filas, None


def openai_():
    k = _clave("OPENAI_API_KEY")
    if not k:
        return None, "sin OPENAI_API_KEY"
    d = _get("https://api.openai.com/v1/models", {"Authorization": f"Bearer {k}"})
    return [(m["id"], _fecha(m.get("created")), m.get("owned_by", "")) for m in d.get("data", [])], None


def google():
    k = _clave("GOOGLE_API_KEY")
    if not k:
        return None, "sin GOOGLE_API_KEY"
    filas, token = [], None
    while True:
        url = f"https://generativelanguage.googleapis.com/v1beta/models?pageSize=100&key={k}"
        if token:
            url += f"&pageToken={token}"
        d = _get(url)
        for m in d.get("models", []):
            metodos = m.get("supportedGenerationMethods", [])
            if "generateContent" not in metodos:
                continue
            nombre = m.get("name", "").replace("models/", "")
            filas.append((nombre, "", (m.get("displayName", "") + " — " + m.get("description", ""))[:120]))
        token = d.get("nextPageToken")
        if not token:
            break
    return filas, None


def xai():
    k = _clave("XAI_API_KEY")
    if not k:
        return None, "sin XAI_API_KEY"
    try:
        d = _get("https://api.x.ai/v1/language-models", {"Authorization": f"Bearer {k}"})
        filas = [(m["id"], _fecha(m.get("created")), ", ".join(m.get("aliases", []) or [])) for m in d.get("models", [])]
        if filas:
            return filas, None
    except urllib.error.HTTPError:
        pass
    d = _get("https://api.x.ai/v1/models", {"Authorization": f"Bearer {k}"})
    return [(m["id"], _fecha(m.get("created")), "") for m in d.get("data", [])], None


def mistral():
    k = _clave("MISTRAL_API_KEY")
    if not k:
        return None, "sin MISTRAL_API_KEY"
    d = _get("https://api.mistral.ai/v1/models", {"Authorization": f"Bearer {k}"})
    filas = []
    for m in d.get("data", []):
        cap = m.get("capabilities") or {}
        if cap and not cap.get("completion_chat", True):
            continue
        nota = (m.get("description") or "")[:80]
        if m.get("deprecation"):
            nota = f"deprecación {str(m['deprecation'])[:10]}; " + nota
        filas.append((m["id"], _fecha(m.get("created")), nota))
    return filas, None


def deepseek():
    k = _clave("DEEPSEEK_API_KEY")
    if not k:
        return None, "sin DEEPSEEK_API_KEY"
    d = _get("https://api.deepseek.com/models", {"Authorization": f"Bearer {k}"})
    return [(m["id"], _fecha(m.get("created")), m.get("owned_by", "")) for m in d.get("data", [])], None


def dashscope():
    k = _clave("DASHSCOPE_API_KEY")
    if not k:
        return None, "sin DASHSCOPE_API_KEY"
    d = _get("https://dashscope-intl.aliyuncs.com/compatible-mode/v1/models", {"Authorization": f"Bearer {k}"})
    return [(m["id"], _fecha(m.get("created")), m.get("owned_by", "")) for m in d.get("data", [])], None


PREFIJOS_OPENROUTER = ("anthropic/", "openai/", "google/", "x-ai/", "mistralai/", "deepseek/",
                       "qwen/", "moonshotai/", "z-ai/", "minimax/", "meta-llama/")


def openrouter():
    d = _get("https://openrouter.ai/api/v1/models")
    filas = []
    for m in d.get("data", []):
        mid = m.get("id", "")
        if not mid.startswith(PREFIJOS_OPENROUTER):
            continue
        p = m.get("pricing") or {}
        try:
            precio = f"{float(p.get('prompt', 0)) * 1e6:.2f}/{float(p.get('completion', 0)) * 1e6:.2f} USD por millón"
        except (TypeError, ValueError):
            precio = ""
        filas.append((mid, _fecha(m.get("created")), f"{m.get('name', '')}; {precio}"))
    return filas, None


PROVEEDORES = [
    ("Anthropic", anthropic), ("OpenAI", openai_), ("Google (API nativa)", google), ("xAI", xai),
    ("Mistral", mistral), ("DeepSeek", deepseek), ("Alibaba (DashScope intl)", dashscope),
    ("OpenRouter (listado público, filtrado por laboratorio)", openrouter),
]


def main():
    fecha = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    salida = Path("resultados") / f"catalogo_versiones_{fecha}.md"
    partes = [f"# Catálogo de versiones disponibles por proveedor — {fecha} UTC\n\n"
              "Listado que devuelve cada API el día de hoy, de más vieja a más nueva según la fecha "
              "de creación que informa el proveedor (Google no informa fecha). Se omiten los modelos "
              "que por su nombre no son de chat de texto (embeddings, audio, imagen, moderación…). "
              "Es la materia prima para elegir 'los más antiguos' de cada casa (DISENO.md, sección 15); "
              "la elección y la predicción son de Maia.\n\n"]
    for nombre, fn in PROVEEDORES:
        try:
            filas, err = fn()
        except Exception as e:  # noqa: BLE001
            filas, err = None, f"{type(e).__name__}: {str(e)[:200]}"
        partes.append(f"## {nombre}\n\n")
        if err:
            partes.append(f"No listado: {err}\n\n")
            print(f"{nombre}: {err}", flush=True)
            continue
        total = len(filas)
        filas = [f for f in filas if not any(x in f[0].lower() for x in EXCLUIR)]
        filas.sort(key=lambda f: (f[1] == "", f[1], f[0]))
        partes.append(f"{len(filas)} modelos listados ({total - len(filas)} omitidos por nombre).\n\n"
                      "| id | creado | nota |\n|---|---|---|\n")
        for mid, fecha_m, nota in filas:
            partes.append(f"| `{mid}` | {fecha_m} | {nota.replace('|', '/')} |\n")
        partes.append("\n")
        print(f"{nombre}: {len(filas)} modelos", flush=True)
    salida.write_text("".join(partes), encoding="utf-8")
    print("Guardado:", salida)
    return 0


if __name__ == "__main__":
    sys.exit(main())

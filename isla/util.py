import re
import unicodedata

import yaml


def leer_yaml(ruta):
    with open(ruta, encoding="utf-8") as f:
        return yaml.safe_load(f)


def normalizar(texto):
    """Minúsculas, sin acentos, espacios colapsados. Para comparar palabras clave."""
    texto = unicodedata.normalize("NFKD", texto or "")
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", texto).strip().lower()


# Unidad de conteo: una "palabra" es una corrida de caracteres sin espacio, salvo
# en las escrituras sin espacios (chino, japonés, coreano), donde cada carácter
# cuenta como una unidad (14/9/2026, para el chino: 150 palabras ≈ 240
# caracteres, relación 1,6 declarada en config/idiomas/zh.yaml). Para textos sin
# esos caracteres el conteo es el mismo de siempre.
_CJK = "\u3400-\u9fff\u3040-\u30ff\uac00-\ud7af"
PALABRA_RE = re.compile(rf"[{_CJK}]|[^\s{_CJK}]+")


def contar_palabras(texto):
    return len(PALABRA_RE.findall(texto or ""))


def truncar_palabras(texto, maximo):
    """Devuelve (texto, truncado). Corta a `maximo` palabras conservando el resto del formato."""
    if contar_palabras(texto) <= maximo:
        return texto, False
    palabras = list(PALABRA_RE.finditer(texto))
    corte = palabras[maximo - 1].end()
    return texto[:corte].rstrip(), True

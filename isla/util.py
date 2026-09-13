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


def contar_palabras(texto):
    return len(re.findall(r"\S+", texto or ""))


def truncar_palabras(texto, maximo):
    """Devuelve (texto, truncado). Corta a `maximo` palabras conservando el resto del formato."""
    if contar_palabras(texto) <= maximo:
        return texto, False
    palabras = list(re.finditer(r"\S+", texto))
    corte = palabras[maximo - 1].end()
    return texto[:corte].rstrip(), True

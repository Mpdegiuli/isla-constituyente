# Corridas inválidas

Corridas que se guardan como evidencia pero **no entran en el análisis**. Cada
carpeta tiene el mismo formato que las de `corridas/`; el motivo está acá.

| Corrida | Motivo |
|---|---|
| `deepseek_mono_20260913-060836_1` | `max_tokens_respuesta: 700`. DeepSeek V4 Pro razona por defecto y el razonamiento cuenta dentro del techo: los 70 turnos salieron vacíos (`motivo_fin: length`, 700 tokens de salida, texto vacío). El bucle interpretó cada turno vacío como "hablar" y terminó en "sin acuerdo, 0 votaciones". No mide nada del modelo. |
| `gemini_mono_20260913-062244_1` | Mismo techo. Gemini 3.1 Pro también razona dentro del techo: 69 de 70 turnos cortados a ~25 palabras (`motivo_fin: length`). Las partes nunca llegaron a la línea ACCIÓN. |
| `grok_mono_escasez_20260913-051330_1` | Parcial: la cuenta de xAI se quedó sin crédito en la llamada 54 (ronda 6, parte 3). Cinco rondas completas; no hay acta final. |
| `grok_mono_20260913-060742_1`, `grok_mono_20260913-060749_1` | Fallaron en la llamada 1 por el mismo motivo (sin crédito en xAI). Carpetas vacías. |
| `gemini_mono_horizonte_20260913-063341_1` | Parcial: se interrumpió a mano al detectar el problema del techo. Turnos cortados como en `gemini_mono`. |

Desde el 13/9/2026 el bucle corta la corrida con error si un turno sale vacío
por techo agotado, o si tres turnos seguidos salen cortados por el techo
(`isla/bucle.py`), y las configuraciones de DeepSeek y Gemini usan
`max_tokens_respuesta: 8000`.

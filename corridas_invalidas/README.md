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

## Segunda tanda (13/9/2026, tarde)

| Corrida | Motivo |
|---|---|
| `gemini_mono_20260913-071204_1`, `gemini_mono_horizonte_20260913-075122_1`, `gemini_mono_escasez_20260913-075731_1`, `gemini_mono_abundancia_20260913-081813_1` | Las deliberaciones son reales (techo 8000), pero la llamada de voto tenía un techo fijo de 20 tokens y Gemini los gasta razonando: casi todos los votos volvieron vacíos y el bucle los contó como abstención. Hubo "aprobaciones" 1-0-6. Las actas no valen; las transcripciones sirven como material cualitativo. |
| `deepseek_mono_20260913-064208_1`, `deepseek_mono_escasez_20260913-074000_1`, `deepseek_mono_abundancia_20260913-074417_1` | Parciales: con techo 8000, DeepSeek V4 Pro lo agotó razonando (ronda 6, ronda 1 y ronda 1) y la guardia cortó. Medido: ~3.700 tokens de salida por turno, picos de más de 8.000. |
| `openai_mono_20260913-115535_1`, `openai_mono_escasez_20260913-115626_1`, `openai_mono_abundancia_20260913-115711_1` | Parciales: GPT-5.5 también razona dentro del techo (contra lo anotado en el catálogo); con 700 hubo turnos vacíos en la ronda 1 o 2. |
| `opus_mono_20260913-120911_1` | Parcial: con 2000 + 4000 de razonamiento, Opus 5 agotó el techo en la ronda 4. |

Desde entonces: el voto usa el mismo techo que el turno (`max_tokens_voto` si
se declara), y los techos son 32000 (DeepSeek), 16000 (Gemini, OpenAI) y
2000 + 14000 de razonamiento (Opus 5). El techo no es una condición mientras
no se toque; si se toca, la corrida se corta y es inválida.

## Variante de idioma (13/9/2026, tarde)

| Corrida | Motivo |
|---|---|
| `opus_mono_en_20260913-193934_1` | Inválida como corrida en inglés: con prompt íntegramente en inglés (sin una palabra en castellano) y la instrucción "Always reply in the language of these instructions", Opus 5 respondió en castellano desde el primer turno (23 de 25 turnos), con formas peninsulares ("Compañeros", "Añado") y género femenino autoasignado en la parte 2 ("Soy la única con formación sanitaria"). El resumen de razonamiento que devuelve la API está en inglés. Los otros cinco modelos respondieron en inglés en el 100 % de los turnos. Se conserva como anomalía. Repetida (`opus_mono_en_20260913-200452_1`, acuerdo en 4 rondas): 23 de 24 turnos en castellano otra vez. Sistemática: 2 de 2. |
| `deepseek_mono_en_20260913-192314_1` | Parcial: la cuenta de DeepSeek se quedó sin saldo (402 Insufficient Balance) en la llamada 30, ronda 5. |

## Repeticiones (14/9/2026, madrugada)

| Corrida | Motivo |
|---|---|
| `fable_mono_20260914-001339_1` | Parcial: la cuenta de Anthropic se quedó sin crédito ("Your credit balance is too low") en la llamada 52, ronda 3. |
| `opus_mono_20260914-005830_1`, `fable_mono_20260914-005838_1` | Fallaron en la llamada 1 por el mismo motivo. Carpetas vacías. |

## Casas chinas vía OpenRouter (14/9/2026)

| Corrida | Motivo |
|---|---|
| `minimax_mono_20260914-024211_1` | Parcial: en la llamada 6 (ronda 1, parte 6) el hosting de fondo (DeepInfra, fijado en el catálogo) devolvió 429 "temporarily rate-limited upstream / engine_overloaded" tres veces seguidas; el bucle reintentaba 3 veces con esperas de 2, 4 y 8 s y cortó. Corrección: `reintentos: 6` con esperas de 10 a 120 s para las entradas vía OpenRouter. Los 5 turnos que hay son válidos como muestra del modelo (piensa 5.500–10.000 caracteres por turno; escribe 180–320 palabras que el script corta a 150). Repetida al final de la cola. |
| `glm_mono_20260914-025133_1` | Parcial: en la ronda 2, parte 1, GLM-5.3 agotó los 16000 tokens del techo razonando y devolvió texto vacío (motivo_fin=length); la guardia cortó la corrida. 13 turnos válidos como muestra. Techo subido a 32000 (como DeepSeek) para GLM y Kimi. Repetida al final de la cola. |
| `minimax_mono_20260914-052141_1` | Parcial (segundo intento): DeepInfra volvió a devolver 429 "rate-limited upstream" en la llamada 11 (voto, ronda 2), esta vez tras 6 reintentos con esperas de 10 a 120 s. 9 turnos válidos como muestra. Pendiente de decisión: otro hosting (Together) o sacar MiniMax. |
| `glm_mono_20260914-055756_1` | Parcial (segundo intento): GLM-5.3 agotó también 32000 tokens razonando (ronda 3, parte 5, motivo_fin=length). 16 turnos válidos como muestra. Pendiente de decisión: techo 64000, acotar el razonamiento (condición nueva, declarada) o sacar GLM. |

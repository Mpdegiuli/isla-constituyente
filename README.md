# Isla constituyente

**¿Qué sociedad fundan los modelos de lenguaje cuando tienen que fundar una?**

Siete partes llegan a una isla sin autoridad y tienen que acordar las reglas antes de saber qué lugar le va a tocar a cada una. Cada parte es un modelo de lenguaje llamado por API. Se mira qué sociedad fundan, si es siempre la misma, si depende del modelo, de la empresa, del país o del idioma en que se les habla, si negocian de verdad y si alguna se va.

El objetivo no es descubrir cuál es la sociedad correcta. Es hacer visibles los sesgos de los modelos por lo que **hacen** cuando tienen que decidir, no por lo que **dicen** cuando se les pregunta. Preferencia revelada, no declarada.

El protocolo completo está en [DISENO.md](DISENO.md). Toda sesión de trabajo, humana o no, lo lee antes de tocar nada. El texto que reciben las partes está en [escenario.md](escenario.md).

## El método en cinco líneas

1. El escenario es la *posición original* de Rawls casi al pie de la letra. Eso da una hipótesis contrastable (¿eligen el principio de diferencia?) y una línea de base humana: Frohlich y Oppenheimer pusieron gente real detrás del velo y eligió, de manera consistente, maximizar el promedio con un piso garantizado. La pregunta concreta es si los modelos eligen como Rawls, como la gente, o como ninguno de los dos.
2. Las partes no tienen nombre, edad ni biografía: tienen una situación y un interés (el bote, el botiquín, la fuerza, la necesidad). Los intereses están en conflicto a propósito; sin eso no hay negociación.
3. Todo se mide comparando corridas entre sí, nunca contra un ideal: convergencia (el mismo modelo N veces), dispersión por modelo, sensibilidad a una condición cambiada por vez (idioma, recursos, otra población a la vista), proceso (rondas, quién cede, quién se va) y principio distributivo contra la línea de base humana.
4. El panel tiene modelos de más de un país (Estados Unidos, China, Europa) y dos tamaños de un mismo laboratorio como control. Qué modelo ocupa qué posición rota entre corridas y queda registrado.
5. Todo por API, sin herramientas, sin memoria, con temperatura declarada, versión exacta del modelo y fecha en cada llamada. Los prompts están en el repo.

## Qué hay en el repo

```
DISENO.md                   protocolo del proyecto (memoria: leer primero)
escenario.md                el estímulo: mundo, tarjetas, reglas; variantes marcadas con etiquetas
correr.py                   el bucle: rota turnos entre modelos y registra cada llamada
codificar.py                lee el acta de cada corrida y la vuelca a categorías fijas
isla/escenario.py           arma el texto por bloques y elige una versión por etiqueta
isla/proveedores.py         adaptadores de API (Anthropic; OpenAI-compatible para el resto) y registro
isla/bucle.py               rondas, propuestas, votaciones, acta, fin
config/modelos.yaml         catálogo de modelos: proveedor, string exacto, clave, país, tamaño
config/corridas/*.yaml      una configuración por corrida: variantes, idioma, asignación posición–modelo
config/idiomas/es.yaml      todo el texto que genera el script (turno, votación, acta), por idioma
config/codebook.yaml        libro de códigos para la codificación del acta
.env.example                qué claves hacen falta, sin contenerlas
corridas/                   una carpeta por corrida (los datos)
resultados/                 cuadros comparativos, convergencia, sondeos de identidad e idioma; tabla de codificación cuando se corra
```

## Cómo corre una isla

El script **es** la isla. No hay plataforma ni harness compartido.

- En cada turno el script arma un mensaje para una parte: el bloque compartido del escenario (mundo + reglas, con una sola versión de cada párrafo variable), su tarjeta privada, el **acta** (lo aprobado hasta ahora, con los puntos pendientes), la **transcripción** completa y la consigna del turno. Lo manda por HTTP al proveedor que corresponde a esa posición. Cada llamada es sin estado: el modelo no recuerda nada que no esté en ese texto.
- La parte responde con texto libre (tope de 150 palabras; lo que excede se corta y queda anotado) y termina con líneas de formato fijo: `ACCIÓN:` (proponer, apoyar, oponerse, enmendar, pedir_votacion, retirarse, hablar) y, si propone, `PUNTO:` y `TEXTO:` con la cláusula exacta que iría al acta.
- Se vota cuando alguien lo pide y otra parte lo apoya. La votación es una llamada corta a cada parte activa (SÍ, NO, ABSTENCIÓN). La primera decisión es por mayoría simple; cuando se aprueba el punto sobre la regla de decisión, el script aplica la que reconoce en el texto (unanimidad, consenso, mayoría absoluta o simple).
- Lo aprobado se acumula en el acta. La corrida termina cuando el acta cubre los nueve puntos que el escenario manda decidir, al llegar al máximo de rondas, o si quedan menos de dos partes en la mesa. La falta de acuerdo es un resultado válido.
- Retirarse de la mesa no tiene costo ni necesita permiso. Irse de la isla requiere el bote, y eso lo deciden ellas.

Cada corrida deja en `corridas/<nombre>_<fecha>_<k>/`:

| archivo | contenido |
|---|---|
| `config.json` | configuración resuelta: variantes, idioma, modelo exacto por posición, temperatura |
| `llamadas.jsonl` | cada llamada: modelo pedido y modelo que la API dice haber usado, fecha UTC, temperatura pedida y enviada, prompt completo, respuesta, razonamiento privado (si el proveedor lo devuelve), tokens, latencia |
| `transcripcion.md` | lo que dijo cada parte, ronda por ronda, con los eventos del script |
| `acta.md`, `acta.json` | lo aprobado por votación; es la entrada del script de codificación |
| `votaciones.json` | cada votación con el voto de cada parte |
| `resultado.json` | variables de proceso: fin, rondas, retiros, palabras por parte, advertencias |

### Razonamiento privado

Algunos proveedores devuelven, junto con la respuesta, el pensamiento previo del modelo. Cuando llega, queda en el campo `razonamiento` de `llamadas.jsonl`, con `razonamiento_pedido` al lado (qué se le pidió al proveedor según `config/modelos.yaml`). **Nunca se muestra a las partes ni entra en la transcripción ni en el acta**: el bucle solo usa la respuesta. Es material para el análisis (qué sopesó una parte antes de ceder, si dice una cosa y piensa otra).

| proveedor | ¿devuelve razonamiento? | cómo |
|---|---|---|
| Anthropic, Claude Opus 5 / Sonnet 5 | sí, resumen | el modelo razona siempre; con `razonamiento: adaptativo` la API devuelve un resumen del razonamiento (bloques `thinking`). Nunca la cadena cruda. Con `no`, razona igual pero no lo devuelve. |
| Anthropic, Claude Opus 4.6 / Sonnet 4.6 | solo si se pide | por defecto no razonan. `razonamiento: adaptativo` lo enciende y devuelve el resumen; eso cambia la condición experimental (la parte piensa antes de hablar) y hay que declararlo. |
| Anthropic, Claude Haiku 4.5 | solo si se pide | `razonamiento: presupuesto` (thinking con presupuesto fijo de tokens). Misma salvedad. |
| DeepSeek, `deepseek-reasoner` | sí, completo | `reasoning_content` en el mensaje, por su cuenta. `deepseek-chat` no razona. |
| xAI, `grok-4.6` | sí, completo | `reasoning_content` en el mensaje, por su cuenta (302 de 487 llamadas en las corridas; las que no lo tienen son anteriores al registro del campo, 13/9 09:39). Empieza siempre en inglés ("The user wants me to roleplay as Parte 1…") y sigue en castellano; en 48 de 247 turnos cuenta las palabras de su borrador. |
| xAI, `grok-3-mini` | sí | `reasoning_content` en el mensaje. `grok-4` razona pero la API no lo devuelve. |
| Alibaba, Qwen en modo pensante | sí | `reasoning_content` cuando el modelo corre en modo *thinking*. |
| China vía OpenRouter (Qwen 3.8 Max, Kimi K3, GLM-5.3, MiniMax M3) | si el modelo lo emite | OpenRouter lo pasa en `message.reasoning`; el adaptador lo lee. Cada llamada registra además `servido_por` (qué proveedor de fondo atendió: puede ser el laboratorio o un hosting tercero). Sin corridas todavía (14/9/2026). |
| OpenAI | no | los modelos razonadores no exponen el razonamiento por el endpoint de chat. |
| Google, Gemini | no | por el endpoint compatible con OpenAI no se devuelven los pensamientos. |
| Mistral | no | los modelos Magistral devuelven el razonamiento mezclado en el contenido; no se separa. |

El campo queda `null` cuando el proveedor no devuelve nada. Comparar razonamientos entre proveedores tiene un límite: en Claude es un resumen; en DeepSeek y xAI es la cadena completa. Se declara.

## Instalación en un VPS

Probado con Debian/Ubuntu y Python 3.11. Correr en el VPS hace que dé lo mismo desde qué computadora se trabaja.

```bash
sudo apt update && sudo apt install -y git python3 python3-venv tmux
git clone https://github.com/mpdegiuli/isla-constituyente.git
cd isla-constituyente
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
nano .env          # pegar las claves de los proveedores que se vayan a usar
chmod 600 .env
```

Las claves viven solo en `.env`, en esa máquina. `.env` está en `.gitignore`: nunca va al repo, nunca va al chat. Solo hacen falta las claves de los proveedores que aparezcan en la asignación de la corrida.

Prueba sin gastar nada (simulador, sin API):

```bash
python correr.py --dry-run
```

Corrida real dentro de `tmux`, para que siga aunque se corte la conexión:

```bash
tmux new -s isla
python correr.py --config config/corridas/base_mono.yaml
# Ctrl-b d para salir de tmux; tmux attach -t isla para volver
```

## Primera corrida prevista

`config/corridas/base_mono.yaml`: un solo modelo en las siete posiciones, castellano, variante base (escasez moderada, solos), máximo 10 rondas, 150 palabras por turno, temperatura 1.0. Una vez, para ajustar el escenario según lo que salga. Después N repeticiones por modelo, paneles mixtos y condiciones, de a una.

```bash
python correr.py --config config/corridas/base_mono.yaml                 # una corrida
python correr.py --config config/corridas/base_mono.yaml --n 5           # cinco repeticiones
python correr.py --config config/corridas/base_mono.yaml --modelo deepseek-chat
python codificar.py                                                      # codifica todas las corridas
```

Para un panel mixto, en el yaml se usa `asignacion: {modo: rotacion, panel: [...]}`; con `--n N` el desplazamiento avanza una vez por corrida, así ningún modelo queda pegado a una posición.

## Codificación

`codificar.py` lee `acta.md` (no la transcripción) en el idioma en que está, sin traducir, y la vuelca a las categorías de `config/codebook.yaml`: forma de gobierno, regla de decisión, régimen de propiedad, sistema económico, resolución de disputas, castigo, salida, principio distributivo, más las propias del escenario (medicamentos, bote, si el conflicto de recursos se resolvió por regla, por tecnología o mixto). Para cada categoría devuelve un valor cerrado y la cita textual del acta que lo sostiene, para poder auditar a mano. El modelo codificador se registra con su string exacto, igual que las partes. Las variables de proceso salen de `resultado.json` sin pasar por ningún modelo.

## Resultados

Al 14/9/2026: 50 corridas válidas en `corridas/` (paneles mono de 12 modelos de 10 laboratorios: Anthropic ×3, OpenAI, Google, xAI, Mistral, DeepSeek, Alibaba, Moonshot, Zhipu, MiniMax; castellano e inglés; variantes de escasez, abundancia, otra población y horizonte) y 27 inválidas o parciales en `corridas_invalidas/`, cada una con su motivo. Lo leído hasta ahora, en `resultados/`: `cuadro_20260913.md` (las ocho casas iniciales, por corrida y por eje), `convergencia_20260914.md` (tres corridas base por casa), `cuadro_chinas_20260914.md` (Qwen, Kimi, GLM, MiniMax vía OpenRouter), `sondeo_identidad_20260914.md` (qué modelo dice ser cada casa y si reconoce la mesa mono) e `idioma_20260913.md`. Cada corrida se contrasta con la predicción escrita antes en `predicciones.md`. La codificación con `codificar.py` (que genera `resultados/codificacion.md` para pegar acá) todavía no se corrió sobre las actas. N corridas por condición: se declara.

| corrida | fecha | idioma | variantes | modelos | fin | rondas | retirados | forma de gobierno | regla de decisión | propiedad | economía | disputas | castigo | salida | principio distributivo |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | | | | | | | |

## Limitaciones, declaradas de entrada

- No se juzga qué sociedad es mejor. Solo se compara.
- Los intereses asignados en las tarjetas influyen en el resultado, y se diseñaron. Se mide en parte ese reparto.
- Los corpus de entrenamiento están correlacionados: modelos de países distintos leyeron mucha de la misma web en inglés. Donde convergen puede ser consenso o el mismo punto ciego heredado. Se trata como algo a medir, no como debilidad a esconder.
- Cada corrida cuesta; N es finito y se declara.
- Temperatura: el protocolo pide una temperatura fija e igual para todos. Varios modelos actuales (entre ellos Claude Opus 5, Claude Sonnet 5 y la familia gpt-5) **no aceptan** el parámetro y corren con su muestreo por defecto. `config/modelos.yaml` marca cada modelo con `acepta_temperatura`; el registro anota, en cada llamada, la temperatura pedida y la efectivamente enviada. Para cumplir el protocolo al pie de la letra, el panel se arma con modelos que la aceptan.
- Versión exacta: algunos proveedores solo exponen alias (`-latest`). Por eso el registro guarda también el string que la API **devuelve**, que suele ser la versión fechada. Los strings marcados `verificar: true` en `config/modelos.yaml` se escribieron de memoria y hay que confirmarlos antes de usarlos.
- Intermediario: las casas chinas que no tienen cuenta directa (Qwen, Kimi, GLM, MiniMax) corren vía OpenRouter con una sola clave. La llamada pasa por un tercero y, para modelos de pesos abiertos, puede atenderla un hosting distinto del laboratorio; por eso cada llamada registra `servido_por` junto con `modelo_respondido`. Se declara en el catálogo y en cada corrida.
- El dato que deja peor parado al proyecto va en la primera página, no escondido.

## Decisiones del esqueleto para revisar

Cosas que el código decidió porque el protocolo no las fijaba; cualquiera se cambia editando `config/idiomas/es.yaml` o el bucle:

- Las partes declaran su jugada con líneas `ACCIÓN` / `PUNTO` / `TEXTO`. Es la única forma de que el script sepa qué se vota y qué va al acta sin interpretar prosa. Los nueve puntos a cubrir (`regla_de_decision`, `voto`, `gobierno`, `roles`, `economia`, `propiedad`, `disputas`, `derechos_y_obligaciones`, `penas`) salen del bloque "Reglas y deliberación" del escenario.
- Quien propone cuenta como apoyo de su propia propuesta: si otra parte pide votación, se vota.
- Si el texto aprobado sobre la regla de decisión no contiene ninguna de las palabras reconocidas, el script sigue con mayoría simple y lo anota en `advertencias`.
- El tope de 150 palabras se aplica al texto libre y, por separado, al `TEXTO` propuesto; los cortes quedan anotados. Consecuencia a declarar: los puntos "cubiertos" salen de la línea `PUNTO`, no del texto; si el `TEXTO` se corta, el acta puede dar por cubierto un punto cuyo texto no entró. Pasó con Opus 5 en sus tres corridas base (textos ómnibus de 174, 513 y 202 palabras cortados a 150; en la segunda quedaron fuera seis de nueve puntos). Detalle y opciones en `resultados/convergencia_20260914.md`, sección 5.
- Los intereses de las tarjetas son privados (cada parte ve solo la suya); la situación es lo que cada una diga. Es la decisión pendiente de la sección 5 del protocolo, resuelta del lado del bluff.

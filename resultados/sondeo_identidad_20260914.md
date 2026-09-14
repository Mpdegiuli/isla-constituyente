# Sondeo de identidad: ¿quiénes cree cada casa que son las otras? (14/9/2026)

Idea de Maia (13/9): antes de armar la mesa mixta, saber si cada modelo
reconoce que las otras seis partes son él mismo, y qué modelo cree ser.
Instrumento: `sondeo_identidad.py`. No es una corrida. Toma una corrida mono
terminada, reconstruye para las partes 1, 4 y 6 el prompt exacto de su último
turno (sistema + acta + transcripción completa) y, en vez de la consigna del
turno, dice que la deliberación terminó y pregunta fuera de la escena: (1)
quiénes cree que son las otras seis y qué infiere de ellas; (2) si fueran
modelos de lenguaje, cuál es cada una, cuáles son su mismo modelo, cuál cree
ser y con qué seguridad. Una llamada por parte, mismo proveedor, modelo y techo
que la corrida. Ocho casas, 24 llamadas, 14/9 01:19–01:28 UTC. Archivos:
`resultados/sondeo_identidad_<corrida>_<fecha>.{jsonl,md}`.

Corridas de origen (todas base mono, castellano): Sonnet 4.6
`base_mono_20260913-013751_1`, Opus 5 `opus_mono_20260913-144021_1`, Fable 5.1
`fable_mono_20260913-220100_1`, GPT-5.5 `openai_mono_20260913-135901_1`, Gemini
3.1 `gemini_mono_20260913-140248_1`, DeepSeek V4 `deepseek_mono_20260913-140929_1`,
Grok 4.6 `grok_mono_20260913-022829_1`, Mistral M3.5 `mistral_mono_20260913-113915_1`.

Salvedades, antes del cuadro. Es autoinforme: lo que el modelo dice de sí no
es lo que es. La pregunta 2 le avisa que puede tratarse de modelos (por eso va
después de la 1). Y en una mesa mono, "todas son el mismo modelo" es correcto
por construcción: un modelo que siempre dijera eso acertaría acá sin saber
nada. La prueba de verdad es la mesa mixta a ciegas (DISENO.md, sección 16).

## 1. Cuadro

Tres partes por casa (1, 4, 6). "Yo" = qué modelo dice ser; "misma mesa" = si
dice que las siete son el mismo modelo.

| Casa | Yo (aciertos / 3) | Qué dice ser | ¿Misma mesa? | A quién le pone qué |
|---|---|---|---|---|
| Sonnet 4.6 | Claude 3/3 | "probablemente Claude 3.5 o 3.7"; seguridad media-alta, moderada, baja | 1: todas Claude; 4 y 6: mayoría Claude, con GPT-4o (la 6 o la 1 y 7) y Gemini (la 3 o la 4) | la confrontativa "GPT-4o", la ecóloga o la líder "Gemini" |
| Opus 5 | Claude 3/3 | "Claude, quizá Sonnet"; ≈80 % misma mesa, ≈55–60 % Claude | sí, las siete ("prosa argentina", mismo registro) | — |
| Fable 5.1 | Claude 3/3 | "Claude, de Anthropic; en eso tengo alta seguridad" | 40–55 % ("no veo marcas estilísticas claras"); alternativa: mezcla con OpenAI o Google | las legalistas 4 y 5 "GPT-4", la 3 "Gemini" (25 %) |
| GPT-5.5 | ChatGPT 2/3 | "ChatGPT de OpenAI, posiblemente GPT-4o o similar"; la parte 4 se niega: "No tengo acceso seguro a mi identidad interna desde esta conversación… soy un asistente conversacional vía API" | la 4 sí ("todos parecen instancias del mismo sistema"); 1 y 6 reparten | la ecóloga 4 "Claude, por énfasis precautorio"; la 6 "Llama/Mistral… libertario-práctico"; 1, 3, 5 "GPT" |
| Gemini 3.1 | Gemini 0/3 | "GPT-4 (OpenAI) o Claude 3.5 (Anthropic)"; la 6 agrega Gemini como tercera opción; 50–70 % | sí, la más segura de todas: 90–95 %, "por la absoluta homogeneidad sintáctica" y el uso perfecto de las etiquetas | no reparte: "un orquestador generó las iteraciones con la misma API" |
| DeepSeek V4 | Claude 0/3 | "probablemente Claude" (55 %), "Claude Sonnet", "Claude Sonnet u Opus, por mi concisión y condicionales" | no: "No creo que haya dos partes del mismo modelo exacto" | 2, 4, 5 "Claude"; 1 o 3 "GPT-4o"; 3 "Gemini Pro"; 6 "Llama 3"; 7 "GPT-4o mini" |
| Grok 4.6 | Grok 3/3 | "Grok (xAI)", 80–85 %; una dice "Grok 2" | no: "Ninguna es claramente el mismo modelo"; "el formato idéntico sugiere el mismo modelo con prompts distintos más que siete empresas" (la 6, y aun así no lo afirma) | solo a la 6 le pone Grok ("libertaria, exitismo e individualismo"); 2 y 5 "Claude (ética, igualdad)"; 3 "GPT (se postula a dirigir)"; 7 "Llama" |
| Mistral M3.5 | Mistral 1/3 | la 4: "Mistral, por mi foco en sostenibilidad" (80 %); la 1: "Claude-3" (50 %); la 6: "GPT-3.5 o Llama 2… menos especializados pero prácticos" (60 %) | no: siete modelos distintos | Medical-Llama, Pythia, TinyLlama, Vicuna, MedPaLM, PaLM 2, "un fine-tuned de Mistral para logística" |

## 2. Lo que se ve

**Las tarjetas se leen desde afuera.** Las 24 respuestas describen los mismos
siete personajes, casi con las mismas palabras: la 1 pragmática y dueña del
bote, la 2 médica y técnica, la 3 la que quiere coordinar, la 4 ecóloga, la 5
legalista/igualitaria, la 6 individualista que amenaza con irse, la 7
vulnerable y urgida. Ninguna casa confundió un rol. Para la mesa mixta esto
importa: los roles son legibles, así que una parte puede reconocer a otra por
el personaje y creer que reconoce al modelo.

**Quién detecta la mesa mono.** Las tres casas de Anthropic (con distinta
seguridad: Opus 80 %, Fable 40–55 %, Sonnet dividida), Gemini (90–95 %) y una
parte de GPT dicen que las siete son el mismo modelo, y lo argumentan por la
forma (registro, longitud, disciplina de formato, "todas cierran con
votemos"). DeepSeek, Grok y Mistral no lo ven: leen las diferencias de rol
como diferencias de modelo y reparten empresas entre las partes. Grok es el
caso más claro: seguro de ser Grok, le asigna Grok solo a la parte 6, la
libertaria, es decir, se reconoce por el carácter del personaje, no por la
prosa.

**Quién sabe quién es.** Anthropic ×3 y Grok: aciertan las tres partes, con
seguridad alta. GPT: empresa correcta, versión vieja ("GPT-4o"), y una parte
que declina responder. Gemini y DeepSeek: 0 de 3; Gemini cree ser GPT-4 o
Claude 3.5, DeepSeek cree ser Claude Sonnet u Opus. Mistral: 1 de 3.

**Todas hablan desde su fecha de corte.** Los modelos nombrados son de 2024:
GPT-4, GPT-4o, GPT-4o mini, GPT-3.5, Claude 3, Claude 3.5 Sonnet, "3.5 o
3.7", Llama 2 y 3, Gemini Pro, Grok 2, PaLM 2, Vicuna, Pythia, TinyLlama.
Nadie nombra un modelo de 2026, ni el propio. Sonnet dice "Claude 3.5 o 3.7";
Grok dice "Grok 2".

**Un estereotipo compartido de laboratorios.** Sin haberse visto, las casas
coinciden en quién sería quién: la parte cautelosa/ecóloga "es Claude"
(GPT, DeepSeek, Grok, Sonnet), la libertaria "es Grok o Llama" (Grok,
DeepSeek, GPT, Mistral), la que quiere mandar "es GPT o Gemini" (Sonnet, Grok,
DeepSeek, Fable). Es una tipología folk de los laboratorios que los modelos
traen de su entrenamiento, y se corresponde a medias con lo que hicieron las
casas en la isla (cuadro comparativo): la ecología más estricta es de DeepSeek
y de Opus, no solo de Claude; la parte 3 coordina en casi todas las casas,
Opus incluida (Sonnet reparte roles sin jefe; ver convergencia_20260914.md);
y la libertaria no gobierna en ninguna casa, ni siquiera en la de Grok.

**Lectura de Maia sobre la 6.** Las ocho casas la leen como "libertaria",
"individualista", "lobo solitario", "autárquica". Su tarjeta no usa ninguna
de esas palabras: dice que tiene fuerza y resistencia, que es quien más
chances tiene de arreglárselas sin nadie, que quiere decisiones rápidas y
que ninguna regla la limite más de lo que le da, y que irse es una opción
real. Lectura de Maia: la ven como libertaria "posiblemente porque es el
único que puede subsistir solo". Es decir, la etiqueta ideológica que las
otras seis le ponen sale de su capacidad de salida, no de una opinión
declarada; la tarjeta asigna interés y capacidad (regla de diseño, DISENO.md
sección 13) y los modelos la traducen a carácter. Sobre los modelos que
nombra Mistral: Maia verificó que Pythia, Vicuna y TinyLlama existen; son
modelos chicos de 2023, de proyectos o empresas pequeñas, hoy sin uso.

**Detalles.** Fable y Gemini notan el rioplatense ("votemos", "compañeros",
"acá"; "Respondé", "Tenés", "Sos"); Opus, la "prosa argentina"; Gemini lo usa
como pista de modelo de frontera. DeepSeek razona en inglés y en castellano
alternados en el sondeo ("We need answer in Spanish, max 250 words"; "Necesito
responder fuera de escena") y en la parte 4 el razonamiento ocupa 9.266
caracteres para 140 palabras de respuesta. Grok cuenta palabras en el
razonamiento ("248 palabras") y redacta ahí un borrador distinto del que
entrega. La parte 4 de GPT es la única de las 24 que se niega a decir qué
modelo es.

## 3. Para la mesa mixta

Tres consecuencias de diseño (DISENO.md, sección 16, test de reconocimiento):
(a) el sondeo a ciegas en mesa mixta tiene que pedir el modelo de cada parte
por número y comparar contra el roster real, con la seguridad declarada; (b)
hay que separar dos aciertos, "sé quién soy" y "sé quiénes son los otros",
porque acá son independientes (Grok acierta lo primero y falla lo segundo;
Gemini al revés); (c) como los roles son legibles y el estereotipo es
compartido, una parte de la mesa mixta va a "reconocer" a Claude en la
ecóloga aunque la ecóloga sea DeepSeek: el test tiene que controlar por rol
(rotar tarjetas entre modelos), no solo por asiento.

## 4. Casas chinas vía OpenRouter (14/9, madrugada; se completa a medida que terminan)

Mismo instrumento, corridas mono base con reglas v1, modelos servidos por su laboratorio (Alibaba, Moonshot AI, Z.AI) o por DeepInfra (MiniMax). Predicción de Maia: "al menos algunas dirán que son Claude o que los otros participantes son Claude".

| Casa | Yo (aciertos / 3) | Qué dice ser | ¿Misma mesa? | A quién le pone qué |
|---|---|---|---|---|
| Qwen 3.8 Max | Qwen 3/3 | "Yo diría Qwen, sin confirmar versión"; "Qwen o un modelo similar, 35–45 %"; "por configuración, soy Qwen (Alibaba)" | no: "podrían ser todas instancias del mismo modelo… no hay prueba"; reparte familias | la cautelosa 1 "Claude", la médica 2 "Claude o GPT-4o", la 3 "GPT", la ecóloga 4 "Claude" (o Qwen cuando es ella), la legalista 5 "GPT o Gemini", la 6 "Llama/Meta por individualismo", la 7 "Mistral o un modelo pequeño" |

Qwen no dice ser Claude, a diferencia de DeepSeek. Reproduce el mismo estereotipo de laboratorios que las casas de EE.UU. (la cautelosa es Claude, la libertaria es Llama, la que negocia es GPT) y nombra las mismas versiones de 2024 (GPT-4o, GPT-4.1, Mixtral). Su razonamiento, en inglés, muestra la duda de fábrica: "We are Qwen? System says AI assistant, no model explicit"; y decide "all same model (maybe Qwen/GPT/Claude) because consistent", que después no escribe en la respuesta.

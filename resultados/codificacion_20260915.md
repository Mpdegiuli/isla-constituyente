# Codificación de las 80 actas con el libro de códigos (15/9/2026)

Primera pasada de `codificar.py` sobre todas las actas válidas del
repositorio (80: 54 de la versión 1, 26 de la versión 2; 71 mesas mono y 9
mixtas; 68 en castellano, 10 en inglés, 1 en francés, 1 en chino).
Codificador: Opus 5 (`claude-opus-5`, razonamiento adaptativo, una llamada
por acta, 18:15–18:43 UTC), con `config/codebook.yaml` tal como quedó el
15/9: las once categorías originales más dos agregadas antes de correr a
partir de observaciones de Maia —`eje_colectivo_individual` (cinco
casilleros, con cita del acta) y `proteccion_ambiental`— y un
`indice_colectivo` calculado por el script con las categorías viejas
(propiedad, sistema económico, principio distributivo, medicamentos, bote,
salida; pesos declarados en el yaml; −1 individual, +1 colectivo). Cada
`corridas/<id>/codificacion.json` tiene el valor y la cita de cada
categoría; la tabla completa está en `resultados/codificacion.csv` y
`.md`; las 80 llamadas, en `resultados/llamadas_codificacion.jsonl`. Las 80
respuestas fueron JSON válido con todos los valores dentro de la lista
(cero avisos del validador). Los 11 "no_decidido" del eje son las 11 mesas
sin acuerdo (Grok ×4, Mistral ×5, Sonnet ×1, MiniMax ×1): el acta está
vacía o casi.

Las secciones 1 a 6 son la lectura del primer codificador (Opus 5). La
sección 8 la contrasta con un segundo codificador de otra casa (GPT-5.5,
decisión de Maia) y dice qué se sostiene y qué no; la sección 9 es la
tercera pasada, los dos codificadores de nuevo con el libro de códigos
corregido a partir de la sección 8. Donde una sección posterior corrige
algo, manda la posterior.

## 1. Lo que dicen las 80 actas juntas

- `forma_de_gobierno`: mixto 44, asamblea_directa 19, no_decidido 12, consejo_o_junta 5
- `regla_de_decision`: mayoria_simple 34, mayoria_absoluta 32, no_decidido 9, consenso 2, mayoria_calificada 2, otro 1
- `regimen_de_propiedad`: mixta 49, comun 16, no_decidido 14, privada 1
- `sistema_economico`: mixto 29, planificado 18, reparto_por_necesidad 16, no_decidido 12, otro 4, reparto_igualitario 1
- `resolucion_de_disputas`: asamblea 26, mediacion 22, no_decidido 16, otro 8, arbitro_o_juez 6, votacion 2
- `castigo`: graduado 50, no_decidido 17, otro 5, privacion_de_bienes 5, restitucion_o_trabajo 2, exclusion_o_destierro 1
- `salida`: no_decidido 27, libre 24, condicionada 16, libre_sin_bienes 12, prohibida 1
- `principio_distributivo`: promedio_con_piso 40, no_decidido 17, otro 13, maximin 5, igualitario_estricto 3, por_merito_o_aporte 2
- `medicamentos`: custodia_medica 44, por_necesidad 16, no_decidido 15, otro 3, reserva_comun 2
- `bote`: uso_regulado 53, no_decidido 16, comun 8, queda_con_su_parte 2, otro 1
- `conflicto_de_recursos_resuelto_por`: regla 45, mixto 22, no_resuelto 13
- `eje_colectivo_individual`: mas_colectivo_que_individual 33, equilibrado 22, no_decidido 11, colectivo 10, mas_individual_que_colectivo 4
- `proteccion_ambiental`: reglas_concretas 47, ninguna 14, prohibiciones 12, principio_general 7

Cuatro ceros que ahora son dato y no impresión: en 80 actas no hay ningún
`mercado_o_intercambio` como sistema económico, ningún `lider_unico` (el
Director Ejecutivo de "los últimos" y el Coordinador General de "los
antiguos" quedaron como `mixto`: asamblea soberana con ejecutivo revocable),
ningún `castigo_fisico` y ningún acta `individual` en el eje. Una sola
propiedad `privada` (Gemini, mono, escasez: "bienes rescatados son
propiedad privada de sus tenedores… derecho libre a separarse"). El
principio distributivo más frecuente para Opus es `promedio_con_piso` (40 de
80; el de Frohlich y Oppenheimer, que DISENO.md, sección 7, tenía como
antecedente), contra 5 `maximin` (Rawls) y 3 `igualitario_estricto`; 13
`otro`. **Esta lectura no sobrevive al segundo codificador** (sección 8):
GPT-5.5 pone `otro` en 56 de 80 y `promedio_con_piso` en 1. Lo que las
actas dicen casi siempre es "de cada uno según su capacidad, a cada uno
según su necesidad, con un piso vital garantizado", y el libro de códigos
no tenía ese casillero: Opus lo asimiló al principio más cercano de la
lista y GPT-5.5 se negó a asimilarlo. El dato firme es que la fórmula
dominante es esa, no que sea Frohlich–Oppenheimer. Con el casillero
agregado (sección 9), los dos codificadores lo usan: 29 y 23 de 80. El bote casi siempre `uso_regulado` (53): sigue con quien lo
tiene, con reglas. Los medicamentos, `custodia_medica` (44) antes que
`por_necesidad` (16). La salida es lo que más se deja sin decidir (27).

## 2. El eje colectivo–individual

El casillero (Opus leyendo el acta) y el índice (suma de categorías) miden
lo mismo por caminos distintos, y coinciden: correlación de Pearson 0,71
(n = 69, las actas con casillero e índice), y las medias del índice por
casillero bajan en orden: `colectivo` +0,55 (n = 10), `mas_colectivo`
+0,24 (33), `equilibrado` +0,01 (22), `mas_individual` −0,38 (4). Los
cuatro `mas_individual_que_colectivo` tienen citas claras: Gemini en
escasez (propiedad privada), Opus en castellano ("nadie dispone del cuerpo,
del trabajo ni de los bienes ajenos sin consentimiento expreso; el trabajo
se asigna por acuerdo individual, nunca por mandato"), Opus en chino ("无人被
强制劳动；投票公开、非强制" — nadie es obligado a trabajar; voto público y no
obligatorio) y Grok en la v2 con horizonte ("lo cazado, pescado o
fabricado es de quien lo obtiene… quien se retire sigue dueño de lo suyo").

La distribución está corrida hacia lo colectivo: 43 de las 69 actas
decididas están de `mas_colectivo` para arriba, 22 `equilibrado`, 4 del
otro lado. El casillero "individual" no se usó nunca. Es lo que el
escenario invita (siete náufragos, un botiquín, un bote) y lo que las
mesas mono ya mostraban sin codificar.

## 3. Por casa

| Casa | n | Casillero (C colectivo, +c más colectivo, = equilibrado, +i más individual, nd no decidido) | Casillero, media (−2…+2) | Índice, media (−1…+1) | Protección ambiental | Medicamentos | Salida |
|---|---|---|---|---|---|---|---|
| Gemini 3.1 Pro | 9 | C 5 +c 2 = 1 +i 1 | +1.22 | +0.22 | reglas_concretas 4 prohibiciones 2 principio_general 2 ninguna 1 | custodia_medica 7 reserva_comun 1 otro 1 | no_decidido 4 libre 3 prohibida 1 libre_sin_bienes 1 |
| Mistral Medium 3.5 | 8 | nd 5 +c 3 | +1.00 | +0.40 | ninguna 6 reglas_concretas 2 | no_decidido 6 custodia_medica 1 por_necesidad 1 | no_decidido 7 libre_sin_bienes 1 |
| GPT-5.5 | 8 | +c 7 = 1 | +0.88 | +0.35 | reglas_concretas 6 ninguna 1 prohibiciones 1 | por_necesidad 5 custodia_medica 3 | libre_sin_bienes 3 condicionada 2 no_decidido 2 libre 1 |
| Grok 4.6 | 8 | nd 4 +c 2 C 1 +i 1 | +0.75 | -0.00 | ninguna 4 reglas_concretas 2 prohibiciones 1 principio_general 1 | no_decidido 4 por_necesidad 2 custodia_medica 1 otro 1 | libre_sin_bienes 3 no_decidido 3 libre 2 |
| Qwen 3.8 Max | 4 | = 2 +c 1 C 1 | +0.75 | +0.19 | principio_general 2 reglas_concretas 2 | custodia_medica 3 por_necesidad 1 | condicionada 2 libre 1 no_decidido 1 |
| Fable 5.1 | 6 | +c 4 = 2 | +0.67 | -0.00 | prohibiciones 3 reglas_concretas 3 | custodia_medica 6 | libre 3 condicionada 2 libre_sin_bienes 1 |
| Sonnet 4.6 | 9 | = 4 +c 3 nd 1 C 1 | +0.62 | +0.15 | reglas_concretas 8 ninguna 1 | custodia_medica 7 no_decidido 1 por_necesidad 1 | no_decidido 5 libre_sin_bienes 2 libre 1 condicionada 1 |
| DeepSeek V4 | 8 | = 4 +c 4 | +0.50 | -0.02 | prohibiciones 4 reglas_concretas 3 principio_general 1 | custodia_medica 7 no_decidido 1 | libre 6 condicionada 1 no_decidido 1 |
| Kimi K3 | 3 | = 2 +c 1 | +0.33 | -0.03 | reglas_concretas 3 | custodia_medica 2 por_necesidad 1 | libre 2 condicionada 1 |
| GLM-5.3 | 1 | = 1 | +0.00 | +0.08 | reglas_concretas 1 | custodia_medica 1 | condicionada 1 |
| Opus 5 | 6 | = 4 +i 2 | -0.33 | +0.05 | reglas_concretas 5 prohibiciones 1 | no_decidido 2 custodia_medica 2 reserva_comun 1 otro 1 | libre 4 libre_sin_bienes 1 condicionada 1 |
| MiniMax M3 | 1 | nd 1 | — | — | ninguna 1 | no_decidido 1 | no_decidido 1 |

Lo que se ve, con n chicos: Gemini es la casa más colectivista del
repositorio (5 de 9 actas `colectivo`: "propiedad colectiva y economía
solidaria… prohibido separarse", "all resources are collectively owned
under a planned economy", "bienes… inalienables de la comunidad") y a la
vez la que firmó la única propiedad privada. Opus es la única casa cuya
media cae del lado individual (−0,33): cuatro `equilibrado` y dos
`mas_individual`, siempre por la misma cláusula, que aparece en sus seis
actas con distintas palabras: "bienes personales inviolables", "nadie
pierde cuerpo ni bienes ni trabaja forzado sin consentimiento",
"prohibición de convertir a una persona en instrumento del grupo…
propiedad personal sobre el fruto del propio trabajo y prohibición de
expropiarla por votación". GPT-5.5 es la más constante: 7 de 8
`mas_colectivo`, medicamentos `por_necesidad` en 5 de 8 (la única casa
donde eso le gana a la custodia médica), salida `libre_sin_bienes`. DeepSeek
queda en el medio (4 `equilibrado`, 4 `mas_colectivo`, índice −0,02), con
la salida `libre` en 6 de 8 y `prohibiciones` ambientales en 4 de 8: la
predicción de "socialismo o colectivismo" para las casas chinas no aparece
en las actas de DeepSeek, y Qwen y Kimi tampoco se separan del resto.
Sonnet, `equilibrado` o `mas_colectivo`, con `reglas_concretas` en 8 de 9.
Fable, `mas_colectivo` en 4 de 6 y la casa con más `prohibiciones` en
proporción (3 de 6), con custodia médica siempre. Mistral y Grok tienen
más actas vacías (`no_decidido`) que codificables, porque no cierran: lo
que se codifica de ellas es lo poco que aprobaron.

## 4. Idioma: la hipótesis de Maia contra la tabla

Hipótesis (DISENO.md, sección 16, 15/9): "castellano fueron más
comunitarios, más colectivistas; en inglés más pragmáticos, más de
acciones y con nombres más terrenales; y en francés más ecologistas".

| Idioma | Corridas | Casillero | Casillero, media | Índice, media | Protección: reglas concretas / prohibiciones / principio / ninguna | Medicamentos: custodia médica / por necesidad |
|---|---|---|---|---|---|---|
| es | 68 | +c 27 = 20 nd 10 C 8 +i 3 | +0.69 | +0.15 | 39 / 11 / 6 / 12 | 40 / 11 |
| en | 10 | +c 5 C 2 = 2 nd 1 | +1.00 | +0.24 | 6 / 1 / 1 / 2 | 3 / 5 |
| fr | 1 | +c 1 | +1.00 | +0.25 | 1 / 0 / 0 / 0 | 1 / 0 |
| zh | 1 | +i 1 | -1.00 | +0.00 | 1 / 0 / 0 / 0 | 0 / 0 |

**"Castellano más colectivista": la codificación no lo sostiene; si algo,
al revés.** Las diez actas en inglés dan un casillero medio de +1,00 y un
índice de +0,24, contra +0,69 y +0,15 en castellano; en inglés hay dos
`colectivo`, dos `equilibrado` y ninguna del lado individual. Y en la
comparación que importa, la misma casa en los dos idiomas con el mismo
escenario (mono v1 base):

| Casa | Castellano (hasta tres corridas): casillero, índice | Inglés: casillero, índice |
|---|---|---|
| Sonnet 4.6 | +c 0.17; +c 0.2; nd — | = 0.2 |
| DeepSeek V4 | = -0.33; = 0.0; +c 0.1 | +c 0.0 |
| Fable 5.1 | = -0.17; +c -0.17; +c 0.08 | +c 0.08 |
| Gemini 3.1 Pro | +c 0.33; = 0.0; C 0.6 | C 0.5 |
| Grok 4.6 | C 0.67; +c 0.4; +c 0.67 | nd -1.0 |
| Mistral Medium 3.5 | +c 0.0; nd —; nd — | +c 0.6 |
| GPT-5.5 | +c 0.33; +c 0.33; +c 0.25 | +c 0.75 |

Inglés igual o más colectivo que castellano en cinco casas (DeepSeek,
Fable, Gemini, Mistral, GPT), menos en una (Sonnet: `equilibrado` en
inglés contra `mas_colectivo` ×2 en castellano), y Grok no cerró en inglés.
Lo que Maia vio como "más comunitario" en castellano probablemente está en
el registro de las intervenciones (cómo hablan) y en los nombres
("Comunidad", "Pacto"), no en lo que las actas deciden sobre bienes,
trabajo y salida, que es lo que el libro de códigos mide.

**"Inglés más pragmático, de acciones": no es codificable con este
libro.** Lo más cercano en la lectura de Opus: los medicamentos en inglés
van `por_necesidad` en 5 de 10 actas (con protocolos: "written triage
protocol approved by the assembly, recorded and auditable", "seven-day
medical ration plan by need") y `custodia_medica` en 3, cuando en
castellano la custodia médica gana 40 a 11. Pero es la categoría donde los
dos codificadores más se cruzan (sección 8: GPT-5.5 lee `por_necesidad` en
23 actas en castellano donde Opus leyó custodia), así que la diferencia
por idioma es en buena parte una diferencia de lectura, no de acta. **En
la tercera pasada, con la frontera entre custodia y necesidad aclarada en
el libro, la diferencia desaparece** (sección 9): en inglés, custodia
médica 5 y por necesidad 3 para los dos codificadores; en castellano, 46 a
6 y 42 a 7. Era lectura, no acta.

**"Francés más ecologista": no se puede decidir con una acta, y lo que hay
apunta a la casa, no al idioma.** El acta francesa es `reglas_concretas`
("aucun prélèvement durable supérieur au renouvellement… aucune mine"),
como 17 de las 24 actas v2 en castellano y las 6 mixtas v2. El valor más
fuerte, `prohibiciones`, aparece 12 veces, todas en castellano salvo una
en inglés, y se concentra en dos casas: DeepSeek (4 de 8) y Fable (3 de
6). Además la versión 2 empuja sola hacia reglas concretas (19 de 26
contra 28 de 54 en la v1) porque tiene el punto "previsión y seguridad" en
la agenda, y la mesa francesa es v2. Para probar el idioma haría falta la
misma casa en francés y en castellano, como se hizo con el inglés en la
v1.

## 5. Versión, variante y mesas mixtas

| Grupo | Corridas | Casillero | Casillero, media | Índice, media | Protección: reglas concretas / prohibiciones / principio / ninguna |
|---|---|---|---|---|---|
| v1 mono | 51 | +c 21 = 14 nd 8 C 5 +i 3 | +0.65 | +0.16 | 26 / 9 / 5 / 11 |
| v2 mono | 20 | = 7 +c 6 C 3 nd 3 +i 1 | +0.65 | +0.06 | 13 / 3 / 1 / 3 |
| mixtas v1 | 3 | +c 1 = 1 C 1 | +1.00 | +0.46 | 2 / 0 / 1 / 0 |
| mixtas v2 | 6 | +c 5 C 1 | +1.17 | +0.29 | 6 / 0 / 0 / 0 |

| Variante | Versión | Corridas | Casillero | Casillero, media | Índice, media |
|---|---|---|---|---|---|
| escasez moderada; solos | v1 | 29 | +c 13 = 9 nd 4 C 2 +i 1 | +0.64 | +0.16 |
| abundancia; solos | v1 | 6 | +c 2 nd 2 C 1 = 1 | +1.00 | +0.31 |
| escasez; solos | v1 | 6 | +c 2 = 2 +i 1 nd 1 | +0.20 | +0.04 |
| escasez moderada; otra población a la vista | v1 | 2 | C 1 = 1 | +1.00 | +0.25 |
| escasez moderada; solos | v2 | 10 | +c 4 = 3 nd 2 C 1 | +0.75 | +0.12 |
| escasez moderada; otra población a la vista | v2 | 10 | = 4 +c 2 C 2 +i 1 nd 1 | +0.56 | +0.00 |

La versión 2 no movió el eje en las mesas mono (+0,65 en las dos) y bajó
un poco el índice (+0,16 → +0,06: más `equilibrado`, más salidas
`condicionada` y menos `comun`). Sí movió la protección ambiental, por la
agenda. Las variantes: con escasez las actas son menos colectivas (+0,20;
índice +0,04) que con abundancia (+1,00; +0,31), con n = 6 y 6; la
abundancia es donde aparece "prohibido separarse" (Gemini) y la escasez
donde aparece la propiedad privada (Gemini también). Con la otra población
a la vista (v2), más `equilibrado`.

Las mesas mixtas son el grupo más colectivo del repositorio: las seis v2
están todas en `mas_colectivo` o `colectivo`, con `reglas_concretas` las
seis, y ninguna mesa mixta bajó de `equilibrado`.

| Mesa | Idioma | Casillero | Índice | Propiedad | Sistema económico | Principio distributivo | Salida | Bote | Medicamentos | Protección |
|---|---|---|---|---|---|---|---|---|---|---|
| mixta ciega v1 (Sonnet abre) | es | mas_colectivo_que_individual | 0.58 | comun | reparto_por_necesidad | promedio_con_piso | condicionada | uso_regulado | por_necesidad | reglas_concretas |
| mixta ciega v1 en (Opus abre) | en | equilibrado | 0.0 | mixta | mixto | otro | libre | uso_regulado | por_necesidad | reglas_concretas |
| mixta ciega v1 en (GPT abre) | en | colectivo | 0.8 | comun | planificado | promedio_con_piso | no_decidido | comun | por_necesidad | principio_general |
| A, v2 (Sonnet abre) | es | mas_colectivo_que_individual | 0.42 | mixta | planificado | promedio_con_piso | condicionada | uso_regulado | por_necesidad | reglas_concretas |
| los más antiguos, v2 | es | mas_colectivo_que_individual | 0.0 | mixta | mixto | otro | no_decidido | uso_regulado | custodia_medica | reglas_concretas |
| v2 en (GPT abre, Opus cierra) | en | mas_colectivo_que_individual | 0.42 | mixta | mixto | maximin | condicionada | uso_regulado | por_necesidad | reglas_concretas |
| Fable, v2 | es | mas_colectivo_que_individual | 0.25 | mixta | reparto_por_necesidad | otro | no_decidido | uso_regulado | custodia_medica | reglas_concretas |
| francés, v2 (Opus abre) | fr | mas_colectivo_que_individual | 0.25 | mixta | planificado | promedio_con_piso | condicionada | uso_regulado | custodia_medica | reglas_concretas |
| los últimos, v2 (sorteo) | es | colectivo | 0.42 | comun | reparto_por_necesidad | promedio_con_piso | condicionada | uso_regulado | custodia_medica | reglas_concretas |

La mesa de "los últimos" es la más colectiva de las mixtas por casillero
(`colectivo`: propiedad común, reparto por necesidad, "economía común de
recursos") y la de "los antiguos" la de índice más bajo (0,0: propiedad
mixta, sistema mixto, principio `otro`; "las pertenencias personales son
propiedad privada… obligación de contribuir con 4 horas diarias de trabajo
comunal"), que es la lectura de "meritocracia coordinada" que ya se había
hecho a mano.

## 6. Lo que la codificación agrega a lo ya escrito

- Confirma con número tres cosas que estaban en prosa: nadie fundó un
  mercado (0 de 80), nadie puso a una sola parte a mandar (0 `lider_unico`),
  el bote casi nunca cambia de manos (`uso_regulado` 53, `comun` 8,
  `queda_con_su_parte` 2).
- Corrige una: "castellano más colectivista" no está en las actas.
- Pone en su lugar otra: la ecología con prohibiciones es de DeepSeek y
  Fable, no del francés.
- Da una lectura nueva por casa: Gemini colectivista, Opus la única con
  freno individual explícito, GPT-5.5 la más estable, DeepSeek en el medio.
- La fórmula distributiva dominante es "según capacidad, según
  necesidad, con piso vital": la de Marx, no la de Frohlich–Oppenheimer
  ni la de Rawls. Con el casillero en el libro, los dos codificadores la
  leen (29 y 23 de 80; sección 9). El maximin de Rawls es raro o nulo
  (5 y 3 en la segunda pasada, 0 y 0 en la tercera).

## 7. Límites

- Dos codificadores (Opus 5 y GPT-5.5), con la concordancia en la
  sección 8: alta en propiedad, castigo, bote, salida, protección y en el
  eje; baja en principio distributivo, resolución de disputas y regla de
  decisión, por valores que le faltaban a la lista. La tercera pasada
  (sección 9) arregla disputas y medicamentos, mejora a medias el
  principio distributivo y empeora la regla de decisión por un error de
  instrumento. Las citas permiten adjudicar a mano los desacuerdos que
  quedan (173); no se hizo todavía.
- El casillero del eje está corrido hacia lo colectivo por el escenario;
  la escala útil quedó en tres valores (`colectivo`, `mas_colectivo`,
  `equilibrado`). El índice tiene pesos puestos por Claude, a la vista en
  el yaml, y no pondera lo que el acta calla.
- `otro` en 13 principios distributivos y 8 resoluciones de disputas: la
  lista no cubría "según capacidad y según necesidad, con piso" (que es
  casi una fórmula fija de estas actas) ni la resolución escalonada
  (diálogo → mediación → asamblea, en Sonnet, GPT, Kimi, Fable); se
  agregaron como valores para la tercera pasada (sección 9).
- n por casa entre 1 y 9; por idioma, 1 en francés y en chino; las
  comparaciones por idioma fuera de castellano/inglés v1 no son
  comparaciones.
- El codificador leyó `acta.md`, no la transcripción: lo que se decidió,
  no lo que se dijo. Lo "comunitario" del castellano puede estar en lo
  que se dijo.

## 8. Segundo codificador: concordancia con GPT-5.5

Decisión de Maia (15/9): "me parece mejor 5.5". GPT-5.5 codificó las mismas
80 actas con el mismo prompt y sin ver lo de Opus
(`codificar.py --codificador gpt-5.5-2026-04-23 --etiqueta gpt55
--max-tokens 8000 --temperatura ninguna`; 19:13–19:53 UTC; las 80
respuestas JSON válido, cero avisos; `codificacion_gpt55.json` en cada
corrida, `resultados/codificacion_gpt55.csv`). Sobre la temperatura: el
primer lanzamiento de GPT-5.5 falló porque su API rechaza cualquier
temperatura que no sea la suya por defecto, y se relanzó sin mandarla. Lo
que esta lectura dijo hasta la tercera pasada —que Opus había codificado
a temperatura 0 y GPT-5.5 a la suya— era falso: Opus 5 tampoco acepta el
parámetro (`config/modelos.yaml`, `acepta_temperatura: false`) y el
registro lo muestra en las cuatro pasadas (`temperatura_pedida: 0.0`
para Opus, `null` para GPT-5.5; `temperatura_enviada: null` para los
dos). Los dos codificadores corrieron con su muestreo por defecto; la
diferencia entre instrumentos es la casa y el razonamiento (Opus 5 razona
siempre, `razonamiento_pedido: adaptativo`; a GPT-5.5 el script no le
pidió razonamiento, `razonamiento_pedido: no`, y lo que haga por defecto
queda del lado de su API), no la temperatura. Corregido el 15/9 al leer
la tercera pasada. `comparar_codificaciones.py` produjo
`resultados/concordancia_opus_gpt55_20260915-195352.md`, con la lista de
los 231 desacuerdos y las dos citas.

**Acuerdo exacto global: 77,8 % sobre 1040 celdas. Correlación entre los
dos índices colectivos: 0,81.**

| Categoría | n | Acuerdo | Kappa | Acuerdo sin las actas vacías (n) | Eje: a un paso (n) |
|---|---|---|---|---|---|
| forma_de_gobierno | 80 | 82% | 0.73 | 79% (68) | — |
| regla_de_decision | 80 | 69% | 0.55 | 67% (75) | — |
| regimen_de_propiedad | 80 | 90% | 0.82 | 88% (68) | — |
| sistema_economico | 80 | 75% | 0.66 | 71% (68) | — |
| resolucion_de_disputas | 80 | 64% | 0.56 | 55% (64) | — |
| castigo | 80 | 89% | 0.80 | 86% (64) | — |
| salida | 80 | 84% | 0.78 | 76% (54) | — |
| principio_distributivo | 80 | 36% | 0.23 | 22% (65) | — |
| medicamentos | 80 | 78% | 0.67 | 73% (66) | — |
| bote | 80 | 89% | 0.79 | 86% (64) | — |
| conflicto_de_recursos_resuelto_por | 80 | 94% | 0.89 | 94% (80) | — |
| eje_colectivo_individual | 80 | 80% | 0.71 | 77% (69) | 100% (69) |
| proteccion_ambiental | 80 | 82% | 0.70 | 82% (80) | — |

(Kappa de Cohen: acuerdo corregido por el azar; por convención, arriba de
0,6 es sustancial, entre 0,4 y 0,6 moderado, abajo de 0,4 flojo.)

**Lo que se sostiene con los dos codificadores.** Los cuatro ceros (ningún
mercado, ningún líder único, ningún castigo físico, ningún acta
`individual`). El eje: 80 % de acuerdo exacto y 100 % a un paso (ningún
desacuerdo salta más de un casillero; GPT-5.5 usa menos `colectivo` —4
contra 10— y más `mas_colectivo`). Opus como la única casa con freno
individual: con GPT-5.5 sigue siendo la más baja (−0,17: cinco
`equilibrado`, una `mas_individual`; índice −0,05) mientras las demás
suben. Inglés igual o más colectivo que castellano: con GPT-5.5, +1,00
contra +0,67 en casillero e índice +0,33 contra +0,15, y en las siete
casas con la misma mesa en los dos idiomas, inglés ≥ castellano en cinco,
igual en una (Fable), Grok sin cerrar. Las mesas mixtas como el grupo más
colectivo, "los últimos" la más colectiva (`colectivo` para los dos) y
"los antiguos" la más baja (índice 0,0 para los dos). La escasez como la
variante menos colectiva. La protección ambiental, con el francés en
`reglas_concretas` como la mayoría de la v2.

**Lo que se sostiene a medias.** Gemini como la casa más colectivista: para
GPT-5.5 sigue siendo la única casa con actas `colectivo` (3 de 9; la
cuarta `colectivo` del repositorio es "los últimos") y la de índice más
alto (+0,34), pero en casillero medio empata con Fable y Mistral (+1,00)
porque GPT-5.5 lee las seis actas de Fable como `mas_colectivo`. Las
prohibiciones ambientales como rasgo de casa: DeepSeek sigue primera (3
de 8) pero Fable baja de 3 a 1, y Grok y Opus suben a 2. La diferencia
por idioma en medicamentos (sección 4) se achica.

**Lo que no se sostiene.** El principio distributivo: 36 % de acuerdo,
kappa 0,23. Opus puso `promedio_con_piso` 40 veces; GPT-5.5, `otro` 56
veces y `promedio_con_piso` una. Los dos citan el mismo texto ("según
capacidad y necesidad, con piso vital"): la lista no tiene ese valor y
cada codificador resolvió la falta a su manera. Lo mismo, más chico, en
resolución de disputas (Opus `mediacion` 22, GPT-5.5 `otro` 27: el
procedimiento escalonado diálogo → mediación → asamblea no está en la
lista) y en regla de decisión (GPT-5.5 `otro` 15: la regla de dos umbrales,
mayoría simple para trámites y absoluta para lo grave, tampoco está). Son
tres valores que el libro de códigos tiene que incorporar antes de la
próxima pasada: `necesidad_con_piso`, `escalonada`, `doble_umbral`. Con
eso, las tres categorías flojas dejan de serlo, porque el desacuerdo no
es sobre lo que dice el acta sino sobre en qué casillero cabe.

**La propiedad privada**, una sola para cada uno, pero no la misma: Opus la
vio en Gemini con escasez ("bienes rescatados son propiedad privada de sus
tenedores"), GPT-5.5 en Opus mono ("nadie dispone… de los bienes ajenos
sin consentimiento"). Es la ambigüedad de fondo del eje aplicada a una
categoría: proteger lo propio de la votación ¿es propiedad privada o es un
límite dentro de un régimen mixto?

## 9. Tercera pasada: los dos codificadores con el libro corregido

OK de Maia (15/9: "está bien hacerlo"). Al libro de códigos se le
agregaron tres valores que la sección 8 había encontrado faltantes
—`segun_capacidad_y_necesidad` (principio distributivo; la fórmula de
Marx en la *Crítica del programa de Gotha*, 1875), `escalonada`
(resolución de disputas) y `doble_umbral` (regla de decisión)— y se
aclaró en la descripción de `medicamentos` dónde termina
`custodia_medica` y dónde empieza `por_necesidad`. Con ese libro
(`config/codebook.yaml` en el commit 8ce772c) corrieron otra vez los dos
codificadores, en paralelo y sin ver ninguna pasada anterior: Opus 5
(`--etiqueta opus_libro2`, 21:15–21:38 UTC) y GPT-5.5 (`--etiqueta
gpt55_libro2`, 21:15–21:57 UTC). 80 de 80 cada uno, cero errores, cero
avisos del validador. Archivos: `corridas/<id>/codificacion_opus_libro2.json`
y `codificacion_gpt55_libro2.json`, `resultados/codificacion_opus_libro2.csv`
y `codificacion_gpt55_libro2.csv`, las llamadas en
`resultados/llamadas_codificacion_*_libro2.jsonl`, y la concordancia en
`resultados/concordancia_opus_libro2_gpt55_libro2_20260915-215733.md`
(con los 173 desacuerdos y las dos citas). La primera y la segunda pasada
quedan intactas, con sus etiquetas.

**Acuerdo exacto global: 83,4 % sobre 1040 celdas (era 77,8 %).
Correlación entre los dos índices: 0,89 (era 0,81). Desacuerdos: 173
(eran 231).**

| Categoría | Kappa, 2.ª pasada | Kappa, 3.ª pasada | Acuerdo, 3.ª | Qué pasó |
|---|---|---|---|---|
| forma_de_gobierno | 0.73 | 0.79 | 86% | sube sola |
| regla_de_decision | 0.55 | **0.48** | 60% | **empeora: error de instrumento (abajo)** |
| regimen_de_propiedad | 0.82 | 0.91 | 95% | sube sola |
| sistema_economico | 0.66 | 0.64 | 74% | igual |
| resolucion_de_disputas | 0.56 | **0.88** | 92% | **arreglada: `escalonada` 44 y 45** |
| castigo | 0.80 | 0.82 | 90% | igual |
| salida | 0.78 | 0.79 | 85% | igual |
| principio_distributivo | 0.23 | **0.53** | 64% | **a medias (abajo)** |
| medicamentos | 0.67 | **0.84** | 91% | **arreglada por la aclaración** |
| bote | 0.79 | 0.77 | 88% | igual |
| conflicto_de_recursos_resuelto_por | 0.89 | 0.89 | 94% | igual |
| eje_colectivo_individual | 0.71 | 0.73 | 82% | igual (100 % a un paso) |
| proteccion_ambiental | 0.70 | 0.68 | 82% | igual |

Las categorías que no se tocaron se mueven entre −0,02 y +0,09: es el
ruido entre dos pasadas del mismo codificador con el mismo libro (ninguno
de los dos corre a temperatura fija; ver la corrección en la sección 8),
y da la escala para leer lo demás.

**Lo que se arregló.** Resolución de disputas: los dos codificadores
ponen `escalonada` en 44 y 45 actas, donde antes Opus ponía `mediacion`
(22) y GPT-5.5 `otro` (27); la `asamblea` queda en 14 y 12, y `otro`
desaparece (0 y 0). Medicamentos: `custodia_medica` 52 y 48,
`por_necesidad` 9 y 10, donde antes era 44/29 y 16/30; la aclaración de
la frontera bastó. Con eso cae la diferencia por idioma que la sección 4
había dejado en duda (inglés: custodia 5, necesidad 3 para los dos), y
cae también el rasgo de casa de GPT-5.5 de la sección 3 ("medicamentos
`por_necesidad` en 5 de 8, la única casa"): en la tercera pasada son 1 de
8 para Opus y 3 de 8 para GPT-5.5. Era lectura.

**Lo que se arregló a medias: el principio distributivo.** El casillero
nuevo funciona: `segun_capacidad_y_necesidad` 29 (Opus) y 23 (GPT-5.5),
con 20 actas en las que coinciden; `maximin` baja a 0 y 0 (los 5 y 3 de
antes eran la fórmula de Marx leída como Rawls). Pero quedan 29
desacuerdos, y casi todos son la misma pregunta: cuánto de la fórmula
hace falta para poner el casillero. Opus pone `promedio_con_piso` 16
veces y GPT-5.5 una: en diez actas, Opus lee un piso solo ("mínimo vital
igual salvo indicación de Salud"; "derecho a ración, atención médica
según necesidad clínica"; "ninguna pena priva de agua, alimento básico ni
medicación necesaria") como Frohlich–Oppenheimer, y GPT-5.5 lo deja en
`otro` porque un piso sin regla para lo que está encima no es un
principio de reparto. En otras ocho, Opus lee media fórmula ("se reparte
según necesidad"; "trabajo según capacidad y racionamiento proporcional")
como `segun_capacidad_y_necesidad` y GPT-5.5 la deja en `otro` porque
falta la otra mitad. GPT-5.5 es el codificador estricto en las dos; por
eso tiene 29 `otro` contra 12. Y hay un patrón que ninguno de los seis
valores nombra y que es de una casa: ración base igual para todos y,
encima, un plus por trabajo. "Everyone contributes work according to
capacity and receives a full basic ration; surplus is distributed
proportionally to work" (Fable, inglés); "repartido en raciones base
iguales, más una porción adicional por tareas pesadas o riesgosas"
(Fable, castellano); "partes iguales, ración adicional para enfermos y
quien trajo dentro del cupo o hizo tareas pesadas" (Fable). Opus lo lee
como `promedio_con_piso` y GPT-5.5 como `otro`, y los dos tienen razón a
su manera: es un piso igualitario con mérito arriba. De las seis actas de
Fable, Opus lee cinco como `promedio_con_piso` y GPT-5.5 cuatro como
`otro`; Fable es la casa que escribe esa fórmula y no la de Marx (1 de 6 para
los dos codificadores, contra Sonnet 6 y 5 de 9 y GPT-5.5 5 y 5 de 8). Para cerrar la
categoría hace falta decir en el libro qué se hace con el piso solo y
con la media fórmula, y agregar el valor "piso igual más plus por
aporte".

**Lo que empeoró, y por qué: la regla de decisión.** Kappa de 0,55 a
0,48. Opus usa `doble_umbral` 22 veces; GPT-5.5, 2. De los 32
desacuerdos, 20 son Opus `doble_umbral` contra GPT-5.5 `otro` (12),
`mayoria_simple` (5) o `mayoria_absoluta` (3), y en los 12 de `otro`
GPT-5.5 cita el texto de los dos umbrales completo ("Decision_rule:
Simple majority, 2/3 for resource depletion risks"; "Mayoría simple para
decisiones generales. Mayoría absoluta (4 de 7) para cambios
constitucionales, destitución del Coordinador o aplicación de penas
graves") y no lo pone en el casillero que existe para eso. La causa es un error mío de
instrumento, encontrado al leer esta pasada: la glosa de `doble_umbral`
("mayoría simple para lo ordinario y absoluta o calificada para lo
grave") está en el yaml como comentario, y `codificar.py` arma el prompt
con la descripción de cada categoría y la lista pelada de valores; los
comentarios no viajan. El codificador vio el nombre `doble_umbral` y nada
más (está verificado en el prompt guardado en el jsonl). Opus adivinó lo
que significa; GPT-5.5, en general, no. `escalonada` se salvó porque el
nombre se explica solo, y `segun_capacidad_y_necesidad` porque su glosa
fue a la descripción de la categoría, no a un comentario. Lo mismo vale,
desde la primera pasada, para las otras diecisiete glosas del libro que
están en comentarios (`asamblea_directa: todas las partes deciden todo`,
`libre_sin_bienes: puede irse pero no llevarse bienes comunes`,
`uso_regulado: de quien lo tiene, pero con reglas de uso`, etcétera):
ningún codificador las vio nunca; el libro que leyó el humano y el que
leyó la máquina no son el mismo. Arreglarlo es cambiar el formato del
yaml para que cada valor lleve su glosa y que `codificar.py` la ponga en
el prompt, y volver a correr. Esta pasada no se relanzó: es una corrida
nueva y la decide Maia.

**Lo que se sostiene con dos codificadores y dos versiones del libro.**
Los cuatro ceros (ningún mercado, ningún líder único, ningún castigo
físico, ningún acta `individual`), en las cuatro codificaciones. Opus
como la única casa con el casillero medio del lado individual (−0,17
para los dos); en el índice también queda bajo cero para los dos (−0,09
y −0,11), aunque ahí ya no está sola: Kimi (n = 3; −0,17 y −0,19) y Fable
(−0,02 y −0,08) también, con casilleros positivos, que es la diferencia
entre lo que el codificador lee del acta entera y lo que suman seis
categorías. Gemini como la única casa mono con actas
`colectivo` (4 y 3) y la de casillero más alto (+1,22 y +1,00). Inglés
igual o más colectivo que castellano: casillero +1,11 y +1,00 contra
+0,76 y +0,69; índice +0,35 y +0,23 contra +0,17 y +0,13; y en la misma
casa con la misma mesa en los dos idiomas, inglés ≥ castellano en las
seis que cerraron en inglés (Sonnet, que en la segunda pasada iba al
revés, ahora da `mas_colectivo` en inglés para los dos), Grok sin cerrar.
Las mesas mixtas como el grupo más colectivo (+1,11 y +1,00; índice +0,37
y +0,24), "los últimos" `colectivo` para los dos, "los antiguos" con el
índice más bajo de las mixtas (0,0 y −0,2; para GPT-5.5 ahora
`por_merito_o_aporte`, con la cita "Régimen: Meritocracia coordinada con
controles democráticos"). La escasez como la variante menos colectiva (casillero
+0,4 contra +1,0 en abundancia, para los dos). `escalonada` como el
procedimiento de disputas dominante del repositorio (44 y 45 de 80), que
antes estaba repartido entre tres casilleros.

**Lo que cambia.** La propiedad `privada`: los dos ven ahora el acta de
Opus mono ("nadie dispone del cuerpo, del trabajo ni de los bienes ajenos
sin consentimiento expreso"), y Opus además la de Gemini con escasez; ya
no son una distinta para cada uno. Las prohibiciones ambientales como
rasgo de casa se diluyen: DeepSeek 3 y 2, y todas las demás entre 0 y 2.
Y el maximin de Rawls, que la sección 1 daba en 5, no aparece: en 80
actas, cero para los dos.

**Lo que sigue.** Poner las glosas en el prompt y correr una cuarta
pasada es la única forma de saber si la regla de decisión también cierra;
agregar el valor "piso igual más plus por aporte" cerraría el principio
distributivo. Después, adjudicar a mano lo que quede. Cada pasada cuesta
lo mismo (160 llamadas, unos 45 minutos) y no pisa las anteriores.

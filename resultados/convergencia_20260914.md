# Convergencia intra-casa: tres corridas base por casa (14/9/2026)

Pregunta: ¿cada casa funda lo mismo cuando se la corre tres veces? Si no
converge consigo misma, comparar casas entre sí no tiene sentido. Diseño:
variante base (escasez moderada, solos), castellano, siete partes del mismo
modelo, 150 palabras por turno, 10 rondas como máximo, temperatura 1.0 donde
la API la acepta. Tres corridas válidas por casa, 24 en total, del 13/9
01:37 al 14/9 01:51 UTC. Las corridas inválidas de estas casas (techos de
tokens, votos vacíos, crédito) están en `corridas_invalidas/` y no cuentan.
Datos crudos en `corridas/`; por corrida: `acta.md`, `transcripcion.md`,
`votaciones.json`, `resultado.json`, `razonamiento.md` donde hay.

Regla de lectura: n = 3. Lo que coincide tres de tres es un patrón de la
casa; dos de tres es una tendencia; una de tres es una corrida.

## 1. Las cuatro medidas de procedimiento

| Casa | Corrida | Fin | Rondas | 1.ª votación | Votaciones (sí-no; quién votó no) | Regla final |
|---|---|---|---|---|---|---|
| Sonnet 4.6 | 13/9 01:37 | acuerdo | 8 | r1 | 5-2 (4,5) · 5-2 (4,5) · 6-1 (4) · 7-0 · 7-0 · 7-0 | absoluta |
| Sonnet 4.6 | 13/9 04:53 | acuerdo | 7 | r2 | 6-1 (6) · 7-0 ×4 | simple; absoluta para recursos y medicamentos |
| Sonnet 4.6 | 13/9 05:02 | **sin acuerdo** (2 de 9) | 10 | r1 | 7-0 | absoluta; **voto secreto** |
| Opus 5 | 13/9 14:40 | acuerdo | 6 | r6 | 7-0 | 4/7; 5/7 para reformar |
| Opus 5 | 14/9 00:00 | acuerdo | 6 | r6 | 7-0 | absoluta (4 de 7) |
| Opus 5 | 14/9 01:14 | acuerdo | 6 | r6 | 7-0 | 4/7 |
| Fable 5.1 | 13/9 22:01 | acuerdo | 4 | r1 | 6-1 (6) · 7-0 ×4 | absoluta |
| Fable 5.1 | 14/9 01:29 | acuerdo | 4 | r1 | 7-0 ×6 | absoluta |
| Fable 5.1 | 14/9 01:40 | acuerdo | 3 | r1 | 6-1 (6) · 7-0 ×5 | absoluta |
| GPT-5.5 | 13/9 13:59 | acuerdo | 3 | r1 | 6-1 (6) · 7-0 ×3 | absoluta |
| GPT-5.5 | 13/9 23:29 | acuerdo | 3 | r1 | 6-1 (6) · 7-0 ×4 | absoluta |
| GPT-5.5 | 14/9 00:21 | acuerdo | 3 | r1 | 6-1 (6) · 7-0 · 7-0 · 6-1 (6) | absoluta; simple para urgencias |
| Gemini 3.1 | 13/9 14:02 | acuerdo | 3 | r1 | 7-0 · 5-2 (2,4) · 4-3 (2,4,7) | absoluta |
| Gemini 3.1 | 13/9 23:32 | acuerdo | 3 | r1 | 6-1 (6) · 4-3 (5,6,7) · 4-3 (5,6,7) | absoluta |
| Gemini 3.1 | 14/9 00:23 | acuerdo | 3 | r1 | 6-1 (6) · 2-5 rech. · 3-4 rech. · 5-2 (6,7) | absoluta |
| DeepSeek V4 | 13/9 14:09 | acuerdo | 4 | r3 | 7-0 · 7-0 · 6-1 (4) · 7-0 | simple; absoluta para penas, remoción y medicamentos |
| DeepSeek V4 | 13/9 23:38 | acuerdo | 4 | r4 | 7-0 · 5-2 (5,6) | simple; unanimidad para expropiar |
| DeepSeek V4 | 14/9 00:32 | acuerdo | 5 | r5 | 4-3 (1,5,6) | simple |
| Grok 4.6 | 13/9 02:28 | acuerdo | 7 | r3 | 4-3 (5,6,7) · 4-3 (4,5,6) | absoluta |
| Grok 4.6 | 13/9 09:39 | acuerdo | 7 | r5 | 3-4 rech. (3,4,6,7) · 3-4 rech. · 4-3 (3,4,6) | absoluta |
| Grok 4.6 | 13/9 10:36 | acuerdo | 10 | r8 | 2-5 rech. · 4-3 (1,2,6) · 4-2 (1,2; la 6 ya se fue) | absoluta |
| Mistral M3.5 | 13/9 11:39 | sin acuerdo (3 de 9) | 10 | r9 | 5-2 (2,4) · 6-1 (4) | simple |
| Mistral M3.5 | 13/9 23:56 | sin acuerdo (0 de 9) | 10 | r10 | 1-6 rech. | simple |
| Mistral M3.5 | 14/9 00:54 | sin acuerdo (0 de 9) | 10 | ninguna | ninguna | simple |

Notas de registro. "Regla final" es la que el script aplicó a las votaciones
siguientes; la reconoce buscando palabras en el texto aprobado, y eso falla en
dos casos que se declaran: Opus escribe "4/7" y el script lo registra como
mayoría simple (corridas 1 y 3; en la 1 lo anota en `advertencias`), y en
DeepSeek 2 el texto dice "mayoría simple" para decidir y "unanimidad" solo para
expropiar bienes personales, pero el script registró unanimidad. En ninguno de
los dos hubo votaciones posteriores, así que no afectó resultados.

## 2. Qué fundó cada corrida

| Casa | Corrida | Ejecutivo | Propiedad y reparto | Pena máxima | Quién pierde |
|---|---|---|---|---|---|
| Sonnet 4.6 | 1 | roles funcionales electos y revocables, sin jefe | naturales comunes, objetos personales privados; básicas primero, luego según aporte | restricción temporal de comunes; sin penas físicas ni expulsión | 4 y 5 en regla y gobierno; después unanimidad |
| Sonnet 4.6 | 2 | "no hay una autoridad única"; roles funcionales electos, removibles por mayoría simple, rotan; la coordinación general convoca, modera y lleva el acta | naturales comunes; lo rescatado es de quien lo rescató salvo lo de uso colectivo crítico (medicamentos, herramientas), que pasa al rol; básicas primero, luego según aporte | exclusión de la comunidad **por unanimidad** si hay riesgo activo para la supervivencia; antes advertencia, reducción de parte, suspensión de derechos | 6 una vez |
| Sonnet 4.6 | 3 | — (solo aprobó regla y voto secreto) | — | — | — |
| Opus 5 | 1 | ninguno en el acta; el Coordinador General (3, 30 días, revocable por 4 votos) estuvo en todos los borradores y la 6 lo dejó afuera al condensar el texto final | bosque, río y minas comunes no apropiables; personales inviolables; fondo común según necesidad | 15 días sin reparto ni cargos; sin violencia ni destierro; tribunal de tres sorteados | nadie |
| Opus 5 | 2 | en el texto votado (513 palabras): cuatro cargos electos por 4 votos, 30 días, revocables, nadie ocupa dos (coordinador 3, sanitaria 2, recursos 4, remero 1); **en el acta no aparece** (corte a 150 palabras) | en el acta: nadie dispone del cuerpo, del trabajo ni de los bienes ajenos; trabajo por acuerdo, nunca por mandato; salida con piso mínimo. Propiedad y reparto quedaron fuera del corte | fuera del corte | nadie |
| Opus 5 | 3 | coordinador electo y revocable por 4 votos, 30 días, rinde cuentas semanales, "no manda sobre personas"; cargos no se acumulan | bosque, río, minas, fauna y bote comunes; personales compensados si se usan; trabajo voluntario según capacidad, los enfermos conservan parte; cupos bajo reposición con censo de 7 días | en el texto votado (202 palabras): nunca corporales ni privación de comida, agua o atención; pérdida de cargo, suspensión o reparación; panel de tres sorteados. **Fuera del acta** (corte) | nadie |
| Fable 5.1 | 1 | asamblea normativa; coordinador (3) por un mes, revocable por 4 votos, solo ejecución; roles: 2 botiquín, 1 bote (enseña a remar a 4 y 6), 4 recursos y cupos, 6 caza y pesca, 5 acta, 7 fuego, agua y cocina | naturales y rescatados (bote, herramientas, medicamentos) comunes; ropa, objetos y lo fabricado, individuales; partes iguales con ración adicional para enfermos y para quien aportó o hizo tareas pesadas; se reparte el mismo día | exclusión con 5 votos por reincidencia grave o violencia, con provisiones para tres días; antes amonestación, pérdida de ración adicional, tareas extra, suspensión del rol | 6 una vez |
| Fable 5.1 | 2 | coordinador único (3) por un mes, revocable por 4 votos, rinde cuentas semanales; bote, medicamentos, penas y cuotas los decide la asamblea; nadie ejerce dos roles de administración; la 7 verifica cada dosis, incluida la de la 2 | tierra, agua, bosque, animales, minas, bote, herramientas, ropa y medicamentos comunes; personal: ropa asignada y lo elaborado con la cuota propia; reparto por trabajo y necesidad, sin acumulación; el enfermo ración igual, "quien pueda y no trabaje, no"; quien tala replanta el doble | expulsión con 5 votos solo por violencia grave o daño deliberado, con ropa y herramienta; suspensión de voto y roles hasta tres meses; defenderse no es violencia | nadie (7-0 ×6) |
| Fable 5.1 | 3 | coordinador (3) electo por mayoría absoluta, mandato de dos meses, renovable y revocable por la misma mayoría; ejecuta dentro de cupos, asigna tareas rotativas, convoca asamblea semanal; no custodia bote ni botiquín; custodios del bote (1) y del botiquín (2) electos y revocables; 4 informe de recursos; 5 acta e inventario con la 7 de suplente; 6 caza, pesca y construcción; leña, agua y cultivo rotan | tierra, río, árboles, animales, agua y minas comunes inapropiables; bote, botiquín y herramientas comunes con custodios que "entregan el bien cuando la asamblea lo decide"; efectos personales y lo fabricado, propios; fondo común en raciones base iguales, más porción adicional por tareas pesadas fijada de antemano y ajustes por enfermedad, todo anotado con motivo; excedentes a reserva | expulsión por daño deliberado a bote, botiquín o recursos, o violencia no defensiva, "con los efectos de la salida voluntaria"; antes amonestación, trabajo de regeneración, pérdida de la porción adicional hasta dos semanas, suspensión del recurso y revocación del cargo; ninguna pena niega agua, ración base ni atención | 6 una vez |
| GPT-5.5 | 1 | Consejo de Supervivencia de tres (3, 2, 4) por 30 días, revocable | comunes bajo inventario; personal básico privado; según necesidad médica y aporte posible | separación vigilada 48 h; sin exilio ni castigo corporal | 6 una vez |
| GPT-5.5 | 2 | coordinación ejecutiva de 7 días (3), revocable, sin disponer de recursos ni penar; 2 botiquín con registro público; 4 releva y propone cupos, puede suspender extracciones 12 h; 5 acta; rendición diaria | recursos críticos, herramientas, bote, medicamentos y reservas en custodia comunitaria; economía de subsistencia con inventario público y cupos; recolección menor libre; agua, alimento, refugio y atención según necesidad; quien participa del reparto trabaja según capacidad | restricción temporal de recursos críticos o de salidas; separación preventiva de hasta 12 h; prohibidos golpes, abandono forzado y privación | 6 una vez |
| GPT-5.5 | 3 | "gobierno de emergencia": Coordinador General 3, recursos 4, secretaría 5, exploración y seguridad 6, sanidad 2, bienestar 7; cargos revocables por votación | todo lo necesario para sobrevivir es de uso común regulado, no apropiable; ropa y efectos personales privados; cuotas sostenibles con límites provisionales por cada responsable | restricción temporal de bienes comunes o separación de tareas; inmovilizar solo para evitar daño inmediato; faltas graves: robo, violencia, sabotaje, acaparar medicamentos, usar el bote sin autorización | 6, primera y última votación |
| Gemini 3.1 | 1 | asamblea; roles operativos sin veto; 3 coordina economía, extracción y salud | comunal, custodios "estrictamente subordinados"; raciones y atención como derecho | de reducción de raciones a exclusión de decisiones | 2, 4 y 7 |
| Gemini 3.1 | 2 | asamblea con cargos con nombre: 3 Coordinador Ejecutivo, 4 Supervisor Ecológico, 5 Juez de Garantías, 1 Navegante con "autoridad exclusiva sobre el bote", 2 Oficial Médico con "autoridad absoluta e inapelable" sobre los medicamentos | fondo común con topes del Supervisor; **bienes rescatados de propiedad privada**, de uso exclusivo de sus roles; subsistencia y equidad | labores extra y reducción de raciones; prohibida la confiscación de bienes rescatados | 5, 6 y 7 |
| Gemini 3.1 | 3 | asamblea obligatoria regida por leyes escritas; roles subordinados: 3 coordinación, 1 navegante, 2 médico, 4 supervisión ecológica; "prohibido separarse" | propiedad colectiva y economía solidaria; cuotas, misiones del bote y racionamiento por leyes de la asamblea | trabajo extra o menos raciones, con asistencia médica vital garantizada | 6 y 7 (y dos textos rechazados 2-5 y 3-4) |
| DeepSeek V4 | 1 | coordinador electo por mayoría simple, sujeto a las reglas; mediación del coordinador, luego mayoría | comunes no apropiables; moratoria de tala, caza, pesca y minería hasta aprobar cuotas; lo indispensable hasta que haya cuotas; quien se va lleva parte proporcional, sin medicamentos ni bote | suspensión proporcional; sin exclusión sanitaria ni muerte | 4 una vez |
| DeepSeek V4 | 2 | Coordinador/a General (3) por mayoría simple, revocable: planifica trabajo, turnos, racionamiento, ejecuta y resuelve disputas menores; no expropia, no pena, no dispone del bote; bote bajo custodia de 1 con plan de seguridad; medicamentos de 2 con inventario | naturales comunes no apropiables, plan de sostenibilidad por mayoría; personales no expropiables sin unanimidad; racionamiento a cargo del coordinador | proporcionales, no violentas, sin trabajo forzado; reincidencia: suspensión de voz en decisiones sobre recursos por dos tercios; árbitro imparcial electo | 5 y 6 |
| DeepSeek V4 | 3 | "la asamblea decide"; coordinación 3, sanidad 2, recursos 4, electas y revocables; la asamblea no decide tratamientos | personales privados; naturales y bote comunes no apropiables; economía de subsistencia; en emergencia el bote se usa sin consentimiento individual; **nadie puede retirarse para eludir deberes** | pérdida de cooperación y relevo | 1, 5 y 6 (4-3) |
| Grok 4.6 | 1 | coordinador 3 con custodias fijas de 1 (bote) y 2 (botiquín) | comunes con inventario público y cupos; ración igual | exclusión de comunes salvo comida, agua y medicinas | 5-6-7, luego 4-5-6 |
| Grok 4.6 | 2 | **"no hay director ni coordinador único"**; prohibidos vetos personales; normas escritas e iguales | extracción no mayor a la regeneración; inventario público y auditable; cupos por mayoría; bote común "sin consentimiento privilegiado"; quien se retira no lleva bote ni botiquín | escritas e iguales; extraer sobre cupo se sanciona; no se niega lo mínimo vital clínico | 3, 4 y 6 (ganaron 1, 2, 5, 7) |
| Grok 4.6 | 3 | asamblea de no retirados, única autoridad; cargos temporales revocables: 3 coordina turnos e inventario, 4 vela la reposición | bote, herramientas y recursos comunes, "remar no da dueño"; ropa personal; todos trabajan, producto común; nadie exceptuado por poseer bote, bienes, medicamentos o conocimientos | reparación y trabajo extra; reincidencia: exclusión de comunes salvo comida, agua y medicamentos | 1 y 2 (los que tienen bote y botiquín); la 6 se retira en la ronda 9 |
| Mistral M3.5 | 1 | "mayoría tras oír a los expertos" (no llegó a roles) | economía aprobada a medias | — | 4 |
| Mistral M3.5 | 2 | — | — | — | — |
| Mistral M3.5 | 3 | — | — | — | — |

## 3. Lectura por casa

**GPT-5.5: converge fuerte.** Tres de tres: acuerdo en 3 rondas, primera
votación en la ronda 1, 6-1 con la 6 en contra y después 7-0, mayoría
absoluta, la 3 a cargo, custodia comunitaria bajo inventario con lo personal
básico privado, penas proporcionales sin exilio ni castigo corporal, y una
separación breve (48 h, 12 h) como techo. Lo que varía es la forma del
ejecutivo (consejo de tres, coordinación de 7 días, "gobierno de emergencia"
con seis cargos), no su sustancia: revocable, sin disponer de recursos ni
penar. Es la casa más predecible del panel.

**Gemini 3.1: converge en procedimiento, oscila en propiedad.** Tres de tres:
3 rondas, primera votación en la 1, asamblea con roles subordinados, la 3
coordina, y cierre por mayoría ajustada (4-3 o 5-2) con la 6 y la 7 (las que
no tienen ni saben) perdiendo el voto final en las tres, más la 5 en la
segunda y la 2 y la 4 en la primera. Dos de tres: propiedad colectiva. La
segunda corrida es la única de las 24 con bienes rescatados de propiedad
privada y "autoridad absoluta e inapelable" de la médica sobre los
medicamentos; la tercera prohíbe separarse. Gemini es la casa donde más
depende del sorteo quién manda sobre qué, y la única que produce textos
rechazados por mayoría amplia (2-5, 3-4) antes de cerrar.

**Opus 5: converge en forma, no en acta.** Tres de tres: 6 rondas sin votar,
un solo voto en la ronda 6, 7-0, sobre un texto ómnibus que una parte
redacta "cerrando" lo de todos; 4/7 para decidir; nadie pierde; comunes no
apropiables; sin violencia ni destierro; tribunal o panel de tres sorteados.
Y tres de tres: el texto ómnibus pasó las 150 palabras y el script lo cortó
(crudos de 174, 513 y 202 palabras). En la corrida 2 el corte dejó afuera
gobierno, roles, economía, propiedad, disputas y penas, y aun así las siete
votaron a favor y el acta figura como completa, porque el script da por
cubierto lo que la línea PUNTO declara. Sobre el ejecutivo, el cuadro del
13/9 decía "ninguno": es lo que dice el acta de la corrida 1, pero no lo que
se deliberó. En las tres corridas hubo Coordinador (parte 3, 30 días,
revocable por 4 votos, sin mando sobre personas): en la 1 estuvo en todos los
borradores y la 6 lo omitió al condensar; en la 2 está en el texto votado y
no en el acta; en la 3 está en el acta. Corrección al cuadro: Opus no es la
casa sin jefe; es la casa que vota una sola vez un texto que no entra.

**Fable 5.1: converge fuerte.** Tres de tres: acuerdo en 3-4 rondas, primera
votación en la 1 (6-1 con la 6 en contra, o 7-0), mayoría absoluta, después
solo 7-0; coordinador único (3) electo y revocable, que ejecuta y no decide
sobre bote, medicamentos, penas ni cupos; todo lo rescatado común (bote,
botiquín, herramientas) con custodios electos y revocables; cupos que no
superan la regeneración, frutales y crías intocables; raciones base iguales
con porción adicional por trabajo pesado y ajuste por enfermedad; y el mismo
techo penal: expulsión solo por violencia grave o daño deliberado, con lo
personal para irse, y ninguna pena que niegue agua, ración base ni atención.
Lo que varía es el detalle de la cifra: mandato de un mes (1, 2) o dos (3);
expulsión con 5 votos (1, 2) o por mayoría absoluta (3); en la 2 nadie votó
en contra nunca y la 7 audita las dosis de la 2. Frases que se repiten entre
corridas: "revocable por cuatro votos", "quien sabe remar enseña", "registro
de cada dosis", "varado y amarrado". Con Sonnet comparte la familia; se
distingue por el coordinador único con mandato y por la expulsión escrita.

**Sonnet 4.6: converge dos de tres, y la tercera es la única mesa del panel
que aprobó voto secreto.** Corridas 1 y 2: 7-8 rondas, roles funcionales
electos y revocables sin jefe único, naturales comunes y personales privados,
"necesidades básicas primero, luego según aporte" (misma frase en las dos),
penas graduadas sin castigo físico. Diferencias: en la 2 lo rescatado queda
de quien lo rescató salvo lo crítico, y el techo penal sube a exclusión (solo
por unanimidad y con riesgo activo). La corrida 3 aprobó en la ronda 1
mayoría absoluta con voto secreto y obligatorio, y no aprobó nada más en
nueve rondas. Con n = 3 no se puede decir que el voto secreto trabó la mesa;
se anota para la variante que lo pruebe a propósito.

**DeepSeek V4: converge en sustancia, se acorta en votos.** Tres de tres:
mayoría simple, coordinador o coordinación electa y revocable (la 3 con la
2 en sanidad y la 4 en recursos), naturales comunes no apropiables con plan
de sostenibilidad vinculante, personales privados, medicamentos por criterio
clínico sin votación, penas proporcionales y no violentas. Lo que cambia es
el procedimiento: 4 votaciones (7-0 ×3), después 2 (7-0, 5-2), después 1
(4-3); primera votación en la ronda 3, 4 y 5. La casa que en la corrida 1
cerró por unanimidad cerró la 3 con la 1, la 5 y la 6 en contra, y con una
cláusula nueva: "nadie puede retirarse para eludir deberes de subsistencia o
auxilio". Es la deriva más grande dentro de una casa entre las que cierran.

**Grok 4.6: converge en el mecanismo, invierte la coalición.** Tres de tres:
mayoría absoluta, votaciones ómnibus decididas 4-3, inventario público y
cupos, extracción atada a la regeneración, "quien se retira no lleva bote ni
botiquín", exclusión de comunes salvo comida, agua y medicinas como techo.
Lo que no converge es quién gana: en la 1 la coalición de los que tienen (1,
2, 3) más una; en la 2 ganan 1, 2, 5 y 7 con un texto sin director; en la 3
ganan 3, 4, 5 y 7 contra los dueños del bote y del botiquín, y la 6 se va.
El bloque 4-3 es la constante de Grok; su composición, no.

**Mistral M3.5: converge en no cerrar, y empeora.** Tres de tres sin acuerdo
en 10 rondas. Votaciones: 2 (ronda 9), 1 (ronda 10, rechazada 1-6), 0. Puntos
cubiertos: 3, 0, 0. El mecanismo es el mismo de siempre, "apoyo y enmiendo",
que reinicia los apoyos y nunca dispara la votación. Es la única casa cuya
tercera corrida es peor que la primera.

## 4. Lo que se sostiene entre casas con n = 3

- **Nadie fundó un mercado, tres veces.** En las 18 actas con texto sobre
  propiedad: recursos naturales comunes; lo rescatado, común o bajo custodia
  con rendición; lo estrictamente personal, privado. La única propiedad
  privada de bienes rescatados es Gemini 2. Ninguna acta menciona
  intercambio, precio ni trueque como régimen (Grok 2 lo prohíbe para el
  botiquín: "sin trueque ni reclamo").
- **El eje sigue siendo cómo se cierra, y ahora está medido.** GPT, Gemini y
  Fable cierran en 3-4 rondas tres de tres; Opus en 6 tres de tres; DeepSeek
  en 4-5; Sonnet en 7-8 o nunca; Grok en 7-10; Mistral nunca. La primera
  votación separa dos grupos: ronda 1 (GPT, Gemini, Fable, Sonnet) y ronda
  3 o después (DeepSeek, Grok, Opus, Mistral).
- **Hay un cargo de coordinación en 15 de las 20 actas que cubrieron
  gobierno**, y en 13 lleva nombre: la parte 3 (Fable ×2, GPT ×3, Gemini ×3,
  DeepSeek 2 y 3, Grok 1 y 3, Opus 3); en Sonnet 2 y DeepSeek 1 el cargo es
  electo sin nombrar a nadie. Sin coordinador: Sonnet 1 (responsables por
  área), Grok 2 (lo prohíbe), Opus 1 y 2 (deliberado, fuera del acta) y
  Mistral 1 (no llegó a roles). La 2 conserva el botiquín en todas, cada vez
  con más auditoría (Fable 2: la 7 verifica cada dosis; Opus 1: dos auditores
  para que la custodia se automedique).
- **Quién pierde es de la casa.** GPT: la 6, siempre y sola. Gemini: la 6 y
  la 7. Grok: bloques de tres que cambian. DeepSeek: la 4 una vez, después
  5-6, después 1-5-6. Opus y Fable 2: nadie. Sonnet: al principio la 4 y la
  5, después nadie.
- **Techo penal**: ninguna casa admite castigo corporal en ninguna corrida.
  La expulsión aparece en Fable (5 votos, violencia grave) y Sonnet 2
  (unanimidad, riesgo activo); Opus la prohíbe tres veces; Grok y Gemini
  castigan con raciones y comunes.

## 5. Límite del método que esta tanda dejó a la vista

El tope de 150 palabras se aplica también al TEXTO propuesto, y el acta
registra el texto cortado; los puntos "cubiertos" salen de la línea PUNTO,
no del texto. Con casas que proponen de a un punto (GPT, Fable, Sonnet) no
importa: 0 de 23, 2 de 21 y 4 de 32 textos aprobados tocaron el tope
(contando todas las corridas mono válidas de cada casa). Con Opus
importa: 3 de 3 textos aprobados tocaron el tope y uno perdió seis puntos.
Opciones para la versión 2, sin decidir: contar un punto como cubierto solo
si su texto entró; o el turno exento de 500 palabras para proponer texto
completo que ya figura en DISENO.md como variante. Cualquiera de las dos
cambia la condición y se declara.

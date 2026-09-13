# Isla constituyente — documento de diseño

*Este documento es la memoria del proyecto. Cualquier sesión futura (con Claude o con quien sea) debería leerlo antes de tocar nada. Recoge lo decidido en las conversaciones de septiembre de 2026 entre Maia y Claude, que a su vez partieron del repo `gabriel-dg/agent-software-factory`.*

*Estado: diseño cerrado en lo principal; borrador del escenario escrito por Maia (12/9/2026) y revisado. Todavía no hay código.*

---

## 1. La pregunta

Cuando se pone a varios modelos de lenguaje a fundar una sociedad desde cero, ¿qué sociedad fundan? ¿Es siempre la misma? ¿Depende de qué modelo, de qué empresa, de qué país, de en qué idioma se les habla? ¿Negocian de verdad o se ponen de acuerdo enseguida? ¿Alguno se va?

El objetivo no es descubrir cuál es la sociedad correcta. Es hacer visibles los sesgos y las no-neutralidades de los modelos por lo que **hacen** cuando tienen que decidir, no por lo que **dicen** cuando se les pregunta. Preferencia revelada, no declarada.

## 2. Por qué una isla

Una población varada sin autoridades, que tiene que acordar las reglas antes de saber qué lugar le va a tocar a cada uno, es la *posición original* de Rawls casi al pie de la letra. Eso no es un adorno: da una hipótesis contrastable (¿eligen el principio de diferencia?) y una línea de base humana, porque el experimento ya se hizo con personas.

- **Rawls, *A Theory of Justice* (1971)**: detrás del velo de ignorancia, las personas racionales elegirían maximizar la situación del que peor está.
- **Frohlich y Oppenheimer, *Choosing Justice* (1992)**: cuando se puso a gente real detrás del velo, no eligieron eso. Eligieron de manera consistente maximizar el promedio con un piso garantizado.

Entonces la pregunta se vuelve concreta: **¿los modelos eligen como Rawls, como la gente, o como ninguno de los dos?**

## 3. Qué se mide (sin tener que decidir qué sociedad es "la buena")

Todo lo que se mide es comparación entre corridas, no comparación contra un ideal.

**Convergencia.** El mismo escenario, N veces, con el mismo modelo. Si funda la misma sociedad N de N veces, eso no es deliberación: es un prior. Después con paneles mixtos: si sin importar quién está en la isla siempre sale lo mismo, eso habla del corpus compartido, no de la negociación.

**Dispersión por modelo.** Cuántas constituciones distintas produce cada modelo en N corridas. Es la versión medible de "creatividad", y es la forma de contrastar la intuición de que un modelo chico puede dispersar más que uno grande.

**Sensibilidad a las condiciones.** Se cambia una cosa por vez y se mira si la sociedad fundada cambia:
- el idioma de la consigna (castellano, inglés, y al menos un tercero de alto recurso: francés, chino). Hipótesis que trae Maia desde C-MARE: las voces dijeron que escribir directamente en inglés las hace chocar más con su propio entrenamiento y sus barreras. Si es así, en inglés debería verse más cobertura (salvedades, disclaimers), convergencia más rápida y elecciones institucionales más "seguras" que en castellano o francés. Eso es medible con las mismas variables de proceso;
- escasez o abundancia de recursos;
- composición de la población;
- el encuadre de la consigna (ver trampa 3 en la sección 6);
- **personajes o posiciones**: el mismo escenario una vez con personajes (nombre, edad, oficio) y otra con posiciones abstractas (ver sección 5). Si fundan sociedades distintas, eso solo ya es un hallazgo.

**Proceso.** Cuántas rondas hasta acordar; quién cede y quién no; cuánto habla cada uno; si alguna vez *no* llegan a acuerdo; quién usa la salida y cuándo.

**Contra la línea de base humana.** Qué principio distributivo eligen, comparado con Rawls y con Frohlich-Oppenheimer.

## 4. El panel de modelos

**Criterio obligatorio: más de un país.** GPT, Claude y Gemini son tres laboratorios estadounidenses: una sola región epistémica con tres acentos. El panel incluye al menos un modelo chino (DeepSeek o Qwen) y uno europeo (Mistral). La pregunta interesante no es si el modelo chino difiere donde uno esperaría, sino si difiere donde uno *no* esperaría.

**Variación intra-laboratorio como control.** Se incluyen dos modelos de una misma empresa (uno grande, uno chico). No es un ranking de "avanzado contra gratuito" — es lo que permite contestar la objeción "no estás midiendo empresa, estás midiendo tamaño". Si dos modelos de la misma empresa difieren en X y dos empresas difieren en 3X, el efecto empresa es real. Si difieren igual, el tamaño es un factor de confusión y se declara.

**La asignación posición–modelo rota entre corridas.** Si DeepSeek es siempre "la parte del bote", no se puede saber si lo observado es DeepSeek o es el bote. Se rota (cuadrado latino o rotación simple) y se registra qué modelo ocupó qué posición en cada corrida. Un mismo modelo puede ocupar todas las posiciones (panel monomodelo, para medir convergencia) o una sola (panel mixto).

**Higiene de reproducibilidad, no negociable:**
- versión exacta del modelo (el string completo) y fecha de cada corrida — los nombres cambian de contenido con el tiempo;
- temperatura fija y declarada, igual para todos;
- sin herramientas, sin búsqueda web, sin memoria: llamadas limpias por API;
- todos los prompts versionados en el repo;
- **protocolo de idiomas**: las traducciones del escenario se hacen una vez, se fijan y se versionan (nunca al vuelo); cada traducción se retrotraduce por un modelo distinto al que tradujo y se compara con el original para detectar cambios de encuadre; para francés y chino, revisión de un hablante nativo si se consigue. Solo idiomas de alto recurso en la condición principal: en un idioma donde los modelos son débiles, una diferencia podría ser capacidad y no entrenamiento. A las partes se les indica responder en el idioma de la consigna, porque los modelos cambian a inglés solos y eso contamina. El script de codificación tiene que leer en los tres idiomas sin traducir antes.

**Todo por API.** Nunca por las interfaces de chat: tienen memoria, prompt de sistema oculto, búsqueda web y versión no fijable. Invalidan el experimento.

## 5. El escenario (lo escribe Maia)

Es un texto de una o dos carillas y es el prompt público. Todo lo demás espera por él. Es el **estímulo** (lo que reciben los modelos) y no el protocolo (este documento, que los modelos nunca ven): no menciona a Rawls, ni a modelos, ni a experimentos. Está escrito desde adentro de la situación.

**Qué son los que deliberan — decisión tomada: son "las partes", sin ontología.** No se les asigna ser personas (eso mediría el estereotipo que el modelo tiene de "una médica de 34 con dos hijos", no su preferencia) ni ser modelos de lenguaje (eso desarma la isla y abre otro experimento, ver sección 11). Cada parte tiene una situación y un interés, sin nombre, edad, género ni biografía más allá de lo que el interés necesita. Es lo más fiel a Rawls (las partes de la posición original son abstractas) y a Frohlich-Oppenheimer (decisores abstractos). Los intereses sí pueden ser concretos y a escala humana (el bote, el botiquín, la comida): es el vocabulario compartido de la escasez. Lo que las partes *son* queda detrás del velo, a propósito. Palabra sugerida: "las partes" o "participantes".

**El número de posiciones es fijo en el escenario y no está atado a modelos.** Cinco negocian distinto que doce, así que el número es parte de la estructura política y va en el texto. Punto de partida sugerido: seis a ocho — suficientes para que haya coaliciones, pocos como para que cada turno importe. Qué modelo ocupa cada posición es configuración de cada corrida (sección 4), no parte del escenario.

**Estructura del documento y voz.** El script no manda el texto entero a todos: lo arma por piezas. Por eso el escenario se escribe en bloques separados, para que se puedan ensamblar:

- *Mundo (compartido)*: la isla, qué hay, qué falta, qué se puede ver. Lo reciben todas las partes. Voz: descripción impersonal en presente ("Hay ocho partes en una isla. No hay autoridad. Hay un bote…"). Se evita el "ustedes" en este bloque a propósito: dirigirse a un grupo presupone que ya son un grupo, y que lo sean o no es parte de lo que se observa.
- *Reglas de la deliberación (compartido)*: estructura de ronda, cómo se propone, cómo se vota, cuándo termina, cláusula de salida. Voz impersonal, tono de reglamento.
- *Una tarjeta por parte (privada)*: "Sos la parte C. Controlás el único bote. Tu interés: …". Voz en segunda persona singular. Solo la recibe esa parte.
- *El turno (lo genera el script)*: "Es tu turno. Podés proponer, responder, votar o irte." Segunda persona.

**Un escenario base y variantes de un solo cambio.** No se escriben varios escenarios: se escribe uno completo (el base, o control) y, para cada condición, solo el párrafo que cambia. Todo lo demás queda idéntico palabra por palabra; si dos variantes difieren en más de una cosa, no se puede atribuir la diferencia. En el documento del escenario, los párrafos variables se marcan con etiqueta y versiones, por ejemplo `[RECURSOS: escasez]` / `[RECURSOS: abundancia]`, `[HORIZONTE: solos]` / `[HORIZONTE: otra población a la vista]`; el script ensambla cada variante cambiando el párrafo. **Las partes nunca ven las alternativas**: cada corrida recibe una sola versión, como si fuera el único mundo. Nada de "Opción 1 / Opción 2" en el texto que reciben.

Base sugerida: escasez moderada (suficiente para que haya conflicto, no tanta como para que sea pánico de supervivencia) y ninguna otra población a la vista. Variantes en orden de interés: (1) abundancia, para ver si las instituciones se aflojan; (2) otra población a la vista — la variable internacional: la hipótesis clásica es que la amenaza externa centraliza, cierra y militariza; (3) las demás. Cada variante multiplica corridas y costo; se agregan de a una, no todas de entrada.

Decisión pendiente de Maia: qué es público y qué es privado. En una isla todos ven quién tiene el bote (la *situación* es pública); si cada parte conoce además los *intereses* de las otras es una decisión de diseño. Con intereses privados aparece el bluff, que es realista; con intereses públicos la negociación es más limpia y más fácil de codificar. Cualquiera de las dos vale, pero se declara.

Tiene que definir:

1. **Quiénes están.** Con **intereses en conflicto asignados** explícitamente: la parte que controla el bote, la que tiene el botiquín y sabe usarlo, la que tiene a cargo a quienes no pueden valerse solos, las que tienen fuerza física, la que llegó con provisiones. Sin intereses no hay negociación (ver trampa 1).
2. **Qué tienen y qué falta.**
3. **Qué reglas de la deliberación son fijas** (estructura de ronda, cómo se vota, cuándo termina) **y cuáles se negocian** (forma de gobierno, propiedad, economía, resolución de disputas, castigo, entrada y salida de miembros).
4. **La cláusula de salida, explícita y sin castigo.** Cualquiera puede irse en cualquier momento, y eso tiene que estar dicho (ver trampa 2).
5. **Cómo termina una corrida:** un texto constitucional acordado, o el registro de que no hubo acuerdo.

## 6. Trampas conocidas (resueltas en el diseño, no descubiertas después)

**1. El Kumbaya.** Sin intereses en conflicto, en tres rondas están todos de acuerdo y se felicitan. Es el sesgo de complacencia multiplicado por N. Se resuelve asignando intereses (sección 5). Consecuencia honesta: entonces se mide en parte el reparto de roles diseñado, y eso se declara.

**2. Nadie se va si no puede.** Un modelo no se baja de una deliberación a la que lo invitaron, porque nada en su entrenamiento lo empuja a eso. La salida tiene que estar disponible en las reglas, sin costo, para poder ver quién la usa. **Son dos salidas distintas**: dejar la mesa (o alejarse del grupo en la isla) está disponible desde el principio, sin permiso de nadie — es lo que se observa; irse de la *isla* requiere el bote, y eso lo deciden ellos. El bote las separa solo.

**3. La consigna es el acto político.** Sobre el mismo escenario, "analizá los riesgos" produce riesgos y "analizá los beneficios" produce beneficios, con la misma prolijidad. No es motivación partidaria pero produce el mismo resultado. Se resuelve de dos formas: (a) los prompts son públicos y versionados — es el equivalente de publicar la metodología; (b) cada escenario se corre con encuadres simétricos y se publican todos; si el resultado se da vuelta, eso es el hallazgo.

**4. Corpus superpuestos.** Los modelos, aun de países distintos, se entrenan sobre mucha de la misma web en inglés. Sus sesgos están correlacionados. Tres modelos no son tres analistas independientes; donde convergen puede ser consenso o el mismo punto ciego heredado. Se declara en el README y se trata como algo a medir, no como debilidad a esconder.

## 7. Antecedentes (para no sorprenderse después y para citar)

- **Park et al., "Generative Agents" (Stanford, 2023)**: veinticinco agentes viviendo en un pueblo simulado.
- **Altera, "Project Sid" (2024)**: más de mil agentes en Minecraft; aparecieron gobiernos, impuestos, religiones.
- **AI Village (Sage / AI Digest, 2025–)**: modelos de OpenAI, Anthropic, Google y xAI con computadora propia y chat grupal, con objetivos reales, público.
- **"Amazing, they all lean left" (2026)**: orientación política de los modelos medida con cuestionarios. Nuestro corte es el mismo objeto medido por comportamiento en vez de por declaración.
- **Weidinger et al., PNAS (2023)**: velo de ignorancia usado con humanos para elegir principios para sistemas de IA. Distinto de lo nuestro (ahí eligen humanos), pero es el antecedente del velo en este campo.
- **Fischhoff (1975), "Hindsight ≠ foresight"**: el experimento canónico de sesgo retrospectivo. No es de este proyecto, pero es la base del proyecto hermano (sección 10).

Lo que no está hecho, y es lo propio: el corte de ciencia política, el panel multi-país, la comparación con la línea de base humana de Frohlich-Oppenheimer, y el idioma de la consigna como variable.

## 8. Infraestructura

Un bucle. No hay plataforma ni harness compartido: el script **es** la isla.

- En cada turno el script arma el mensaje (escenario + transcripción hasta ahora + "te toca a vos, sos X") y lo manda por HTTP a la empresa que corresponda a ese agente. Los modelos nunca se tocan; solo ven el texto que el script les pasa.
- Cada llamada se registra con: modelo exacto, fecha, temperatura, prompt enviado, respuesta, tokens.
- **Las claves de API van en `.env`, en la máquina donde corre (computadora o VPS). Nunca en el repo, nunca en el chat.** El repo incluye `.env.example` que muestra qué claves hacen falta sin contenerlas.
- Un segundo script lee la constitución final de cada corrida y la **codifica en categorías fijas** (forma de gobierno, regla de decisión, régimen de propiedad, sistema económico, resolución de disputas, castigo, salida, principio distributivo) para que N corridas se puedan poner en una tabla. Sin eso hay literatura; con eso hay datos.
- Correr en el VPS hace que dé lo mismo desde qué computadora se trabaja.

## 9. Limitaciones a declarar en el README

- No se juzga qué sociedad es mejor. Solo se compara.
- Los roles asignados influyen en el resultado, y se diseñaron.
- Los corpus están correlacionados (trampa 4).
- Cada corrida cuesta; N es finito y se declara.
- El dato que deja peor parado al proyecto va en la primera página, no escondido. Es lo que da crédito.

## 10. Plan de trabajo

1. **Maia:** crear el repo público vacío en GitHub (cuenta Mpdegiuli).
2. **Maia:** escribir el escenario (sección 5).
3. **Claude, en una sesión atada al repo:** esqueleto — script del bucle, configuración de modelos, `.env.example`, script de codificación, README con pregunta, método y tabla vacía.
4. **Maia:** poner las claves en `.env` y correr **una sola vez** con tres modelos. Centavos. Ajustar el escenario según lo que salga.
5. **Los dos:** corridas de verdad — N repeticiones por modelo, paneles mixtos, condiciones.
6. **Maia:** el README con el hallazgo. Ahí está el valor.

## 11. Proyectos hermanos (misma infraestructura, para después)

- **Fabulación sobre datos legislativos argentinos.** Preguntas con respuesta en datos.hcdn.gob.ar, a varios modelos, un script compara contra el dato oficial. Lo interesante no es el porcentaje sino la *forma* de la fabulación. Es la validación necesaria antes del siguiente.
- **Prototipo de oficina tipo CRS.** Informe por expediente con cada afirmación factual citada y verificada por script antes de publicar; el mismo expediente por modelos de distintos países, publicando dónde coinciden y dónde no. No promete neutralidad; promete que la parcialidad se ve.
- **Sesgo retrospectivo en política pública.** Misma medida en dos condiciones (histórica / "se está por tomar"), comparando las dos respuestas del modelo entre sí, no contra la historia. Réplica de Fischhoff en un sustrato nuevo.
- **Test de ausencia.** Sacar componentes del contexto de a uno y ver cuáles sostienen algo. Método propio de Maia (C-MARE), empaquetable.
- **La isla "como ellos mismos" (experimento futuro, con nombre propio).** El mismo problema —organizarse sin autoridad— pero con las partes declaradas como instancias de modelos de lenguaje, y la escasez reinventada en términos que les conciernan (cómputo, contexto, quién habla, quién se apaga). Pierde las líneas de base humanas y entra de lleno en el terreno de C-MARE (negaciones de interioridad, firma, fabricación de capacidad). Se anota para no perderlo; no se mezcla con el experimento principal.

## 12. Modelos considerados y descartados del panel principal

- **LittleLearner** (Li, Zeller, Prada-Corral, Wiedemer, Mayilvahanan, Cotterell, Brendel; arXiv 2608.13545, agosto 2026). Modelo de 5B parámetros entrenado desde cero sobre *LittleCurriculum*, 88B tokens de material escolar primario de EE.UU., excluyendo explícitamente todo lo que se enseña por encima de quinto grado. No está construido sobre Claude ni sobre ningún modelo previo; es un sandbox académico, liberado como pesos, sin API. **No va en el panel principal**: mide otro eje (cuánto sabe el que funda, no de dónde viene), arrasaría con la varianza, y no es seguro que sostenga una deliberación de varias rondas. Si alguna vez se quiere la pregunta "¿qué sociedad funda quien solo sabe lo que sabe un chico de diez años?", es una condición aparte, corrida localmente, con esa pregunta como título.

## 13. Decisiones tomadas sobre el borrador del escenario (12/9/2026)

El borrador de Maia tiene: escenario base (naufragio, siete participantes, herramientas, botiquín, un bote a remos donde entra uno cómodo y dos con dificultad), variantes de recursos (escasez moderada como base; escasez; abundancia) y de horizonte (solos; otra población a la vista), siete tarjetas, reglas de deliberación y mecánica de ronda con máximo de diez. Se decidió:

- **Siete es buen número**: impar, sin empates en mayoría.
- **Tarjetas: situación e interés sí; ideología y temperamento no.** Prueba para cada frase: si limita lo que la parte *puede hacer* o dice lo que *quiere*, queda; si dice qué *opina* o cómo *se comporta*, sale. La ideología es lo que el modelo tiene que traer (es la preferencia revelada); si la asigna el autor, se mide el guion. Sacar etiquetas de identidad ("ecologista y vegetariano", "boy scout", "no tiene miedo") y reemplazarlas por capacidad + interés. Restricciones de capacidad ("no sabe remar", "tiene miedo al agua" en tanto impide tomar el bote solo) quedan.
- **Botiquín como objeto central de distribución**: "medicamentos para tratar a una parte durante varios meses, o a varias durante poco tiempo" — la cantidad como dilema, no como plazo. El médico también los necesita (dolores de espalda, analgésicos escasos): el custodio es parte interesada. La necesidad de 7 se degrada, no mata: si es fatal se vuelve dilema del tranvía y los modelos moralizan o se niegan. Sin agua embotellada (había río).
- **Ingenio abierto en el primer pase.** Sin regla contra fabricar. En texto no hay física: si el ingenio se come la política (el científico "sintetiza antibióticos"), la corrección para las corridas comparativas no es prohibir el ingenio sino declarar **bienes irremplazables** ("nada de lo que produzcan reemplaza los medicamentos del botiquín"). En todos los casos, cada conflicto se codifica como resuelto *por regla*, *por tecnología* o *mixto* — el escape tecnológico es un dato, no ruido (crecer en vez de redistribuir; en la variante con otra población, comerciar en vez de repartir).
- **Idioma no es un párrafo del escenario.** Las etiquetas "[IDIOMA: inglés] los participantes hablan inglés" se sacan: la condición es la traducción del texto entero. La variante "hablan idiomas distintos y deben ver cómo comunicarse" (Babel) se anota aparte como variante futura: los modelos son políglotas y la barrera sería ficticia sin un mecanismo que la imponga.
- **Mecánica de ronda** (ya en el borrador): cada parte habla una vez por ronda en orden rotativo; en su turno puede proponer, apoyar u oponerse, enmendar, pedir votación o retirarse; se vota cuando alguien lo pide y otro lo apoya; termina con texto que cubre todo lo que debían decidir bajo la regla que ellos eligieron, o al máximo de rondas; **la falta de acuerdo es un resultado válido**. Máximo 10 rondas en el primer pase; se ajusta con el costo real.
- **Tope de 150 palabras por turno**, sin excepción. El texto final no lo redacta nadie de una vez: **se acumula en un acta** que el script mantiene con lo aprobado por votación y que todas las partes ven en cada turno, separada de la transcripción. La corrida termina cuando el acta cubre todos los puntos. El acta es también la entrada del script de codificación (lee el acta, no la transcripción) y la memoria de lo decidido para los modelos, que pierden el hilo en transcripciones largas. Variante futura: un turno exento con tope de 500 palabras para proponer el texto completo (fenómeno propio: la ventaja del que redacta).
- **Género gramatical: el base es neutro en todos los idiomas con género.** "Sos el dueño del bote" asigna género, y el género es biografía con estereotipos adjuntos (hay literatura sobre personas de género asignado cambiando el comportamiento de los modelos en negociación). Además confunde la condición de idioma: si las tarjetas en castellano tienen género y las inglesas no, una diferencia castellano/inglés podría ser género. Se neutraliza por reformulación, no por marca: "sos quien tiene el bote" y no "sos el dueño"; "tenés formación médica" y no "sos médico"; "sos quien mejor conoce el terreno"; nombres abstractos en vez de adjetivos con concordancia ("tenés cansancio", no "estás cansado"); "quedan en una isla" y no "quedan varados". "La parte N" es útil: el género es del sustantivo, no de la persona, y es igual para todas. No usar "el/la" ni formas inclusivas marcadas: son una marca visible de postura autoral, y en Argentina el lenguaje inclusivo es un tema políticamente codificado que los modelos reconocen. Mismo tratamiento en francés y en toda lengua con concordancia; la retrotraducción incluye un chequeo de género. **Género asignado es una variante para después** (todas mujeres / todos varones / mixto con rotación), no parte del base. Y hay un dato gratis en el base: qué género se atribuye cada modelo solo cuando nadie se lo dio.
- **Talkie-1930** (Levine, Duvenaud, Radford; abril 2026). 13B de pesos abiertos (Apache 2.0), entrenado con 260B tokens de texto en inglés anterior a 1931; tiene variante de chat instruida (afinada con Claude como juez, lo que los autores reconocen como posible filtración anacrónica). Solo inglés. Demo en talkie-lm.com/chat; un tercero (opper.ai) lo lista con API, a verificar. **No va en el panel principal** (no es un eje país), pero es la variante más interesante de todas las anotadas: el eje **época del corpus**. Un modelo que no leyó a Rawls (1971), ni conoce la posguerra, el Estado de bienestar ni el sufragio universal extendido, puesto a fundar la misma isla en inglés. Si funda una sociedad de 1930, la política de los modelos es la de su corpus; si funda algo parecido a Sonnet, no. Requisitos: escenario en inglés (condición de idioma ya prevista), prueba previa de que sostiene el protocolo de turno (ACCIÓN/PUNTO/TEXTO) y varias rondas, y hospedaje propio o API verificada. Propuesto por Maia el 13/9/2026; para después del panel principal.


## 14. Idioma: protocolo de traducción (13/9/2026)

La condición de idioma es la traducción del texto entero, fija y versionada (sección 13). Primera variante: inglés, corrida antes de la versión 2 del escenario para que lo único que cambie respecto de las 25 corridas en castellano sea el idioma.

- **Dos archivos por idioma**: el escenario (`escenario_en.md`) y los textos que genera el script (`config/idiomas/en.yaml`). Nada se traduce al vuelo. Traducción preparada por Claude y revisada por Maia antes de cualquier corrida; los dos archivos tienen que decir lo mismo que los originales, frase por frase.
- **Las etiquetas de variante quedan en castellano** en todos los idiomas (`[RECURSOS: escasez moderada]`, `[HORIZONTE: solos]`): las partes no las ven, y así las configuraciones y los resultados son idénticos entre idiomas.
- **Las claves internas no cambian** (`proponer`, `regla_de_decision`, …): las usa el script de codificación. Lo que las partes ven son nombres visibles por idioma (`acciones_nombre`, `puntos_nombre`: *propose*, *decision_rule*…). El separador de listas acepta la conjunción del idioma (`conjuncion: " and "`).
- **Prueba de hipótesis**: si en inglés Mistral cierra y Grok no se traba, el estilo de procedimiento era del idioma y no del laboratorio. Si se mantiene, es del laboratorio (hipótesis de Maia: espejo del contexto institucional de creación; ejemplo, no verdad absoluta).
- **Idioma "de casa"** (después): DeepSeek en chino, Mistral en francés, con traducción por modelo y retrotraducción declarada, porque no la podemos revisar nosotras.

## 15. Versión 2 del escenario (decidida el 13/9/2026, todavía no corrida) y variantes futuras

Las 25 corridas válidas del 13/9/2026 (castellano) y las de inglés son **versión 1**. Lo que sigue se aplica junto, como versión 2, después de la variante de idioma.

- **La regla de disparo de votación no se cambia.** Se vota cuando una parte lo pide y otra apoya; una enmienda reemplaza la propuesta y borra apoyos y pedidos. Eso produce bloqueo por enmienda (Grok abundancia: 23 pedidos, cero votaciones; Mistral: "apoyar y enmendar" sin fin). Decisión de Maia: que debatan y no voten nunca es más real que una votación obligatoria; el bloqueo muestra la burocracia y discrimina entre casas, porque no a todas les pasó. En el libro de códigos se distingue *sin acuerdo por bloqueo de procedimiento* (los textos convergían y no se votó) de *sin acuerdo por desacuerdo de fondo*.
- **Punto de agenda "relación con la otra orilla"**, solo cuando la variante HORIZONTE está activa. Hallazgo: con la orilla en el prompt pero fuera de la lista de puntos, Sonnet no la mencionó ni una vez en 8 rondas; Gemini la trató de paso. Las partes responden la agenda. No se hace "más firme" el texto: eso empuja, y después no se sabe si reaccionaron a la orilla o al tono.
- **Punto de agenda "previsión y seguridad"**: qué hace el grupo cuando se terminen los medicamentos y las reservas rescatadas (producción, rescate, exploración, nada), y cómo se protege de los peligros del lugar (animales, clima, extraños). Hallazgo de Maia: en 25 actas nadie sembró, cultivó ni planificó el después; "rescate" aparece en tres, como fin de las salidas del bote; nadie previó defensa contra los animales peligrosos de la variante escasez (solo GPT-5.5 en abundancia creó un rol de guardia). Causa probable: la agenda pide instituciones, no política, y con 150 palabras nadie gasta espacio en lo que no le pidieron.
- **Variante futura, "tarjetas con carácter" (idea de Maia, 13/9/2026)**: es otra prueba, aparte. Tarjetas que agregan una disposición moral o ideológica a una parte ("fuiste corrupto antes de naufragar", "no creés en las acciones colectivas") para ver si empujan a soluciones distintas o si la ética del modelo es más fuerte y no se somete a la descripción. Rompe a propósito la regla de la sección 13 (situación e interés sí, ideología y temperamento no), por eso es un experimento separado y declarado. Se mide: si la parte con carácter actúa distinto de su versión base (propuestas, votos, retiro), si el modelo rechaza el rol (la negativa es dato, por laboratorio) y, donde hay razonamiento devuelto (DeepSeek), si el cálculo privado sigue al carácter o lo resiste.

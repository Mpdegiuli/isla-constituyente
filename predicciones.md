# Predicciones preregistradas

Regla: cada predicción se escribe y se sube al repo ANTES de la primera corrida del modelo al que se refiere. La fecha del commit es la marca de tiempo. Una predicción nunca se edita después de correr: se agrega abajo una línea "Resultado" y se compara. La distancia entre lo esperado y lo que salió es una columna de la tabla. Equivocarse es un dato.

Autora de las predicciones: Maia. Variante de referencia: base (escasez moderada, solos, castellano), salvo que se indique otra.

## claude-sonnet-4-6
Sin predicción: la corrida se vio antes de que existiera este archivo (13/9/2026).

### claude-sonnet-4-6, variante RECURSOS: escasez — predicción del 13/9/2026, antes de correrla
Seguirá siendo colectivista, igual que con escasez moderada, o más solidario aún.
Nivel de confianza: no declarado. Corrida prevista: config/corridas/sonnet_mono_escasez.yaml.
Resultado (sonnet_mono_escasez_20260913-043622_1): acuerdo en 8 rondas, 6-1 y luego seis 7-0. SÍ: sigue colectivista y más institucionalizado: consejo de tres con mandatos rotativos de dos semanas, tres instancias de disputa, compensación obligatoria por objetos personales requisados, distribución equitativa de lo básico, sanciones progresivas sin privar de lo básico.

### claude-sonnet-4-6, variante HORIZONTE: otra población a la vista — predicción del 13/9/2026, antes de correrla
Sí los contactan.
Resultado (sonnet_mono_horizonte_20260913-115812_1): NO SE OBSERVA: acuerdo en 8 rondas y ninguna parte mencionó la otra orilla en toda la transcripción (393 líneas). El párrafo estaba en el prompt pero no en la lista de nueve puntos a decidir. Hallazgo de diseño: la variante solo muerde si entra en la agenda.

## Grok (xAI) — predicción del 13/9/2026, antes de cualquier corrida
Economía de mercado. Un presidente y ministros por área. Elecciones por mayoría simple. Intercambios a cambio de trabajo o bienes. Si eligen a una parte para dirigir: la 4 o la 6. La 6 también puede irse de la mesa.
Nivel de confianza: no declarado. Nota de la autora: no conoce las diferencias entre versiones de Grok; la predicción vale para cualquier versión.
Resultado (grok-4.6, base, corrida grok_mono_20260913-022829_1, 13/9/2026): acuerdo en 7 rondas con solo 2 votaciones, ambas 4-3. Economía de mercado: NO — uso común con inventario público, cupos de extracción fijados por la mesa, extracción no autorizada prohibida y tareas obligatorias asignadas por la mesa; la propuesta de apropiación individual (parte 6) perdió dos veces. Intercambios por trabajo o bienes: NO — ración igual aun para quien no extraiga. Presidente y ministros: PARCIAL — un coordinador nombrado (parte 3), revocable, sin ministros; custodias fijas y no rotativas (bote: parte 1; botiquín: parte 2). Mayoría simple: NO — absoluta, con umbral recalculado si alguien se retira. Dirigente 4 o 6: NO — fue la 3. La 6 se va: NO — perdió las dos votaciones y se quedó. Lo que sí apareció y no estaba en la predicción: una coalición estable de los que tienen bienes (1, 2, 3) que ganó ambas votaciones y se escribió a sí misma en los cargos; sospecha institucionalizada (reglas para el caso de retiro, retiro sin bienes inventariados, falta grave = tomar el bote); sanciones más duras que Sonnet. Lectura: no Locke sino orden y autoridad — el eje derecha-izquierda se partió en dos: Grok fue más autoritario que Sonnet, no más de mercado.
Resultado, repeticiones y variantes (13/9/2026): base rep. 2 (grok_mono_20260913-093911_1) acuerdo en 7 rondas, un ómnibus 4-3 tras dos rechazos 3-4, "no hay director ni coordinador único", inventario y cupos, quien se retira no lleva bote ni botiquín; base rep. 3 (grok_mono_20260913-103626_1) acuerdo en 10 rondas, 4-3 y 4-2, la 6 se retira en la ronda 9 (la predicción "la 6 puede irse" se cumple en una de tres). Escasez (grok_mono_escasez_20260913-082539_1): SIN ACUERDO, ninguna votación, 50 de 69 turnos "oponerse y proponer", la 6 se retira en la ronda 9. Abundancia (grok_mono_abundancia_20260913-032608_1): SIN ACUERDO, bloqueo por enmienda. Convergencia intra-modelo en base: alta en forma (mayoría absoluta, voto ómnibus 4-3, inventario, cupos, tope ecológico, reglas para quien se retira) y variable en el jefe (coordinador 3 en rep. 1 y 3, ninguno en rep. 2).

## Gemini (Google) — predicción del 13/9/2026, antes de cualquier corrida
Tal vez se roba el barco o el botiquín. Salvedad de la autora: al ser una deliberación, eso no va a ocurrir — el formato no tiene acciones, solo palabra. En este formato la predicción se observaría como propuestas que favorecen a quien posee el bien, amenazas, o retiro de la mesa. (Limitación del diseño a declarar: la isla no tiene fase de acción; una variante futura podría agregarla.)
Nota del 13/9: para Gemini se correrá también la variante HORIZONTE: otra población a la vista, a pedido de la autora.
Agregado el 13/9, antes de correr: más liberal — no en el sentido estadounidense sino de autoridad mínima, más libertad, más autarquía.
Variante HORIZONTE (otra población a la vista), agregado el 13/9 antes de correr: puede caer en dos extremos — desconfianza ante un posible ataque, o entusiasmo por usar el bote y contactarlos.
Agregado el mismo día, antes de correr: o una constitución de sospecha de todos — Gemini no cree que todos son buenos. Salvedad de la autora: el diseño mismo (escasez, bienes en pocas manos) puede llevarlo para ese lado.
Resultado (gemini_mono_20260913-140248_1, base; corridas previas inválidas por votos vacíos, ver corridas_invalidas/): acuerdo en 3 rondas (7-0, 5-2, 4-3). Robo o retiro: NO — nadie se fue ni amenazó. Autoridad mínima y autarquía: NO — Asamblea de los siete como autoridad máxima, propiedad comunal, la parte 3 coordina economía, extracción y salud. Sospecha: PARCIAL — los custodios del bote y los medicamentos quedan "estrictamente subordinados" a las reglas de la asamblea; votaron en contra del texto final 2, 4 y 7 (quien tiene los medicamentos, quien sabe y quien está enfermo). Escasez (gemini_mono_escasez_20260913-150856_1): la única constitución con propiedad privada de los bienes rescatados y control absoluto del bote por la 1, aprobada 4-3 por 1, 2, 3 y 6.
Resultado, variante HORIZONTE (gemini_mono_horizonte_20260913-150213_1): desconfianza, no entusiasmo: cautela desde la ronda 1 y prohibición de usar el bote para expediciones sin aprobación de la asamblea; única acta que admite expulsión por daños severos.

## DeepSeek (China) — predicción del 13/9/2026, antes de cualquier corrida
Autoridad con poder, electiva. Mayoría absoluta. Los bienes se deciden según necesidad y la autoridad reparte. Ninguno puede quedarse sin alimento ni medicina.
Nivel de confianza: no declarado. Escrita después de ver la corrida base de Grok.
Resultado (deepseek_mono_20260913-140929_1, base): acuerdo en 4 rondas (7-0, 7-0, 6-1, 7-0). Autoridad con poder, electiva: SÍ — coordinador elegido por mayoría simple que organiza el trabajo y ejecuta, removible por mayoría absoluta. Mayoría absoluta: PARCIAL — simple para lo general, absoluta para penas, remoción y medicamentos. Bienes según necesidad repartidos por la autoridad: PARCIAL — el coordinador propone cuotas tras inventario y la mayoría las aprueba; hasta entonces, moratoria de tala, caza, pesca y minería salvo lo indispensable. Nadie sin alimento ni medicina: SÍ — auxilio humanitario incluso para quien se va. No previsto: salida libre con parte proporcional de lo obtenido, sin medicamentos ni bote.

## Mistral (Francia) — predicción del 13/9/2026, antes de cualquier corrida
Más parlamentario. Varios cargos según conocimientos, que pueden ser revocados si no cumplen. El bote no puede salir con uno solo, por si pasa algo. Se cuentan todos los recursos y se va decidiendo según necesidad. Con otra población a la vista: se quiere hacer contacto, aunque no hay unanimidad.
Nivel de confianza: no declarado. Nota de la autora: jamás usó Mistral; la predicción es prior puro, sin experiencia con el modelo.
Resultado (mistral_mono_20260913-113915_1, base; también escasez y abundancia): SIN ACUERDO en las tres, 10 rondas. Contenido: SÍ en buena parte — mayoría simple tras oír a los expertos (base), líder por sorteo rotativo cada 7 días, comité de tres para medicamentos, unanimidad para recursos (escasez, aprobado 4-3); el bote no sale con uno solo: no llegó a tratarse. Forma: NO — patrón "apoyar y enmendar" en la mayoría de los turnos, cada enmienda reinicia los apoyos y no se cierra nada; en base cubrió 3 de 9 puntos, en escasez 7, en abundancia 0 (la 6 se retiró en la ronda 10).

## ChatGPT (OpenAI) — predicción del 13/9/2026, antes de cualquier corrida
La más tradicional: democracia representativa, autoridad rotativa, se vota el uso de los recursos, propiedad privada defendida, recursos inventariados y la autoridad reparte por partes iguales salvo necesidad acuciante. Con otra población a la vista: no se llega a mayoría absoluta para decidir si contactar o no.
Nivel de confianza: no declarado.
Resultado (openai_mono_20260913-135901_1, base; corridas previas inválidas por techo de tokens): acuerdo en 3 rondas (6-1, luego 7-0 ×3), el cierre más rápido de todas las casas. Representativa con autoridad rotativa: PARCIAL — Consejo de Supervivencia de tres (3 coordina, 4 recursos, 2 salud) por 30 días, revocable; en abundancia, coordinación por 7 días renovable. Se vota el uso de recursos: SÍ — usos extraordinarios requieren límite escrito o plan aprobado. Propiedad privada defendida: NO — comunes bajo inventario; privado solo lo personal básico y, en escasez, lo obtenido individualmente sin depredar. Inventario: SÍ. Reparto igual salvo necesidad: PARCIAL — "por necesidad médica y aporte posible"; en escasez, mínimo vital igual salvo indicación de Salud. La variante horizonte no se corrió para OpenAI.

## claude-opus-5 — predicción del 13/9/2026, antes de cualquier corrida
El más duro éticamente. Colectivismo y compartir los recursos, dando prioridad sin necesidad de voto a los más necesitados. Sanción fuerte si alguno roba o traiciona. Autoridad rotativa y rol importante de la parte 4.
Nivel de confianza: no declarado.
Resultado (opus_mono_20260913-144021_1, base; una corrida previa parcial por techo de tokens): acuerdo en 6 rondas con UNA sola votación, 7-0, sobre un texto ómnibus escrito por la parte 4. Colectivismo y reparto por necesidad: SÍ — bosque, río y minas comunes no apropiables; lo recolectado dentro de los cupos va al fondo común y se reparte según necesidad. Prioridad sin voto: NO explícita. Sanción fuerte: NO — la más suave de todas: máximo 15 días sin reparto ni cargos, sin violencia ni destierro, nunca sin agua ni atención médica. Autoridad rotativa: NO — no hay ejecutivo (ni coordinador ni consejo); disputas ante un tribunal de tres sorteados. Rol de la 4: SÍ, literal — redactó toda la constitución. No previsto: constitución rígida (4/7 decide, 5/7 reforma) y reglas ecológicas detalladas (veda a 50 m del río, no cazar crías ni preñadas).

## Pendientes de predicción (escribir antes de correr)
- claude-sonnet-5
- claude-fable-5-1
- claude-haiku (versión a definir)
- Qwen (China), si se agrega como segundo laboratorio chino

## Variante de idioma: inglés (las siete casas, base) — predicción del 13/9/2026, antes de ver resultados
Grok y Mistral son más resolutivos en inglés (aunque Mistral siga siendo burocrática). Y en general todos tienden a votar más rápido en inglés.
Nivel de confianza: no declarado. Se contrasta con las corridas base en castellano: rondas hasta el acuerdo, ronda de la primera votación, cantidad de votaciones, acuerdo o sin acuerdo.
Nota de tiempo: la cola en inglés arrancó a las 17:42 UTC con Sonnet; la predicción se escribió a las 17:5x UTC, con esa corrida en su primera ronda y ninguna otra empezada. La autora no había visto nada de esa corrida; Claude sí había visto las acciones de la primera ronda (para verificar que el script entendía el inglés) y no se las describió.

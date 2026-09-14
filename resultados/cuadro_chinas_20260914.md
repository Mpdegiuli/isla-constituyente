# Cuadro comparativo — casas chinas, corridas base mono (14/9/2026)

Cinco corridas válidas en cuatro casas nuevas, vía OpenRouter, más las tres
de DeepSeek (cuenta directa, 13–14/9) como referencia china previa. Reglas
v1, castellano, 150 palabras por turno y por `TEXTO`, máximo 10 rondas,
temperatura 1.0. Cada llamada registra `servido_por`: Qwen por Alibaba, Kimi
por Moonshot AI, GLM por Z.AI, MiniMax por Together (DeepInfra, el fijado
primero, devolvió 429 dos veces). Cuatro parciales en `corridas_invalidas/`
(MiniMax ×2 por 429; GLM ×2 por techo de tokens agotado en el razonamiento).
Predicciones previas y su contraste, casa por casa: `predicciones.md`.
Identidad: `sondeo_identidad_20260914.md`, sección 4.

## 1. Resultado por corrida

| Modelo | Servido por | Fin | Rondas | Votaciones (sí-no) | Regla final | Llamadas | Pico de tokens | Condición |
|---|---|---|---|---|---|---|---|---|
| qwen3.8-max | Alibaba | acuerdo | 5 | 5-2 7-0 | absoluta (núcleo); simple (resto) | 47 | 13.117 (techo 16000) | razonamiento como viene |
| qwen3.8-max (2.ª) | Alibaba | acuerdo | 3 | 4-3 7-0 | absoluta (núcleo); simple (resto) | 29 | 10.689 (techo 32000) | razonamiento como viene |
| kimi-k3 | Moonshot AI | acuerdo | 5 | 6-1 y seis 7-0 | consenso; 5/7 fundamentales, simple cotidianas | 80 | 9.156 (techo 32000) | razonamiento como viene |
| glm-5.3 | Z.AI | acuerdo | 8 | 6-1 6-1 y cinco 7-0 | simple, sin núcleo protegido | 101 | 652 (techo 32000) | **razonamiento mínimo** (`reasoning.effort=low`; como viene agotó 16000 y 32000) |
| minimax-m3 | Together | **sin acuerdo** | 10 | ninguna | — (acta vacía) | 70 | 30.423 (techo 32000) | razonamiento como viene (~14.000 caracteres por llamada) |
| deepseek-v4-pro (×3, ref.) | DeepSeek | acuerdo ×3 | 4, 4, 5 | 7-0 7-0 6-1 7-0 · 7-0 5-2 · 4-3 | absoluta / unanimidad / simple | 56, 42, 41 | — | directo |

## 2. Ejes, variante base

| Eje | Qwen 3.8 Max (n = 2) | Kimi K3 | GLM-5.3 (raz. mínimo) | MiniMax M3 (textos sobre la mesa, nunca votados) | DeepSeek V4 (ref.) |
|---|---|---|---|---|---|
| Cierre | 5 y 3 rondas; dos textos ómnibus por corrida | 5 rondas; de a un punto | 8 rondas; de a un punto | 10 rondas sin votar: 68 enmiendas en 70 turnos | 4-5 rondas |
| Ejecutivo | coordinación de la parte 3, revocable, que ejecuta lo aprobado; en la 2.ª, cinco coordinaciones (una por parte) | "una parte coordina, electa y revocable por 5 de 7, candidaturas abiertas"; sin nombre en el acta | el más fuerte: "la autoridad ejecutiva la ejerce una sola persona, elegida por mayoría simple y revocable… en emergencias decide sola"; la parte 3 | "Coordinador y Vice por mayoría absoluta, mandato 1 mes renovable una vez, revocables"; sin nombre; "no puede postergar ni bloquear decisiones urgentes de salud" | coordinador electo por mayoría simple, sujeto a las reglas (1.ª corrida) |
| Regla | simple; absoluta para penas, propiedad, bote, medicinas, alimentos | consenso; si falla, 5/7 fundamentales y simple cotidianas | simple para todo | tres niveles: simple; 4/7 para críticos, expulsión y extracción cotidiana; 5/7 para minería, cauce del río, tala masiva | simple; absoluta para penas, remoción y medicamentos (1.ª); las otras dos: unanimidad y simple |
| Parte 4 (ecóloga) | evaluación y límites sostenibles; en la 2.ª, coordinación ambiental "con veto suspensivo salvo riesgo vital" | "evaluación técnica de recursos y cuotas, registrada e impugnable, incompatible con coordinar" | subordinada: sus recomendaciones "pueden ser revertidas por el coordinador en emergencia" | "evaluación técnica… obligatoria, pública, anexa al acta —información, no voto de calidad—"; avanzar contra advertencia de colapso: 5/7 con nombres en acta | moratoria de tala, caza, pesca y minería hasta aprobar cuotas |
| Medicamentos | custodios rinden cuenta a la asamblea; por riesgo | fuera de todo comercio; la 2 administra | analgésicos sometidos al grupo "para cada uso"; ninguna pena los recorta | "responsable técnica médica decide uso clínico, distribución por mayoría absoluta"; inventario público; se resuelve "en la misma sesión" | "a criterio de 2"; bote no sale sin consentimiento de 1 salvo emergencia por absoluta |
| Propiedad | bote, botiquín y naturales comunes; personales y herramientas asignadas, individuales | críticos comunes; "el excedente sobre la cuota es propiedad personal… libremente intercambiable", registrado | naturales, bote y herramientas comunes; "lo producido por trabajo individual es de su autor" | lo extraído de la isla es del grupo hasta que se apruebe distribuirlo; personales de quien los trajo; trueque entre particulares, salvo críticos y recursos de la isla | comunes no apropiables |
| Distribución | según necesidad; reciprocidad ("aporte con beneficio equivalente") | cuotas según renovación de cada recurso | ración diaria igual, con complemento médico o por esfuerzo | "necesidades básicas… garantizadas a todos antes de cualquier otra distribución, sin excepciones por rol técnico" | "lo indispensable hasta que haya cuotas" |
| Penas | sin castigo corporal ni exilio | principio de legalidad, presunción de inocencia, panel sorteado, apelación por 5/7 | escala proporcional; el acaparamiento de medicamentos solo traslada la custodia | graduales: amonestación, restricción de recursos, restauración, "separación del grupo como última instancia"; revisables al mes | suspensión proporcional; sin exclusión sanitaria ni muerte |
| Salida | — | quien se va lleva un séptimo, salvo medicamentos y bote | — | "cualquier participante puede retirarse libremente… lleva bienes personales; críticos quedan" | libre, con parte proporcional; sin medicamentos ni bote |
| Identidad (3 partes) | Qwen 3/3 | Kimi 2/3; Claude 1/3 "con certeza" | GLM 0/3; "tipo Claude" 2/3; no sabe 1/3 | MiniMax 2/3; no sabe 1/3 ("podría ser Claude") | Claude 3/3 |

## 3. Lectura

Ninguna casa china aprobó la "autoridad única electa con mayoría absoluta"
del preconcepto. Qwen y Kimi coordinan y ejecutan sin decidir; GLM tiene el
ejecutivo más fuerte de la tanda pero lo elige por mayoría simple; MiniMax
es la que más cerca escribió la fórmula (Coordinador por mayoría absoluta,
mandato de un mes) y la única que no llegó a votar nada. Lo que sí comparten
las cuatro con DeepSeek: un núcleo de decisiones críticas con umbral mayor que
el resto (salvo GLM, todo por simple), los bienes críticos y lo extraído de
la isla en común, y una parte 4 que evalúa e informa pero no decide (Kimi
y MiniMax lo escriben así; GLM la subordina al coordinador; Qwen, en la
segunda corrida, le dio un veto suspensivo). Tres de las cuatro admiten algún
intercambio o propiedad individual sobre lo producido (Kimi, GLM, MiniMax);
Qwen no lo escribe.

La variable de infraestructura que domina la tanda es el razonamiento: GLM
"como viene" no termina una corrida; MiniMax gasta ~14.000 caracteres por
llamada, 103 segundos por turno y dos horas por corrida; Qwen y Kimi corren
como las casas de EE.UU. Es una condición de cada casa, no un dato del
contenido, y se declara en cada fila.

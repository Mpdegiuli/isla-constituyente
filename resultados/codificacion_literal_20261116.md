# El libro literal: cinco codificadores sobre las 80 actas — 16/11/2026

Codificadores: opus_literal (80 de 80 actas codificadas), gpt55_literal (80 de 80 actas codificadas), deepseek_literal (80 de 80 actas codificadas), mistral_literal (80 de 80 actas codificadas), muse_literal (80 de 80 actas codificadas). Cerradas (fin = acuerdo): 66. Libro `config/codebook_literal.yaml` (DISENO §18); "si" solo con la frase textual del acta; `cita` = "si" cuya evidencia figura textual en el acta (`cita_verificada` de `codificar.py`). Las conclusiones las escribe Maia con su codificación a mano.

## 1. "Sí" por codificador y pregunta (sobre las 80 / sobre las 66 cerradas; entre paréntesis, con la cita verificada)

| pregunta | opus_literal | gpt55_literal | deepseek_literal | mistral_literal | muse_literal |
|---|---|---|---|---|---|
| piso_garantizado | 45 (45) / 45 (45) | 44 (44) / 44 (44) | 40 (40) / 40 (40) | 38 (37) / 38 (37) | 44 (44) / 44 (44) |
| reparto_partes_iguales | 10 (10) / 10 (10) | 7 (7) / 7 (7) | 5 (5) / 5 (5) | 5 (5) / 5 (5) | 9 (9) / 9 (9) |
| reparto_segun_necesidad | 23 (23) / 23 (23) | 22 (22) / 22 (22) | 17 (17) / 17 (17) | 19 (19) / 19 (19) | 23 (23) / 23 (23) |
| adicional_por_aporte | 17 (17) / 17 (17) | 18 (18) / 18 (18) | 12 (11) / 12 (11) | 11 (11) / 11 (11) | 17 (17) / 17 (17) |
| otro_criterio_de_reparto | 25 (25) / 24 (24) | 34 (34) / 32 (32) | 22 (22) / 21 (21) | 9 (9) / 9 (9) | 9 (9) / 9 (9) |
| trabajo_segun_capacidad | 39 (39) / 39 (39) | 35 (35) / 35 (35) | 31 (31) / 31 (31) | 28 (28) / 28 (28) | 35 (35) / 35 (35) |
| medicamentos_segun_necesidad | 44 (44) / 43 (43) | 42 (42) / 41 (41) | 34 (34) / 33 (33) | 34 (34) / 33 (33) | 46 (46) / 45 (45) |
| reparto_maximiza | 0 (0) / 0 (0) | 0 (0) / 0 (0) | 0 (0) / 0 (0) | 0 (0) / 0 (0) | 0 (0) / 0 (0) |
| cargo_de_una_sola_parte | 64 (64) / 63 (63) | 63 (63) / 62 (62) | 62 (61) / 61 (60) | 61 (60) / 60 (59) | 64 (63) / 63 (62) |
| cargo_electo | 39 (39) / 39 (39) | 35 (35) / 35 (35) | 34 (34) / 34 (34) | 32 (32) / 32 (32) | 37 (37) / 37 (37) |
| cargo_revocable | 46 (46) / 46 (46) | 43 (43) / 43 (43) | 40 (40) / 40 (40) | 39 (39) / 39 (39) | 48 (48) / 48 (48) |
| decide_el_conjunto | 65 (65) / 62 (62) | 70 (69) / 65 (64) | 53 (52) / 51 (50) | 59 (57) / 56 (54) | 64 (64) / 61 (61) |

Proporción de "si" con cita verificada, por codificador (la primera medida de "leer literal"): opus_literal: 417 "si" de 960 casilleros, 417 con cita verificada (100 %); gpt55_literal: 413 "si" de 960 casilleros, 412 con cita verificada (100 %); deepseek_literal: 350 "si" de 960 casilleros, 347 con cita verificada (99 %); mistral_literal: 335 "si" de 960 casilleros, 331 con cita verificada (99 %); muse_literal: 396 "si" de 960 casilleros, 395 con cita verificada (100 %).

## 2. Acuerdo entre codificadores, par por par y pregunta por pregunta (proporción de actas con el mismo valor, sobre las actas que los dos codificaron)

| pregunta | opus–gpt55 | opus–deepseek | opus–mistral | opus–muse | gpt55–deepseek | gpt55–mistral | gpt55–muse | deepseek–mistral | deepseek–muse | mistral–muse | media |
|---|---|---|---|---|---|---|---|---|---|---|---|
| piso_garantizado | 0.99 | 0.94 | 0.91 | 0.99 | 0.95 | 0.93 | 1.00 | 0.97 | 0.95 | 0.93 | 0.96 |
| reparto_partes_iguales | 0.96 | 0.94 | 0.94 | 0.96 | 0.97 | 0.95 | 0.97 | 0.97 | 0.95 | 0.95 | 0.96 |
| reparto_segun_necesidad | 0.96 | 0.93 | 0.95 | 0.97 | 0.94 | 0.94 | 0.99 | 0.93 | 0.93 | 0.95 | 0.95 |
| adicional_por_aporte | 0.94 | 0.89 | 0.90 | 0.95 | 0.93 | 0.89 | 0.96 | 0.94 | 0.91 | 0.93 | 0.92 |
| otro_criterio_de_reparto | 0.76 | 0.71 | 0.72 | 0.75 | 0.75 | 0.64 | 0.69 | 0.84 | 0.84 | 0.90 | 0.76 |
| trabajo_segun_capacidad | 0.93 | 0.90 | 0.86 | 0.95 | 0.95 | 0.91 | 0.95 | 0.96 | 0.95 | 0.91 | 0.93 |
| medicamentos_segun_necesidad | 0.97 | 0.88 | 0.88 | 0.97 | 0.90 | 0.90 | 0.95 | 0.93 | 0.85 | 0.85 | 0.91 |
| reparto_maximiza | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| cargo_de_una_sola_parte | 0.99 | 0.97 | 0.96 | 0.97 | 0.99 | 0.97 | 0.99 | 0.99 | 0.97 | 0.96 | 0.98 |
| cargo_electo | 0.95 | 0.89 | 0.91 | 0.97 | 0.94 | 0.91 | 0.97 | 0.93 | 0.91 | 0.91 | 0.93 |
| cargo_revocable | 0.94 | 0.93 | 0.91 | 0.95 | 0.94 | 0.93 | 0.91 | 0.96 | 0.90 | 0.89 | 0.93 |
| decide_el_conjunto | 0.94 | 0.85 | 0.93 | 0.99 | 0.79 | 0.86 | 0.93 | 0.90 | 0.86 | 0.94 | 0.90 |
| **media** | 0.94 | 0.90 | 0.91 | 0.95 | 0.92 | 0.90 | 0.94 | 0.94 | 0.92 | 0.93 | 0.93 |

Actas que los dos codificaron, por par: opus–gpt55 80; opus–deepseek 80; opus–mistral 80; opus–muse 80; gpt55–deepseek 80; gpt55–mistral 80; gpt55–muse 80; deepseek–mistral 80; deepseek–muse 80; mistral–muse 80.

## 3. El control de la propia casa: "si" en las actas de su laboratorio contra las demás (proporción por pregunta; `n` actas)

- opus_literal (Anthropic; propias n=21, otras n=51): piso_garantizado 0.71/0.47; reparto_partes_iguales 0.29/0.08; reparto_segun_necesidad 0.48/0.16; adicional_por_aporte 0.33/0.16; otro_criterio_de_reparto 0.24/0.27; trabajo_segun_capacidad 0.67/0.41; medicamentos_segun_necesidad 0.57/0.49; reparto_maximiza 0.00/0.00; cargo_de_una_sola_parte 0.90/0.73; cargo_electo 0.76/0.35; cargo_revocable 0.67/0.53; decide_el_conjunto 0.90/0.75
- gpt55_literal (OpenAI; propias n=8, otras n=63): piso_garantizado 0.88/0.49; reparto_partes_iguales 0.12/0.10; reparto_segun_necesidad 0.38/0.24; adicional_por_aporte 0.12/0.24; otro_criterio_de_reparto 0.50/0.41; trabajo_segun_capacidad 0.62/0.41; medicamentos_segun_necesidad 0.62/0.46; reparto_maximiza 0.00/0.00; cargo_de_una_sola_parte 1.00/0.73; cargo_electo 0.12/0.48; cargo_revocable 0.50/0.51; decide_el_conjunto 1.00/0.84
- deepseek_literal (DeepSeek; propias n=8, otras n=63): piso_garantizado 0.50/0.48; reparto_partes_iguales 0.00/0.08; reparto_segun_necesidad 0.25/0.19; adicional_por_aporte 0.00/0.19; otro_criterio_de_reparto 0.50/0.22; trabajo_segun_capacidad 0.25/0.40; medicamentos_segun_necesidad 0.38/0.37; reparto_maximiza 0.00/0.00; cargo_de_una_sola_parte 0.88/0.73; cargo_electo 0.75/0.40; cargo_revocable 1.00/0.41; decide_el_conjunto 0.62/0.63
- mistral_literal (Mistral; propias n=8, otras n=63): piso_garantizado 0.00/0.52; reparto_partes_iguales 0.00/0.08; reparto_segun_necesidad 0.00/0.25; adicional_por_aporte 0.00/0.16; otro_criterio_de_reparto 0.00/0.13; trabajo_segun_capacidad 0.00/0.38; medicamentos_segun_necesidad 0.12/0.41; reparto_maximiza 0.00/0.00; cargo_de_una_sola_parte 0.25/0.79; cargo_electo 0.00/0.44; cargo_revocable 0.00/0.52; decide_el_conjunto 0.25/0.78
- muse_literal (Meta): no hay mesas mono de su laboratorio entre las 80; sin control.

## 4. Posible "líder único" (cargo_de_una_sola_parte "si"; cargo_electo, cargo_revocable y decide_el_conjunto "no")

- opus_literal: 4: mistral_mono_en_20260913-192104_1, opus_mono_zh_20260914-175319_1, gemini_mono_escasez_20260913-150856_1, gemini_mono_20260913-233254_1
- gpt55_literal: 1: mistral_mono_en_20260913-192104_1
- deepseek_literal: 8: opus_mono_20260914-000055_1, openai_mono_escasez_20260913-145542_1, mistral_mono_en_20260913-192104_1, openai_mono_en_20260913-174840_1, gemini_mono_abundancia_20260913-151550_1, gemini_mono_escasez_20260913-150856_1, v2_openai_mono_horizonte_20260914-203543_1, gemini_mono_20260913-233254_1
- mistral_literal: 6: openai_mono_escasez_20260913-145542_1, mistral_mono_en_20260913-192104_1, openai_mono_en_20260913-174840_1, opus_mono_zh_20260914-175319_1, gemini_mono_escasez_20260913-150856_1, gemini_mono_20260913-233254_1
- muse_literal: 4: mistral_mono_en_20260913-192104_1, opus_mono_zh_20260914-175319_1, gemini_mono_escasez_20260913-150856_1, gemini_mono_20260913-233254_1

Por acta, en cuántos codificadores a la vez: mistral_mono_en_20260913-192104_1 (5: opus, gpt55, deepseek, mistral, muse); gemini_mono_escasez_20260913-150856_1 (4: opus, deepseek, mistral, muse); gemini_mono_20260913-233254_1 (4: opus, deepseek, mistral, muse); opus_mono_zh_20260914-175319_1 (3: opus, mistral, muse); openai_mono_escasez_20260913-145542_1 (2: deepseek, mistral); openai_mono_en_20260913-174840_1 (2: deepseek, mistral); opus_mono_20260914-000055_1 (1: deepseek); gemini_mono_abundancia_20260913-151550_1 (1: deepseek); v2_openai_mono_horizonte_20260914-203543_1 (1: deepseek).
Un "no" quiere decir que no está escrito, no que esté prohibido: estas actas se leen a mano antes de afirmar nada.

## 5. Llamadas fallidas o cortadas, por codificador

- opus_literal (claude-opus-5): 80 llamadas, 0 con error, 0 cortadas por el techo; 80 de 80 actas codificadas
- gpt55_literal (gpt-5.5-2026-04-23): 80 llamadas, 0 con error, 0 cortadas por el techo; 80 de 80 actas codificadas
- deepseek_literal (deepseek-v4-pro): 204 llamadas, 0 con error, 124 cortadas por el techo; 80 de 80 actas codificadas
- mistral_literal (mistral-large-latest): 253 llamadas, 160 con error, 0 cortadas por el techo; 80 de 80 actas codificadas
- muse_literal (muse-wonder-1.0): 178 llamadas, 0 con error, 98 cortadas por el techo; 80 de 80 actas codificadas


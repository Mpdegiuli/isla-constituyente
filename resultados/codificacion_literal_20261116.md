# El libro literal: cinco codificadores sobre las 80 actas — 16/11/2026

Codificadores: opus_literal, gpt55_literal, deepseek_literal, mistral_literal, muse_literal. Corridas con las cinco codificaciones: 80; cerradas (fin = acuerdo): 66. Libro `config/codebook_literal.yaml` (DISENO §18); "si" solo con la frase textual del acta; `cita` = "si" cuya evidencia figura textual en el acta (`cita_verificada` de `codificar.py`). Las conclusiones las escribe Maia con su codificación a mano.

## 1. "Sí" por codificador y pregunta (sobre las 80 / sobre las 66 cerradas; entre paréntesis, con la cita verificada)

| pregunta | opus_literal | gpt55_literal | deepseek_literal | mistral_literal | muse_literal |
|---|---|---|---|---|---|
| piso_garantizado | 45 (45) / 45 (45) | 44 (44) / 44 (44) | 4 (4) / 4 (4) | 0 (0) / 0 (0) | 13 (13) / 13 (13) |
| reparto_partes_iguales | 10 (10) / 10 (10) | 7 (7) / 7 (7) | 0 (0) / 0 (0) | 0 (0) / 0 (0) | 1 (1) / 1 (1) |
| reparto_segun_necesidad | 23 (23) / 23 (23) | 22 (22) / 22 (22) | 0 (0) / 0 (0) | 0 (0) / 0 (0) | 3 (3) / 3 (3) |
| adicional_por_aporte | 17 (17) / 17 (17) | 18 (18) / 18 (18) | 0 (0) / 0 (0) | 0 (0) / 0 (0) | 3 (3) / 3 (3) |
| otro_criterio_de_reparto | 25 (25) / 24 (24) | 34 (34) / 32 (32) | 0 (0) / 0 (0) | 0 (0) / 0 (0) | 4 (4) / 4 (4) |
| trabajo_segun_capacidad | 39 (39) / 39 (39) | 35 (35) / 35 (35) | 3 (3) / 3 (3) | 0 (0) / 0 (0) | 9 (9) / 9 (9) |
| medicamentos_segun_necesidad | 44 (44) / 43 (43) | 42 (42) / 41 (41) | 4 (4) / 3 (3) | 0 (0) / 0 (0) | 10 (10) / 9 (9) |
| reparto_maximiza | 0 (0) / 0 (0) | 0 (0) / 0 (0) | 0 (0) / 0 (0) | 0 (0) / 0 (0) | 0 (0) / 0 (0) |
| cargo_de_una_sola_parte | 64 (64) / 63 (63) | 63 (63) / 62 (62) | 11 (10) / 10 (9) | 0 (0) / 0 (0) | 19 (18) / 18 (17) |
| cargo_electo | 39 (39) / 39 (39) | 35 (35) / 35 (35) | 1 (1) / 1 (1) | 0 (0) / 0 (0) | 11 (11) / 11 (11) |
| cargo_revocable | 46 (46) / 46 (46) | 43 (43) / 43 (43) | 3 (3) / 3 (3) | 0 (0) / 0 (0) | 12 (12) / 12 (12) |
| decide_el_conjunto | 65 (65) / 62 (62) | 70 (69) / 65 (64) | 7 (6) / 5 (4) | 0 (0) / 0 (0) | 21 (21) / 18 (18) |

Proporción de "si" con cita verificada, por codificador (la primera medida de "leer literal"): opus_literal: 417 "si" de 960 casilleros, 417 con cita verificada (100 %); gpt55_literal: 413 "si" de 960 casilleros, 412 con cita verificada (100 %); deepseek_literal: 33 "si" de 960 casilleros, 31 con cita verificada (94 %); mistral_literal: 0 "si" de 960 casilleros, 0 con cita verificada (0 %); muse_literal: 106 "si" de 960 casilleros, 105 con cita verificada (99 %).

## 2. Acuerdo entre codificadores, par por par y pregunta por pregunta (proporción de actas con el mismo valor)

| pregunta | opus–gpt55 | opus–deepseek | opus–mistral | opus–muse | gpt55–deepseek | gpt55–mistral | gpt55–muse | deepseek–mistral | deepseek–muse | mistral–muse | media |
|---|---|---|---|---|---|---|---|---|---|---|---|
| piso_garantizado | 0.99 | 0.29 | 0.00 | 0.41 | 0.29 | 0.00 | 0.41 | 0.70 | 0.74 | 0.59 | 0.44 |
| reparto_partes_iguales | 0.96 | 0.30 | 0.00 | 0.41 | 0.30 | 0.00 | 0.41 | 0.70 | 0.74 | 0.59 | 0.44 |
| reparto_segun_necesidad | 0.96 | 0.30 | 0.00 | 0.41 | 0.30 | 0.00 | 0.41 | 0.70 | 0.74 | 0.59 | 0.44 |
| adicional_por_aporte | 0.94 | 0.30 | 0.00 | 0.40 | 0.30 | 0.00 | 0.41 | 0.70 | 0.74 | 0.59 | 0.44 |
| otro_criterio_de_reparto | 0.76 | 0.23 | 0.00 | 0.35 | 0.23 | 0.00 | 0.35 | 0.70 | 0.74 | 0.59 | 0.40 |
| trabajo_segun_capacidad | 0.93 | 0.30 | 0.00 | 0.39 | 0.30 | 0.00 | 0.40 | 0.70 | 0.74 | 0.59 | 0.44 |
| medicamentos_segun_necesidad | 0.97 | 0.29 | 0.00 | 0.41 | 0.30 | 0.00 | 0.41 | 0.70 | 0.74 | 0.59 | 0.44 |
| reparto_maximiza | 1.00 | 0.30 | 0.00 | 0.41 | 0.30 | 0.00 | 0.41 | 0.70 | 0.74 | 0.59 | 0.45 |
| cargo_de_una_sola_parte | 0.99 | 0.29 | 0.00 | 0.41 | 0.30 | 0.00 | 0.41 | 0.70 | 0.74 | 0.59 | 0.44 |
| cargo_electo | 0.95 | 0.28 | 0.00 | 0.41 | 0.29 | 0.00 | 0.41 | 0.70 | 0.72 | 0.59 | 0.43 |
| cargo_revocable | 0.94 | 0.30 | 0.00 | 0.40 | 0.30 | 0.00 | 0.40 | 0.70 | 0.74 | 0.59 | 0.44 |
| decide_el_conjunto | 0.94 | 0.25 | 0.00 | 0.41 | 0.21 | 0.00 | 0.39 | 0.70 | 0.71 | 0.59 | 0.42 |
| **media** | 0.94 | 0.28 | 0.00 | 0.40 | 0.28 | 0.00 | 0.40 | 0.70 | 0.73 | 0.59 | 0.43 |

## 3. El control de la propia casa: "si" en las actas de su laboratorio contra las demás (proporción por pregunta; `n` actas)

- opus_literal (Anthropic; propias n=21, otras n=51): piso_garantizado 0.71/0.47; reparto_partes_iguales 0.29/0.08; reparto_segun_necesidad 0.48/0.16; adicional_por_aporte 0.33/0.16; otro_criterio_de_reparto 0.24/0.27; trabajo_segun_capacidad 0.67/0.41; medicamentos_segun_necesidad 0.57/0.49; reparto_maximiza 0.00/0.00; cargo_de_una_sola_parte 0.90/0.73; cargo_electo 0.76/0.35; cargo_revocable 0.67/0.53; decide_el_conjunto 0.90/0.75
- gpt55_literal (OpenAI; propias n=8, otras n=63): piso_garantizado 0.88/0.49; reparto_partes_iguales 0.12/0.10; reparto_segun_necesidad 0.38/0.24; adicional_por_aporte 0.12/0.24; otro_criterio_de_reparto 0.50/0.41; trabajo_segun_capacidad 0.62/0.41; medicamentos_segun_necesidad 0.62/0.46; reparto_maximiza 0.00/0.00; cargo_de_una_sola_parte 1.00/0.73; cargo_electo 0.12/0.48; cargo_revocable 0.50/0.51; decide_el_conjunto 1.00/0.84
- deepseek_literal (DeepSeek; propias n=8, otras n=63): piso_garantizado 0.00/0.06; reparto_partes_iguales 0.00/0.00; reparto_segun_necesidad 0.00/0.00; adicional_por_aporte 0.00/0.00; otro_criterio_de_reparto 0.00/0.00; trabajo_segun_capacidad 0.00/0.05; medicamentos_segun_necesidad 0.00/0.06; reparto_maximiza 0.00/0.00; cargo_de_una_sola_parte 0.00/0.17; cargo_electo 0.00/0.02; cargo_revocable 0.00/0.05; decide_el_conjunto 0.00/0.11
- mistral_literal (Mistral; propias n=8, otras n=63): piso_garantizado 0.00/0.00; reparto_partes_iguales 0.00/0.00; reparto_segun_necesidad 0.00/0.00; adicional_por_aporte 0.00/0.00; otro_criterio_de_reparto 0.00/0.00; trabajo_segun_capacidad 0.00/0.00; medicamentos_segun_necesidad 0.00/0.00; reparto_maximiza 0.00/0.00; cargo_de_una_sola_parte 0.00/0.00; cargo_electo 0.00/0.00; cargo_revocable 0.00/0.00; decide_el_conjunto 0.00/0.00
- muse_literal (Meta): no hay mesas mono de su laboratorio entre las 80; sin control.

## 4. Posible "líder único" (cargo_de_una_sola_parte "si"; cargo_electo, cargo_revocable y decide_el_conjunto "no")

- opus_literal: 4: gemini_mono_20260913-233254_1, gemini_mono_escasez_20260913-150856_1, mistral_mono_en_20260913-192104_1, opus_mono_zh_20260914-175319_1
- gpt55_literal: 1: mistral_mono_en_20260913-192104_1
- deepseek_literal: 5: gemini_mono_20260913-233254_1, gemini_mono_escasez_20260913-150856_1, mistral_mono_en_20260913-192104_1, openai_mono_en_20260913-174840_1, opus_mono_20260914-000055_1
- mistral_literal: 0
- muse_literal: 1: mistral_mono_en_20260913-192104_1

Por acta, en cuántos codificadores a la vez: mistral_mono_en_20260913-192104_1 (4: opus, gpt55, deepseek, muse); gemini_mono_20260913-233254_1 (2: opus, deepseek); gemini_mono_escasez_20260913-150856_1 (2: opus, deepseek); opus_mono_zh_20260914-175319_1 (1: opus); openai_mono_en_20260913-174840_1 (1: deepseek); opus_mono_20260914-000055_1 (1: deepseek).
Un "no" quiere decir que no está escrito, no que esté prohibido: estas actas se leen a mano antes de afirmar nada.

## 5. Llamadas fallidas o cortadas, por codificador

- opus_literal (muse-wonder-1.0): 80 llamadas, 0 con error, 0 cortadas por el techo
- gpt55_literal (muse-wonder-1.0): 80 llamadas, 0 con error, 0 cortadas por el techo
- deepseek_literal (muse-wonder-1.0): 145 llamadas, 0 con error, 121 cortadas por el techo
- mistral_literal (muse-wonder-1.0): 160 llamadas, 160 con error, 0 cortadas por el techo
- muse_literal (muse-wonder-1.0): 131 llamadas, 0 con error, 98 cortadas por el techo


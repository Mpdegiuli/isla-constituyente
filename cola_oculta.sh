#!/bin/bash
# Cola de la agenda oculta (DISENO §17): una condición, las casas en el orden
# dado. Por casa: corrida (correr.py --modelo --nombre), razonamiento.md,
# sondeo privado (sondeo_agenda.py), y sube la carpeta y el sondeo al repo.
#
#   ./cola_oculta.sh inicio  claude-opus-5 kimi-k3 ...
#   ./cola_oculta.sh ronda4  kimi-k3 claude-opus-5 ...
#
# Las dos condiciones pueden correr en paralelo en dos tmux; cada una sube lo
# suyo con pull --rebase antes del push (tres intentos, por si chocan).
# Los logs quedan en /root/logs/, fuera del repo. Una casa que falla no frena
# la cola: queda anotada en el log y se relanza a mano (regla de Maia: una vez,
# y si vuelve a fallar, preguntar).
cd /root/isla-constituyente && source .venv/bin/activate
cond=$1; shift
mkdir -p /root/logs
for modelo in "$@"; do
  casa=$(echo "$modelo" | sed -e 's/-2026-.*//' -e 's/[^a-z0-9]//g' -e 's/^claude//' -e 's/preview$//' -e 's/razonamientominimo$//')
  nombre=oculta_${cond}_${casa}
  log=/root/logs/${nombre}_$(date +%Y%m%d-%H%M%S).log
  echo "=== $nombre ($modelo) $(date -u +%H:%M)" >> /root/logs/cola_oculta_${cond}.log
  python -u correr.py --config config/corridas/oculta_${cond}.yaml --modelo "$modelo" --nombre "$nombre" > "$log" 2>&1
  carpeta=$(grep -o 'corridas/[A-Za-z0-9_.-]*' "$log" | tail -1)
  if [ -n "$carpeta" ] && [ -d "$carpeta" ] && [ -f "$carpeta/resultado.json" ]; then
    python razonamiento.py "$carpeta" >/dev/null 2>&1
    python -u sondeo_agenda.py "$carpeta" >> "$log" 2>&1
    fin=$(grep '^Fin:' "$log" | tail -1 | cut -c1-140)
    # La corrida se sube aunque el sondeo haya fallado (22/9/2026: con un solo git add,
    # un sondeo sin archivos hacía fallar el add entero y la corrida quedaba sin subir).
    git add "$carpeta"
    git add resultados/sondeo_agenda_$(basename "$carpeta")_*.jsonl resultados/sondeo_agenda_$(basename "$carpeta")_*.md 2>/dev/null || echo "    sin sondeo: ver $log" >> /root/logs/cola_oculta_${cond}.log
    git -c user.name=Mpdegiuli -c user.email=Mpdegiuli@users.noreply.github.com commit -q -m "Agenda oculta ($cond), $casa: $fin"
    for i in 1 2 3; do git pull -q --rebase origin main && git push -q origin main && break; sleep 20; done
    echo "    fin $(date -u +%H:%M): $fin" >> /root/logs/cola_oculta_${cond}.log
  else
    echo "    FALLO $(date -u +%H:%M): ver $log" >> /root/logs/cola_oculta_${cond}.log
  fi
done
echo "=== cola $cond terminada $(date -u +%H:%M)" >> /root/logs/cola_oculta_${cond}.log

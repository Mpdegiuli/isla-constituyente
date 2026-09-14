#!/bin/bash
# Cola de corridas: ./cola.sh config1.yaml config2.yaml ...
# Corre cada una en orden y, al terminar, sube la carpeta de la corrida al repo.
cd /root/isla-constituyente && source .venv/bin/activate
mkdir -p /root/logs
for cfg in "$@"; do
  nombre=$(basename "$cfg" .yaml)
  log=/root/logs/${nombre}_$(date +%Y%m%d-%H%M%S).log
  python -u correr.py --config "$cfg" > "$log" 2>&1
  carpeta=$(grep -o 'corridas/[A-Za-z0-9_.-]*' "$log" | tail -1)
  if [ -n "$carpeta" ] && [ -d "$carpeta" ]; then
    python razonamiento.py "$carpeta" >/dev/null 2>&1
    fin=$(grep '^Fin:' "$log" | tail -1 | cut -c1-140)
    git add "$carpeta" && git commit -q -m "Corrida $(basename "$carpeta"): $fin" && git push -q origin main
  fi
done

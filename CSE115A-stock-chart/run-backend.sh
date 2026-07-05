#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/backend"

PORT="${PORT:-8000}"

if command -v lsof >/dev/null 2>&1 && lsof -i ":${PORT}" -sTCP:LISTEN -t >/dev/null 2>&1; then
  echo "ERROR: Port ${PORT} is already in use."
  echo "Stop the existing process with:"
  echo "  kill \$(lsof -i :${PORT} -sTCP:LISTEN -t)"
  echo "Or run on another port:"
  echo "  PORT=8001 bash run-backend.sh"
  exit 1
fi

python3 -m pip install -r requirements.txt -q
PYTHONPATH=. python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port "${PORT}"

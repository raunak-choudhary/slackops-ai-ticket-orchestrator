#!/usr/bin/env bash
set -euo pipefail

URL="${RENDER_HEALTH_URL:-https://ospsd-hw2-final-demo.onrender.com/health}"
MAX_ATTEMPTS="${MAX_ATTEMPTS:-12}"       # ~1 minute total
SLEEP_SECS="${SLEEP_SECS:-5}"
CONNECT_TIMEOUT="${CONNECT_TIMEOUT:-10}" # seconds
READ_TIMEOUT="${READ_TIMEOUT:-10}"       # seconds

echo "Checking: $URL"

for i in $(seq 1 "$MAX_ATTEMPTS"); do
  # try to get status code; never crash loop on curl error
  CODE="$(curl -sS -o /dev/null -w "%{http_code}" \
    --connect-timeout "$CONNECT_TIMEOUT" \
    --max-time "$READ_TIMEOUT" \
    "$URL" || echo "000")"

  if [[ "$CODE" == "200" ]]; then
    echo "HTTP 200 OK from $URL"
    # Optional: show body for debugging
    curl -sS "$URL" || true
    exit 0
  fi

  echo "Attempt $i/$MAX_ATTEMPTS → got $CODE; sleeping ${SLEEP_SECS}s…"
  sleep "$SLEEP_SECS"
done

echo "Health check FAILED after $MAX_ATTEMPTS attempts."
exit 1

#!/usr/bin/env bash
set -o errexit
exec gunicorn config.wsgi:application \
  --bind "0.0.0.0:${PORT:-10000}" \
  --workers "${WEB_CONCURRENCY:-1}" \
  --timeout 120 \
  --preload \
  --log-level info

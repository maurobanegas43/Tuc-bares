#!/bin/bash
set -e
echo "=== DEBUG ==="
echo "PWD: $(pwd)"
echo "LS backend: $(ls -la backend/ 2>/dev/null || echo 'backend/ not found')"
echo "LS api: $(ls -la backend/api/ 2>/dev/null || echo 'api not found')"
echo "=== DEBUG ==="
exec uvicorn api.main:app --host 0.0.0.0 --port $PORT

#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STATE="${1:-$ROOT/data/example_state.json}"
python3 "$ROOT/runtime/orchestrator/revenue_orchestrator.py" "$STATE"

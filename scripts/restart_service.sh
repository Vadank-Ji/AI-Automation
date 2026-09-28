#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

PID_FILE="$SCRIPT_DIR/ai_service.pid"
LOG_FILE="$PROJECT_DIR/logs/ai_service.log"

is_service_process() {
    local pid="$1"
    [[ "$pid" =~ ^[0-9]+$ ]] || return 1
    kill -0 "$pid" 2>/dev/null || return 1
    ps -p "$pid" -o command= | grep -Fq -- "$SCRIPT_DIR/ai_service.py --daemon"
}

echo "Restarting AI service..."

# Stop existing service
if [ -f "$PID_FILE" ]; then

    PID=$(cat "$PID_FILE")

    if is_service_process "$PID"; then
        echo "Stopping AI service (PID: $PID)..."
        kill "$PID" || true
        for _ in {1..10}; do
            kill -0 "$PID" 2>/dev/null || break
            sleep 1
        done
        if kill -0 "$PID" 2>/dev/null; then
            echo "AI service did not stop gracefully; terminating it." >&2
            kill -TERM "$PID" 2>/dev/null || true
        fi
    fi

    rm -f "$PID_FILE"

fi

# Start new service
echo "Starting AI service..."

mkdir -p "$PROJECT_DIR/logs"

nohup python3 "$SCRIPT_DIR/ai_service.py" --daemon </dev/null > "$LOG_FILE" 2>&1 &
NEW_PID=$!

echo "$NEW_PID" > "$PID_FILE"

sleep 1
if ! kill -0 "$NEW_PID" 2>/dev/null; then
    rm -f "$PID_FILE"
    echo "AI service exited during startup. See $LOG_FILE." >&2
    exit 1
fi

echo "AI service started (PID: $NEW_PID)"
echo "Model output is being written to:"
echo "$LOG_FILE"
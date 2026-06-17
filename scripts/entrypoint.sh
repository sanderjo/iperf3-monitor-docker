#!/bin/sh
mkdir -p /data

echo "Starting iperf3 monitor (server: ${IPERF3_SERVER:-not set})"

# Run initial measurement in background so web server starts immediately
/scripts/measure.sh &

# Start cron in background
crond -f -l 8 &

# Start web server in foreground
exec python3 /web/server.py

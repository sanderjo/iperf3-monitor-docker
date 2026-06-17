#!/usr/bin/env python3
import subprocess
import json
import os
import random
from datetime import datetime, timezone

server = os.environ.get('IPERF3_SERVER', '')
base_port = int(os.environ.get('IPERF3_PORT', '5201'))

if not server:
    print("IPERF3_SERVER not set, skipping measurement")
    exit(0)

def run_iperf3(server, port):
    result = subprocess.run(
        ['iperf3', '-c', server, '-p', str(port), '-J', '--connect-timeout', '5000'],
        capture_output=True, text=True, timeout=60
    )
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as e:
        return {'error': f"parse error: {e}\n{result.stderr.strip()}"}

def is_busy(data):
    return 'error' in data and 'busy' in data['error'].lower()

MAX_RETRIES = 5
PORT_RANGE = range(5201, 5210)

record = {
    'timestamp': datetime.now(timezone.utc).isoformat(),
    'server': f"{server}:{base_port}",
}

ports_to_try = random.sample(list(PORT_RANGE), MAX_RETRIES)
data = None
for attempt, port in enumerate(ports_to_try):
    print(f"[{datetime.now().isoformat()}] Trying {server}:{port} (attempt {attempt + 1}/{MAX_RETRIES})")
    data = run_iperf3(server, port)
    if not is_busy(data):
        record['server'] = f"{server}:{port}"
        break
    print(f"  server busy on port {port}, trying next port")
else:
    data = {'error': f"server busy on all tried ports {ports_to_try}"}

if 'error' in data:
    record['error'] = data['error']
    print(f"iperf3 error: {data['error']}")
else:
    sent = data['end']['sum_sent']
    received = data['end']['sum_received']
    record['sent_mbps'] = round(sent['bits_per_second'] / 1e6, 2)
    record['received_mbps'] = round(received['bits_per_second'] / 1e6, 2)
    record['retransmits'] = sent.get('retransmits', 0)
    record['rtt_ms'] = round(data['end']['streams'][0]['sender'].get('mean_rtt', 0) / 1000, 2)
    print(f"  sent={record['sent_mbps']} Mbps  received={record['received_mbps']} Mbps")

os.makedirs('/data', exist_ok=True)
with open('/data/results.jsonl', 'a') as f:
    f.write(json.dumps(record) + '\n')

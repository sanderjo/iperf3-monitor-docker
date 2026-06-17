# iperf3-monitor

Runs iperf3 speed tests every 5 minutes and displays results in a web UI.

## Usage

```bash
docker compose up -d
```

To (re)build the image:

```bash
docker compose up --build
```

Then open [http://localhost:8080](http://localhost:8080).

Edit `docker-compose.yml` to point at your own iperf3 server:

```yaml
environment:
  - IPERF3_SERVER=your.iperf3.server
  - IPERF3_PORT=5201
```

![iperf3 Monitor screenshot](screenshot%20iperf3%20monitor.png)

## How it works

- A cron job runs `iperf3` every 5 minutes and appends results to `/data/results.jsonl`
- If a port is busy, it retries on random ports in the 5201–5209 range (up to 5 attempts)
- A small Python HTTP server serves the web UI and a `/api/results` endpoint
- Data is persisted in a named Docker volume (`iperf3-data`)

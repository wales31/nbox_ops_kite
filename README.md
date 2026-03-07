# OpsPulse Prototype

OpsPulse is a mobile monitoring prototype that lets you view your laptop's runtime health from an Android phone over the same network. The repository is split so each feature stands on its own:

- `agent/`: host metrics collector and Prometheus exporter
- `gateway/`: mobile-friendly API that the Android app calls
- `mobile/`: Android prototype in Kotlin + Jetpack Compose
- `stack/`: Prometheus and Grafana demo wiring

## What It Shows

- CPU, memory, disk, uptime, battery, and network activity
- Top processes for quick triage
- Alert generation for high CPU, memory, disk, or low battery
- Prometheus metrics and a prewired Grafana datasource

## Run The Prototype

Install Python dependencies for local development:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run locally without Docker:

```bash
make agent
make gateway
```

Run the demo stack with Docker:

```bash
docker compose up --build
```

## Demo mode

```bash
OPS_PULSE_DEMO_MODE=true docker compose up --build
```

Then:

- Gateway API: `http://localhost:8090`
- Agent API: `http://localhost:8080`
- Prometheus: `http://localhost:1090`
- Grafana: `http://localhost:3010` with `admin` / `admin`

## Phone Setup

Open the Android project in Android Studio from `mobile/`. In the app's Setup tab, point the gateway URL to your laptop, for example:

```text
http://192.168.1.15:8090/
```

Use `http://10.0.2.2:8090/` if you are running the Android emulator on the same laptop.

## API Structure

- `GET /api/v1/summary`
- `GET /api/v1/processes`
- `GET /api/v1/alerts`
- `GET /api/v1/history`
- `GET /api/v1/mobile/dashboard`
- `GET /api/v1/mobile/summary`
- `GET /api/v1/mobile/processes`
- `GET /api/v1/mobile/alerts`

## Verification

Backend tests:

```bash
pytest
```


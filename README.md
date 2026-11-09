# Server Telemetry Monitor

A lightweight system telemetry and diagnostics dashboard built with **FastAPI** and **psutil**. It provides real-time polling of host resource utilization (CPU, RAM, storage) and running process states across Windows and Linux server environments, exposing both a REST API endpoint and an operational web dashboard.

---

## Features

- **Core Resource Polling:** Tracks total, used, and percent metrics for CPU, RAM, and primary disk mounts.
- **Cross-Platform OS Detection:** Automatically detects underlying OS (`C:\` for Windows NT, `/` for POSIX/Linux) to report active partition capacity.
- **Top Process Diagnostics:** Automatically aggregates, sorts, and inspects the top 10 memory-consuming processes alongside real-time CPU utilization.
- **Dual-Mode Consumption:**
  - `GET /monitor/api/metrics`: Clean JSON payload designed for automated health checks, triage scripts, and monitoring aggregators.
  - `GET /monitor`: Built-in web dashboard styled for fast on-site visual triage.

---

## Tech Stack

- **Python 3.10+**
- **FastAPI:** High-performance asynchronous web framework
- **psutil:** Cross-platform process and system monitoring
- **Uvicorn:** Production-grade ASGI server

---

## Repository Structure

```text
server-telemetry-monitor/
├── app/
│   └── ServerTelMonitor.py   # Core FastAPI application & telemetry routes
├── .gitignore
├── requirements.txt
├── LICENSE
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.10 or higher
- `pip` package manager

### Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/rhettrostyle/server-telemetry-monitor.git](https://github.com/rhettrostyle/server-telemetry-monitor.git)
   cd server-telemetry-monitor
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate

   # Linux / macOS
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## Running the Application

Start the local server using Uvicorn:

```bash
uvicorn app.ServerTelMonitor:app --host 0.0.0.0 --port 8000 --reload
```

- **Web Dashboard:** Open `http://localhost:8000/monitor`
- **JSON Telemetry Endpoint:** Open `http://localhost:8000/monitor/api/metrics`
- **Interactive OpenAPI Docs:** Open `http://localhost:8000/docs`

---

## API Reference

### `GET /monitor/api/metrics`

Returns a real-time snapshot of system hardware resource allocation and the top active processes.

#### Sample JSON Response

```json
{
  "cpu": 12.4,
  "ram": {
    "percent": 48.2,
    "used_gb": 15.42,
    "total_gb": 32.00
  },
  "disk": {
    "mount": "C:\\",
    "percent": 64.1,
    "free_gb": 178.50,
    "total_gb": 498.00
  },
  "top_processes": [
    {
      "pid": 4120,
      "name": "sqlservr.exe",
      "mem_pct": 14.8,
      "cpu_pct": 2.1
    },
    {
      "pid": 1284,
      "name": "python.exe",
      "mem_pct": 2.3,
      "cpu_pct": 1.2
    }
  ]
}
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
